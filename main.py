from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated
from datetime import date, timedelta, datetime
from fastapi.responses import JSONResponse
from supabase import create_client

# =========================
# SUPABASE CONFIG
# =========================

SUPABASE_URL = "https://nwjjbwmchgzjoxdituji.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53ampid21jaGd6am94ZGl0dWppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg0ODc4NjAsImV4cCI6MjA5NDA2Mzg2MH0.5j-8oZjhlv6C2iWiT0oCtf1u0X6ys8nj3iYmhnE0ZSY"


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# BOOK MODELS
# =========================


class Books(BaseModel):

    book_id: Annotated[
        str,
        Field(..., description="Book ID")
    ]

    nameofbook: Annotated[
        str,
        Field(..., description="Book Name")
    ]

    author: Annotated[
        str,
        Field(..., description="Author Name")
    ]

    genre: Annotated[
        str,
        Field(..., description="Genre")
    ]

    quantity: Annotated[
        int,
        Field(..., gt=0)
    ]

    fineperday: Annotated[
        int,
        Field(..., gt=0)
    ]


class Books_update(BaseModel):

    nameofbook: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    quantity: Optional[int] = None
    fineperday: Optional[int] = None


# =========================
# CUSTOMER MODELS
# =========================

class Customer(BaseModel):

    book_id: Annotated[
        str,
        Field(..., description="Book ID")
    ]

    customer_name: Annotated[
        str,
        Field(..., description="Customer Name")
    ]

    days_borrowed: Annotated[
        int,
        Field(..., gt=0)
    ]

    issue_date: date = date.today()

    @computed_field
    @property
    def return_date(self) -> date:
        return self.issue_date + timedelta(days=self.days_borrowed)


class Customer_update(BaseModel):

    customer_name: Optional[str] = None
    days_borrowed: Optional[int] = None


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {"message": "Library API Running Successfully"}


# =========================
# GET BOOK
# =========================

@app.get("/book_info/{book_id}")
def book_info(book_id: str):

    response = supabase.table("books") \
        .select("*") \
        .eq("book_id", book_id) \
        .execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")

    return response.data[0]


# =========================
# CREATE BOOK
# =========================

@app.post("/create")
def create(book: Books):

    existing = supabase.table("books") \
        .select("*") \
        .eq("book_id", book.book_id) \
        .execute()

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Book already exists"
        )

    supabase.table("books").insert({

        "book_id": book.book_id,
        "nameofbook": book.nameofbook,
        "author": book.author,
        "genre": book.genre,
        "quantity": book.quantity,
        "fineperday": book.fineperday

    }).execute()

    return JSONResponse(
        status_code=200,
        content={"message": "Book added successfully"}
    )


# =========================
# UPDATE BOOK
# =========================

@app.put("/update")
def update_book(book_id: str, book: Books_update):

    response = supabase.table("books") \
        .select("*") \
        .eq("book_id", book_id) \
        .execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    update_data = book.model_dump(exclude_unset=True)

    supabase.table("books") \
        .update(update_data) \
        .eq("book_id", book_id) \
        .execute()

    return {
        "message": "Book updated successfully"
    }


# =========================
# DELETE BOOK
# =========================



# =========================
# GET CUSTOMER
# =========================

@app.get("/customer")
def get_customer(customer_id: str):

    response = supabase.table("customer") \
        .select("*") \
        .eq("customer_id", customer_id) \
        .execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return response.data[0]


# =========================
# ISSUE BOOK
# =========================

@app.post("/Customer_create")
def add_customer(customer: Customer, customer_id: str):

    # CHECK CUSTOMER EXISTS

    existing_customer = supabase.table("customer") \
        .select("*") \
        .eq("customer_id", customer_id) \
        .execute()

    if existing_customer.data:
        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    # CHECK BOOK

    book = supabase.table("books") \
        .select("*") \
        .eq("book_id", customer.book_id) \
        .execute()

    print(book.data)

    if not book.data:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book_data = book.data[0]

    print("Quantity:", book_data["quantity"])

    if int(book_data["quantity"]) <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book out of stock"
        )

    # REDUCE QUANTITY

    new_quantity = int(book_data["quantity"]) - 1

    supabase.table("books") \
        .update({
            "quantity": new_quantity
        }) \
        .eq("book_id", customer.book_id) \
        .execute()

    # ADD CUSTOMER

    supabase.table("customer").insert({

        "customer_id": customer_id,
        "book_id": customer.book_id,
        "customer_name": customer.customer_name,
        "days_borrowed": customer.days_borrowed,
        "issue_date": str(customer.issue_date),
        "return_date": str(customer.return_date),
        "nameofbook": book_data["nameofbook"]

    }).execute()

    return {
        "message": "Book issued successfully"
    }


# =========================
# UPDATE CUSTOMER
# =========================

@app.put("/customer_update")
def update_customer(
    customer_id: str,
    customer_update: Customer_update
):

    response = supabase.table("customer") \
        .select("*") \
        .eq("customer_id", customer_id) \
        .execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    existing = response.data[0]

    update_data = customer_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        existing[key] = value

    issue_date = datetime.strptime(
        existing["issue_date"],
        "%Y-%m-%d"
    ).date()

    new_return = issue_date + timedelta(
        days=existing["days_borrowed"]
    )

    existing["return_date"] = str(new_return)

    supabase.table("customer") \
        .update({

            "customer_name": existing["customer_name"],
            "days_borrowed": existing["days_borrowed"],
            "return_date": existing["return_date"]

        }) \
        .eq("customer_id", customer_id) \
        .execute()

    return {
        "message": "Customer updated successfully"
    }


# =========================
# RETURN BOOK
# =========================

@app.delete("/return_book")
def return_book(customer_id: str):

    customer = supabase.table("customer") \
        .select("*") \
        .eq("customer_id", customer_id) \
        .execute()

    if not customer.data:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer_data = customer.data[0]

    book_id = customer_data["book_id"]

    # GET BOOK

    book = supabase.table("books") \
        .select("*") \
        .eq("book_id", book_id) \
        .execute()

    book_data = book.data[0]

    # INCREASE QUANTITY

    new_quantity = int(book_data["quantity"]) + 1

    supabase.table("books") \
        .update({
            "quantity": new_quantity
        }) \
        .eq("book_id", book_id) \
        .execute()

    # FINE CALCULATION

    expected_return = datetime.strptime(
        customer_data["return_date"],
        "%Y-%m-%d"
    )

    today = datetime.today()

    fine = 0

    if today > expected_return:

        extra_days = (today - expected_return).days

        fine = extra_days * int(book_data["fineperday"])

    # DELETE CUSTOMER RECORD

    supabase.table("customer") \
        .delete() \
        .eq("customer_id", customer_id) \
        .execute()

    return {

        "message": "Book returned successfully",
        "fine": fine

    }
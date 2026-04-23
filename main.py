from fastapi import FastAPI,HTTPException
import json
from pydantic import computed_field,field_validator,BaseModel,Field
from typing import List,Literal,Optional,Annotated
import json
from fastapi.responses import JSONResponse
from datetime import date,timedelta,datetime

class Books(BaseModel):
    Book_id: Annotated[str, Field(..., description="id of the book")]
    nameofbook: Annotated[str, Field(..., description="name of the book")]
    author: Annotated[str, Field(..., description="name of the author")]
    quantity: Annotated[int, Field(..., description="number of books available",gt=0)]
    fineperday:Annotated[int, Field(..., description="fine per book",gt=0)]

class Books_update(BaseModel):
    nameofbook: Annotated[Optional[str], Field(default=None)]
    author: Annotated[Optional[str], Field(default=None)]
    quantity: Annotated[Optional[int], Field(default=None, gt=0)]
    fineperday:Annotated[Optional[int], Field(default=None,gt=0)]


class Customer(BaseModel):
    Book_id: Annotated[str, Field(..., description="id of the book")]
    customer_name: Annotated[str, Field(..., description="name of the customer")]
    days_borrowed: Annotated[int, Field(..., description="number of days you have to borrow")]
    
    issue_date: date = date.today()

    @computed_field
    @property
    def return_date(self) -> date:
        return self.issue_date + timedelta(days=self.days_borrowed)
    
    
class Customer_update(BaseModel):
    customer_name: Annotated[Optional[str], Field(..., description="name of the customer")]
    days_borrowed: Annotated[Optional[int], Field(..., description="number of days you have to borrow")]
    
    
def read_books():
    with open("books.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('books.json', 'w') as f:
        json.dump(data, f, indent=4)

def read_customer():
    with open("customer.json", "r") as file:
        data = json.load(file)
    return data

def save_customer(data):
    with open('customer.json', 'w') as f:
        json.dump(data, f, indent=4)

def nameofbook_by_id(Book_id:str):
    Books_data=read_books()
    nameofbook=Books_data[Book_id]["nameofbook"]
    return nameofbook


app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI working"}


@app.get("/book_info/{book_id}")
def book_info(book_id: str):
    data = read_books()

    if book_id not in data:
        raise HTTPException(status_code=404,detail="Book not found")
    
    return data[book_id]


@app.post("/create")
def create(Book:Books):
    data = read_books()

    if Book.Book_id in data:
        raise HTTPException(status_code=404,detail="Book not found")
    data[Book.Book_id]=Book.model_dump(exclude="Book_id")
    save_data(data)

    return JSONResponse(
            status_code=200,
            content={"message": "Book added successfully"}
        )


@app.put("/update")
def update_book(book_id:str,book:Books_update):
    data=read_books()
    if book_id not in data:
        return HTTPException(status_code=404,detail="Book does not exists")
    book_data=book.model_dump(exclude_unset=True)

    exisiting_data=data[book_id]

    for key,value in book_data.items():
        exisiting_data[key]=value
    exisiting_data["Book_id"]=book_id
    book_obj=Books(**exisiting_data)
    exisiting_data=book_obj.model_dump(exclude="Book_id")
    data[book_id]=exisiting_data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message":"updated successfully"}
    )


@app.delete("/delete")
def delete_books(book_id:str):
    data=read_books()
    if book_id not in data:
        return HTTPException(status_code=404,detail="Book does not exists")
    del data[book_id]
    save_data(data)
    return JSONResponse(
        status_code=200,
        content={"message":"deleted successfully"}
    )


@app.get("/customer")
def get_customer_data(customer_id:str):
    data=read_customer()
    if customer_id not in data:
        raise HTTPException(status_code=400,detail="Customer not found")
    return data[customer_id]


@app.post("/Customer_create")
def add_customer(customer:Customer,customer_id:str):
    issue_date=customer.issue_date
    customer_data=read_customer()
    Books_data=read_books()
    nameofbook=nameofbook_by_id(customer.Book_id)
    return_date=customer.return_date
    nameofbook=nameofbook_by_id(customer.Book_id)

    if customer_id in customer_data:
        raise HTTPException(status_code=400,detail="customer already exists")
    if customer.Book_id not in Books_data:
        raise HTTPException(status_code=404, detail="Book not found")

    if Books_data[customer.Book_id]["quantity"] <= 0:
        raise HTTPException(status_code=400, detail="Book out of stock")

    Books_data[customer.Book_id]["quantity"]-=1
    save_data(Books_data)
    customer_data[customer_id]=customer.model_dump()
    customer_data[customer_id]["nameofbook"]=str(nameofbook)
    customer_data[customer_id]["issue_date"]=str(issue_date)
    customer_data[customer_id]["return_date"]=str(return_date)
    save_customer(customer_data)
    return JSONResponse(
        status_code=200,
        content={"message":"Customer added successfully"}
    )


@app.put("/customer_update")
def update_customerdetail(customer_update: Customer_update, customer_id: str):
    customer_data = read_customer()

    if customer_id not in customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_data = customer_data[customer_id]

    nameofbook = existing_data.get("nameofbook")
    issue_date = existing_data.get("issue_date")
    update_data = customer_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        existing_data[key] = value

    existing_data.pop("nameofbook", None)
    existing_data.pop("return_date", None)
    existing_data.pop("issue_date", None)

    pyd_object = Customer(**existing_data)
    updated_data = pyd_object.model_dump()

    updated_data["nameofbook"] = nameofbook
    updated_data["issue_date"] = issue_date
    updated_data["return_date"] = str(pyd_object.return_date)
    customer_data[customer_id] = updated_data
    save_customer(customer_data)

    return JSONResponse(
        status_code=200,
        content={"message": "Customer data updated successfully"}
    )

    
@app.delete("/return_book")
@app.delete("/return_book")
def return_book(customer_id: str):
    customer_data = read_customer()
    book_data = read_books()

    if customer_id not in customer_data:
        raise HTTPException(status_code=400, detail="customer not found")

    record = customer_data[customer_id]

    issued_date = record["issue_date"]
    return_date_expected = record["return_date"]
    days_borrowed = record["days_borrowed"]
    book_id = record["Book_id"]

    issue = datetime.strptime(issued_date, "%Y-%m-%d")
    expected = datetime.strptime(return_date_expected, "%Y-%m-%d")
    returned = datetime.today()

    total_days = (returned - issue).days

    book_data[book_id]["quantity"] += 1

    fineperday = book_data[book_id]["fineperday"]

    if returned >= expected:
        extra_days = (returned - expected).days
        total_price =extra_days * fineperday
        fine = extra_days * fineperday
    elif returned<expected:
        return{
            "message":"Thanks for returning in time"
        }
    del customer_data[customer_id]

    save_customer(customer_data)
    save_data(book_data)

    return {
        "message": "Book returned successfully",
        "total_days": total_days,
        "fine": fine,
        "total_price": total_price
    }
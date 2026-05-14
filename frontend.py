import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="centered"
)

# ==========================================
# TITLE
# ==========================================

st.title("📚 Library Management System")

# ==========================================
# SIDEBAR MENU
# ==========================================

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Home",
        "Add Book",
        "View Book",
        "Update Book",
        "Delete Book",
        "Issue Book",
        "View Customer",
        "Update Customer",
        "Return Book"
    ]
)

# ==========================================
# HOME
# ==========================================

if menu == "Home":

    st.header("🏠 Dashboard")

    st.write("""
    ## Features
    - Add Books
    - View Books
    - Update Books
    - Delete Books
    - Issue Books
    - Return Books
    - Fine Calculation
    """)

    st.success("Backend Connected Successfully")


# ==========================================
# ADD BOOK
# ==========================================

elif menu == "Add Book":

    st.header("➕ Add Book")

    book_id = st.text_input("Book ID")
    nameofbook = st.text_input("Book Name")
    author = st.text_input("Author")
    genre = st.text_input("Genre")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    fineperday = st.number_input(
        "Fine Per Day",
        min_value=1,
        step=1
    )

    if st.button("Add Book"):

        payload = {
            "book_id": book_id,
            "nameofbook": nameofbook,
            "author": author,
            "genre": genre,
            "quantity": quantity,
            "fineperday": fineperday
        }

        response = requests.post(
            f"{BASE_URL}/create",
            json=payload
        )

        st.json(response.json())


# ==========================================
# VIEW BOOK
# ==========================================

elif menu == "View Book":

    st.header("📖 View Book")

    book_id = st.text_input("Enter Book ID")

    if st.button("Get Book"):

        response = requests.get(
            f"{BASE_URL}/book_info/{book_id}"
        )

        st.json(response.json())


# ==========================================
# UPDATE BOOK
# ==========================================

elif menu == "Update Book":

    st.header("✏️ Update Book")

    book_id = st.text_input("Book ID")

    nameofbook = st.text_input("New Book Name")
    author = st.text_input("New Author")
    genre = st.text_input("New Genre")

    quantity = st.number_input(
        "New Quantity",
        min_value=1,
        step=1
    )

    fineperday = st.number_input(
        "New Fine Per Day",
        min_value=1,
        step=1
    )

    if st.button("Update Book"):

        payload = {
            "nameofbook": nameofbook,
            "author": author,
            "genre": genre,
            "quantity": quantity,
            "fineperday": fineperday
        }

        response = requests.put(
            f"{BASE_URL}/update?book_id={book_id}",
            json=payload
        )

        st.json(response.json())


# ==========================================
# DELETE BOOK
# ==========================================

elif menu == "Delete Book":

    st.header("🗑 Delete Book")

    book_id = st.text_input("Book ID")

    if st.button("Delete Book"):

        response = requests.delete(
            f"{BASE_URL}/delete?book_id={book_id}"
        )

        st.json(response.json())


# ==========================================
# ISSUE BOOK
# ==========================================

elif menu == "Issue Book":

    st.header("👤 Issue Book")

    customer_id = st.text_input("Customer ID")

    customer_name = st.text_input("Customer Name")

    book_id = st.text_input("Book ID")

    days = st.number_input(
        "Days Borrowed",
        min_value=1,
        step=1
    )

    if st.button("Issue Book"):

        payload = {
            "book_id": book_id,
            "customer_name": customer_name,
            "days_borrowed": days
        }

        response = requests.post(
            f"{BASE_URL}/Customer_create?customer_id={customer_id}",
            json=payload
        )

        st.json(response.json())


# ==========================================
# VIEW CUSTOMER
# ==========================================

elif menu == "View Customer":

    st.header("🧑 View Customer")

    customer_id = st.text_input("Customer ID")

    if st.button("Get Customer"):

        response = requests.get(
            f"{BASE_URL}/customer?customer_id={customer_id}"
        )

        st.json(response.json())


# ==========================================
# UPDATE CUSTOMER
# ==========================================

elif menu == "Update Customer":

    st.header("📝 Update Customer")

    customer_id = st.text_input("Customer ID")

    customer_name = st.text_input("New Customer Name")

    days_borrowed = st.number_input(
        "New Days Borrowed",
        min_value=1,
        step=1
    )

    if st.button("Update Customer"):

        payload = {
            "customer_name": customer_name,
            "days_borrowed": days_borrowed
        }

        response = requests.put(
            f"{BASE_URL}/customer_update?customer_id={customer_id}",
            json=payload
        )

        st.json(response.json())


# ==========================================
# RETURN BOOK
# ==========================================

elif menu == "Return Book":

    st.header("📦 Return Book")

    customer_id = st.text_input("Customer ID")

    if st.button("Return Book"):

        response = requests.delete(
            f"{BASE_URL}/return_book?customer_id={customer_id}"
        )

        st.json(response.json())
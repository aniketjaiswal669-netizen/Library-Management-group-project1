import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Library Management", layout="wide")

st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Choose Option", [
    "Add Book",
    "View Book",
    "Update Book",
    "Delete Book",
    "Add Customer",
    "View Customer",
    "Return Book"
])

# ------------------ ADD BOOK ------------------
if menu == "Add Book":
    st.header("Add New Book")

    book_id = st.text_input("Book ID")
    name = st.text_input("Book Name")
    author = st.text_input("Author")
    quantity = st.number_input("Quantity", min_value=1)
    fine = st.number_input("Fine per day", min_value=1)

    if st.button("Add Book"):
        data = {
            "Book_id": book_id,
            "nameofbook": name,
            "author": author,
            "quantity": quantity,
            "fineperday": fine
        }

        res = requests.post(f"{BASE_URL}/create", json=data)

        if res.status_code == 200:
            st.success("Book Added Successfully")
        else:
            st.error(res.text)

# ------------------ VIEW BOOK ------------------
elif menu == "View Book":
    st.header("View Book Info")

    book_id = st.text_input("Enter Book ID")

    if st.button("Fetch Book"):
        res = requests.get(f"{BASE_URL}/book_info/{book_id}")

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error(res.text)

# ------------------ UPDATE BOOK ------------------
elif menu == "Update Book":
    st.header("Update Book")

    book_id = st.text_input("Book ID")
    name = st.text_input("New Name")
    author = st.text_input("New Author")
    quantity = st.number_input("New Quantity", min_value=0)
    fine = st.number_input("New Fine", min_value=0)

    if st.button("Update"):
        data = {}

        if name:
            data["nameofbook"] = name
        if author:
            data["author"] = author
        if quantity:
            data["quantity"] = quantity
        if fine:
            data["fineperday"] = fine

        res = requests.put(f"{BASE_URL}/update?book_id={book_id}", json=data)

        if res.status_code == 200:
            st.success("Updated Successfully")
        else:
            st.error(res.text)

# ------------------ DELETE BOOK ------------------
elif menu == "Delete Book":
    st.header("Delete Book")

    book_id = st.text_input("Book ID")

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/delete?book_id={book_id}")

        if res.status_code == 200:
            st.success("Deleted Successfully")
        else:
            st.error(res.text)

# ------------------ ADD CUSTOMER ------------------
elif menu == "Add Customer":
    st.header("Issue Book to Customer")

    customer_id = st.text_input("Customer ID")
    book_id = st.text_input("Book ID")
    name = st.text_input("Customer Name")
    days = st.number_input("Days Borrowed", min_value=1)

    if st.button("Add Customer"):
        data = {
            "Book_id": book_id,
            "customer_name": name,
            "days_borrowed": days
        }

        res = requests.post(
            f"{BASE_URL}/Customer_create?customer_id={customer_id}",
            json=data
        )

        if res.status_code == 200:
            st.success("Customer Added")
        else:
            st.error(res.text)

# ------------------ VIEW CUSTOMER ------------------
elif menu == "View Customer":
    st.header("View Customer")

    customer_id = st.text_input("Customer ID")

    if st.button("Fetch Customer"):
        res = requests.get(f"{BASE_URL}/customer?customer_id={customer_id}")

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error(res.text)

# ------------------ RETURN BOOK ------------------
elif menu == "Return Book":
    st.header("Return Book")

    customer_id = st.text_input("Customer ID")

    if st.button("Return"):
        res = requests.delete(f"{BASE_URL}/return_book?customer_id={customer_id}")

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error(res.text)
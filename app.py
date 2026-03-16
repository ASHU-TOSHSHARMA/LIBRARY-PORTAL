
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("library.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
username TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
author TEXT,
quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
book TEXT,
date TEXT
)
""")

conn.commit()

st.set_page_config(page_title="Smart Library",layout="wide")

st.markdown("<h1 style='text-align:center;'>📚 Smart Library Portal</h1>",unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu",["Home","Register","Login","Dashboard"])

# HOME
if menu=="Home":
    st.write("Welcome to Smart Library Management System")

# REGISTER
elif menu=="Register":
    name = st.text_input("Name")
    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Register"):
        cursor.execute("INSERT INTO users(name,username,password) VALUES(?,?,?)",(name,username,password))
        conn.commit()
        st.success("Registration Successful")

# LOGIN
elif menu=="Login":
    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        data = cursor.fetchone()

        if data:
            st.session_state["user"]=username
            st.success("Login Successful")
        else:
            st.error("Invalid Login")

# DASHBOARD
elif menu=="Dashboard":

    if "user" not in st.session_state:
        st.warning("Please Login First")

    else:

        st.success("Welcome "+st.session_state["user"])

        option = st.selectbox("Options",["Add Book","View Books","Issue Book","Return Book","Graph"])

        if option=="Add Book":
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            qty = st.number_input("Quantity")

            if st.button("Add"):
                cursor.execute("INSERT INTO books(title,author,quantity) VALUES(?,?,?)",(title,author,qty))
                conn.commit()
                st.success("Book Added")

        if option=="View Books":
            cursor.execute("SELECT * FROM books")
            data = cursor.fetchall()
            df = pd.DataFrame(data,columns=["ID","Title","Author","Qty"])
            st.dataframe(df)

        if option=="Issue Book":
            book = st.text_input("Book Name")

            if st.button("Issue"):
                cursor.execute("INSERT INTO issued(username,book,date) VALUES(?,?,date('now'))",(st.session_state["user"],book))
                conn.commit()
                st.success("Book Issued")

        if option=="Return Book":
            book = st.text_input("Book Name")

            if st.button("Return"):
                cursor.execute("DELETE FROM issued WHERE username=? AND book=?",(st.session_state["user"],book))
                conn.commit()
                st.success("Returned")

        if option=="Graph":
            cursor.execute("SELECT title,quantity FROM books")
            data = cursor.fetchall()

            if data:
                df = pd.DataFrame(data,columns=["Book","Qty"])
                fig,ax = plt.subplots()
                ax.bar(df["Book"],df["Qty"])
                st.pyplot(fig)
            else:
                st.info("No books data available for graph.")

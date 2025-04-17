# register.py
import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_register():
    st.title("Doctor Registration")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_username and new_password and confirm_password:
            if new_password == confirm_password:
                conn = sqlite3.connect("clinic_visitors.db")
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO doctors (username, password) VALUES (?, ?)",
                              (new_username, hash_password(new_password)))
                    conn.commit()
                    conn.close()
                    st.success("Registration successful! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different one.")
            else:
                st.warning("Passwords do not match.")
        else:
            st.warning("Please fill out all fields.")

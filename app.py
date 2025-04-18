import streamlit as st
from login import show_login
from database import initialize_database

def main():
    initialize_database()
    show_login()

if __name__ == "__main__":
    main()

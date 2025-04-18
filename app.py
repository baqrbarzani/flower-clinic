import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration from YAML
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Login form
name, authentication_status, username = authenticator.login(
    fields={
        'Form name': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Login': 'Login'
    },
    location='sidebar'
)

# Conditional app flow
if authentication_status:
    st.sidebar.success(f"Welcome, {name}!")
    authenticator.logout('Logout', location='sidebar')
    st.title("Dashboard")
    st.write("This is the main dashboard after logging in.")
elif authentication_status is False:
    st.sidebar.error("Invalid username or password.")
elif authentication_status is None:
    st.sidebar.info("Please enter your login credentials.")

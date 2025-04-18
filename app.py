import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load the YAML config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# 🔐 Login (updated return type is a dict)
auth_result = authenticator.login(
    location='sidebar',
    fields={
        'Form name': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Login': 'Login'
    }
)

if auth_result["authenticated"]:
    st.sidebar.success(f"Welcome {auth_result['name']} 👋")
    authenticator.logout('Logout', location='sidebar')
    st.title("Dashboard")
    st.write("Here’s your Flower Clinic dashboard.")
elif auth_result["authenticated"] is False:
    st.sidebar.error("Invalid username or password.")
else:
    st.sidebar.info("Please enter your login details.")

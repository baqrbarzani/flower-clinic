import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load YAML config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Run login
auth_result = authenticator.login(
    location='sidebar',
    fields={
        'Form name': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Login': 'Login'
    }
)

# 🔐 Safety check: make sure login ran properly
if auth_result and "authenticated" in auth_result:
    if auth_result["authenticated"]:
        st.sidebar.success(f"Welcome {auth_result['name']} 👋")
        authenticator.logout('Logout', location='sidebar')
        st.title("Dashboard")
        st.write("Here’s your Flower Clinic dashboard.")
    else:
        st.sidebar.error("Invalid username or password.")
else:
    st.sidebar.info("Please enter your login details.")

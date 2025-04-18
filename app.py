import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render login form in the sidebar
name, authentication_status, username = authenticator.login(
    location='sidebar',
    fields={
        'Form name': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Login': 'Login'
    }
)

# Check authentication status
if authentication_status:
    st.sidebar.success(f"Welcome *{name}*")
    authenticator.logout('Logout', location='sidebar')
    st.title('Main Application')
    st.write('This is the main content of the app.')
elif authentication_status is False:
    st.sidebar.error('Username/password is incorrect')
elif authentication_status is None:
    st.sidebar.warning('Please enter your username and password')

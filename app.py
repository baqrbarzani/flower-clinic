import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator without 'preauthorized'
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render login form in the sidebar
authenticator.login('Login', location='sidebar')

# Check authentication status
if st.session_state["authentication_status"]:
    st.sidebar.success(f"Welcome *{st.session_state['name']}*")
    authenticator.logout('Logout', location='sidebar')
    st.title('Main Application')
    st.write('This is the main content of the app.')
elif st.session_state["authentication_status"] is False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.sidebar.warning('Please enter your username and password')

# Registration form
try:
    if authenticator.register_user('Register', preauthorization=config.get('preauthorized', {}).get('emails', [])):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

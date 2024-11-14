import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase
import re
from datetime import datetime

# Initialize Firebase Admin SDK
# Make sure to replace the path with your firebase-credentials.json file
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your/firebase-credentials.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
    'apiKey': "AIzaSyDsrIcuUlnVM-CYNj_lLlSrfiX_bqOx6so",
    'authDomain': "paygap-project.firebaseapp.com",
    'projectId': "paygap-project",
    'databaseURL': "https://paygap-project-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "paygap-project.firebasestorage.app",
    'messagingSenderId': "288758264928",
    'appId': "1:288758264928:web:94f7e0a06610a91a113f05",
    'measurementId': "G-M6DDG0QVE6"
}


# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth_pb = firebase.auth()
db = firestore.client()

# Initialize session state variables
if 'user' not in st.session_state:
    st.session_state.user = None
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None

# Function to validate email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Function to validate phone number
def is_valid_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def main():
    st.title("Authentication System")
    
    # Sidebar menu
    menu = ["Login", "Sign Up", "Reset Password"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        st.subheader("Login")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            try:
                user = auth_pb.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.session_state.authentication_status = True
                st.success("Logged in successfully!")
                
                # Fetch user data from Firestore
                user_data = db.collection('users').document(user['localId']).get().to_dict()
                st.write(f"Welcome {user_data['name']} from {user_data['company_name']}!")
                
            except Exception as e:
                st.error("Invalid credentials or error occurred.")
                st.session_state.authentication_status = False
    
    elif choice == "Sign Up":
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            company_name = st.text_input("Company Name")
            country = st.text_input("Country")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type='password')
            confirm_password = st.text_input("Confirm Password", type='password')
            
            submit_button = st.form_submit_button("Sign Up")
            
            if submit_button:
                if not all([name, email, company_name, country, phone, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address")
                elif not is_valid_phone(phone):
                    st.error("Please enter a valid phone number")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    try:
                        # Create user in Firebase Authentication
                        user = auth.create_user(
                            email=email,
                            password=password
                        )
                        
                        # Store additional user data in Firestore
                        user_data = {
                            'name': name,
                            'email': email,
                            'company_name': company_name,
                            'country': country,
                            'phone': phone,
                            'created_at': datetime.now()
                        }
                        
                        db.collection('users').document(user.uid).set(user_data)
                        
                        st.success("Account created successfully! Please login.")
                        
                    except Exception as e:
                        st.error(f"Error occurred: {str(e)}")
    
    elif choice == "Reset Password":
        st.subheader("Reset Password")
        
        email = st.text_input("Email")
        if st.button("Reset Password"):
            try:
                auth_pb.send_password_reset_email(email)
                st.success("Password reset link sent to your email!")
            except Exception as e:
                st.error("Error occurred while sending reset link.")

if __name__ == '__main__':
    main()

# Created/Modified files during execution:
# Note: This script requires:
# - firebase-credentials.json (Firebase Admin SDK credentials)
# - requirements.txt (containing: streamlit, firebase-admin, pyrebase4)
import streamlit as st
from pipeline2.page1 import display_page
from pipeline2.page2 import selection_page
from pipeline2.page3 import data_upload
from pipeline2.page4 import customization
from pipeline2.page5 import pay_ranges_function


def login_function(username, password):
    return username == "admin" and password == "admin"


def main():
    st.title("Authentication Page")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if login_function(username, password):
            st.session_state.page = "page_1"
        else:
            st.error("Invalid username or password.")


# Initialize session state for page control
if "page" not in st.session_state:
    st.session_state.page = "main"

# Display the correct page
if st.session_state.page == "main":
    main()
elif st.session_state.page == "page_1":
    display_page()
elif st.session_state.page == "page_2":
    selection_page()
elif st.session_state.page == "page_3":
    data_upload()
elif st.session_state.page == "page_4":
    customization()
elif st.session_state.page == "page_5":
    pay_ranges_function()



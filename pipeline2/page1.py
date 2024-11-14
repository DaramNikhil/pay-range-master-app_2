import streamlit as st


def display_page():
    st.header("Pay Range Builder")
    st.write("Helping HR professionals create fair pay ranges with ease")

    st.markdown(""" 
        - **Data-Driven**: No guesswork and requires no effort for ensuring fit.
        - **Multiple Approaches**: Choose an approach that best fits your organization.
        - **Accurate Budgeting**: Identify outliers and align budgeting with your pay policy.
        """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", help="Go back to Login Page"):
            st.session_state.page = 'main'
    with col2:
        if st.button("Next", help="Proceed to the next page"):
            st.session_state.page = "page_2"
    
    
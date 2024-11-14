import streamlit as st


def selection_page():
    st.subheader("Whats Your Approch!")
    selected_option = st.radio(
        "I will use:",
        ("Market rates of jobs to create pay ranges", 
         "Pay data of existing employees to build pay ranges", 
         "A combination strategy as it's well aligned with my organization"),
         horizontal=False
    )
    st.session_state.selected_approach = selected_option
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "page_1"
        
    with col2:
        if st.button("Next"):
            if selected_option == "Market rates of jobs to create pay ranges":
                st.write("You got a competitive edge!")
                st.session_state.page = "page_3"
            elif selected_option == "Pay data of existing employees to build pay ranges":
                st.write("Yes, Fairness matters!")
                st.session_state.page = "page_3"
            elif selected_option == "A combination strategy as it's well aligned with my organization":
                st.write("It's a win-win!")
                st.session_state.page = "page_3"

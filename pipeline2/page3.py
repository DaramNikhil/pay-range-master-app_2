import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.getcwd())
from calculations import market_pay, market_pay_based, combination_strategy
from pipeline2 import page4

def data_upload():
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])
    df = None
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        st.session_state.row_data = df
        st.write(f"total records {df.shape[0]}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("First 5 Rows")
            st.dataframe(df.head(), hide_index=True)
        with col2:
            st.subheader("Last 5 Rows")
            st.dataframe(df.head(), hide_index=True)



    left, right = st.columns(2)
    with left:
        if st.button("Back"):
            st.session_state.page = "page_2"

    with right:
        if df is not None and st.button("Next"):
            if st.session_state.selected_approach == "Market rates of jobs to create pay ranges":
                preprocess_df, plot_data = market_pay.main(df=df)
                st.session_state.custom_df = preprocess_df
                st.session_state.plt_data = plot_data
                st.session_state.page = "page_4"

            elif st.session_state.selected_approach == "Pay data of existing employees to build pay ranges":
                preprocess_df = market_pay_based.analyze_salary_distribution(df=df)
                st.session_state.custom_df = preprocess_df
                st.session_state.page = "page_4"

            elif st.session_state.selected_approach == "A combination strategy as it's well aligned with my organization":
                preprocess_df = combination_strategy.calculate(df=df)
                st.session_state.custom_df = preprocess_df
                st.session_state.page = "page_4"



import streamlit as st
import pandas as pd
import numpy as np
import utils
from calculations import market_pay

def pay_ranges_function():
    st.header("Calibrating Your Pay Ranges")
    st.write("The pay ranges are based on your job title, department, and location.")
    df = st.session_state.custom_df
    if st.session_state.selected_approach == "Market rates of jobs to create pay ranges":
        plot_data = st.session_state.plt_data
        customize_options = st.radio("Do you want to age your pay ranges?", ("Yes, that's a good idea", "No, I'm fine"))
        if customize_options == "Yes, that's a good idea":
            col1, col2, col3 = st.columns([1, 1, 1])
            age_percent = col1.text_input("Monthly aging percent (%)")
            age_months = col2.text_input("Months to age")
            age_button = col3.button("Apply Aging")
            if age_button:
                try:
                    age_percent = float(age_percent)
                    age_months = float(age_months)   
                    df["Range Mid"] = pd.to_numeric(df["Range Mid"], errors="coerce")  
                    df["New Range Mid"] = df["Range Mid"] * (1 + (age_percent / 100) * age_months)
                    st.session_state["aged_ranges"] = df.copy()
                    st.write(f"Pay ranges aged at {int(age_percent)}% for {int(age_months)} months")
                    st.dataframe(st.session_state["aged_ranges"], hide_index=True)
                except ValueError:
                    st.error("Please enter valid numbers for percentage and months.")
        else:
            # st.button("Reset Ageing", key="reset_ageing_button", disabled=True if "aged_ranges" not in st.session_state else False)
            st.dataframe(df, hide_index=True)

    elif st.session_state.selected_approach == "Pay data of existing employees to build pay ranges":
        st.dataframe(df, hide_index=True)

    elif st.session_state.selected_approach == "A combination strategy as it's well aligned with my organization":
        st.dataframe(df, hide_index=True)

    

    left, right = st.columns(2)
    with right:
        if st.button("Click Here to See Visualisations"):
            if "selected_approach" in st.session_state:
                if st.session_state.selected_approach == "Market rates of jobs to create pay ranges":
                    utils.create_salary_structure_bar_chart(df_results=plot_data)
                elif st.session_state.selected_approach == "Pay data of existing employees to build pay ranges":
                    utils.create_salary_structure_bar_chart_2(df_results_2=df)
                elif st.session_state.selected_approach == "A combination strategy as it's well aligned with my organization":
                    st.error("Currently There is no Visualisation available")
    with left:
        if st.button("Back"):
            st.session_state.page = "page_4"




    
    

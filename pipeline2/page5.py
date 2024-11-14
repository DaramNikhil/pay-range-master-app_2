import streamlit as st
import pandas as pd
import numpy as np
import utils

def pay_ranges_function():
    st.header("Calibrating Your Pay Ranges")
    st.write("The pay ranges are based on your job title, department, and location.")
    main_df = st.session_state.custom_df

    # Option to age pay ranges
    customize_options = st.radio("Do you want to age your pay ranges?", ("Yes, that's a good idea", "No, I'm fine"))

    if customize_options == "Yes, that's a good idea":
        col1, col2, col3 = st.columns([1, 1, 1])
        age_percent = col1.text_input("Monthly aging percent (%)")
        age_months = col2.text_input("Months to age")
        age_button = col3.button("Apply Aging")

        if age_button:
            try:
                # Convert inputs to numeric values
                age_percent = float(age_percent)
                age_months = int(age_months)

                # Convert 'Range Mid' column to numeric, handling errors
                main_df["Range Mid"] = pd.to_numeric(main_df["Range Mid"], errors="coerce")

                
                if main_df["Range Mid"].isnull().any():
                    st.warning("Some 'Range Mid' values were non-numeric and have been set to 0.")
                    main_df["Range Mid"].fillna(0, inplace=True)

                
                main_df["New Range Mid"] = main_df["Range Mid"] * (1 + (age_percent / 100) * age_months)

                
                st.session_state["aged_ranges"] = main_df.copy()
                st.write(f"Pay ranges aged at {age_percent}% for {age_months} months.")
                st.dataframe(st.session_state["aged_ranges"], hide_index=True)
                


            except ValueError:
                st.error("Please enter valid numbers for percentage and months.")

    else:
        st.dataframe(main_df)

    
    if st.button("Click Here to See Visualization"):
        if "selected_approach" in st.session_state:
            if st.session_state.selected_approach == "Market rates of jobs to create pay ranges":
                utils.create_salary_structure_bar_chart(df_results=st.session_state["aged_ranges"] if "aged_ranges" in st.session_state else main_df)
            elif st.session_state.selected_approach == "Pay data of existing employees to build pay ranges":
                utils.create_salary_structure_bar_chart_2(df=st.session_state["aged_ranges"] if "aged_ranges" in st.session_state else main_df)

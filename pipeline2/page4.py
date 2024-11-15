import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os




def customization():
    st.header("Data Customization Page")
    st.write("Welcome to the data customization page.")
    if "custom_df" in st.session_state:
        df = st.session_state.custom_df
        st.data_editor(df, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.page = "page_3"

        with col2:
            if st.button("Next"):
                st.session_state.page = "page_5"


    else:
        st.write("No data available to customize. Please go back to the previous page.")

import streamlit as st

def set_centered_layout():
    st.set_page_config(layout="centered")
    st.markdown("""
        <style>
            .block-container {
                max-width: 800px;
                margin: auto;
            }
        </style>
    """, unsafe_allow_html=True)
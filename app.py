import streamlit as st
import pandas as pd
import os
from typing import Optional

from data_loader import DataLoader
from schema_extractor import SchemaExtractor
from sql_validator import SQLValidator
from sql_agent import SQLAgent
from db_executor import DBExecutor

st.set_page_config(
    page_title="SQL Agent - Natural Language to SQL",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()    
    if 'schema' not in st.session_state:
        st.session_state.schema = {}    
    if 'loaded_files' not in st.session_state:
        st.session_state.loaded_files = []    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

def load_uploaded_file(uploaded_file) -> tuple:
    try:
        table_name, success, message = st.session_state.data_loader.load_from_uploaded_file(uploaded_file)        
        if success:
            conn = st.session_state.data_loader.get_connection()
            extractor = SchemaExtractor(conn)
            st.session_state.schema = extractor.get_schema()
            if uploaded_file.name not in st.session_state.loaded_files:
                st.session_state.loaded_files.append(uploaded_file.name)        
        return success, message    
    except Exception as e:
        return False, f"Error loading file: {str(e)}"
    

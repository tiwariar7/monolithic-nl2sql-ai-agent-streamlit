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
    
def process_natural_language_query(question: str, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile") -> dict:
    try:
        if not st.session_state.schema:
            return {
                'sql': '',
                'result': pd.DataFrame(),
                'success': False,
                'message': 'No database loaded. Please upload a dataset first.'
            }        
        conn = st.session_state.data_loader.get_connection()
        extractor = SchemaExtractor(conn)
        validator = SQLValidator()
        executor = DBExecutor(conn)
        schema_text = extractor.format_schema_for_prompt(st.session_state.schema)
        if api_key:
            try:
                agent = SQLAgent(api_key=api_key, model=model)
                st.info(f"Using Groq API with {model}")
            except Exception as e:
                return {
                    'sql': '',
                    'result': pd.DataFrame(),
                    'success': False,
                    'message': f'Groq API Error: {str(e)}'
                }
        else:
            st.error("Groq API key required. Please provide your API key in the sidebar.")
            return {
                'sql': '',
                'result': pd.DataFrame(),
                'success': False,
                'message': 'Groq API key required'
            }
        with st.spinner("Generating SQL query..."):
            sql = agent.generate_sql(question, schema_text)        
        if sql.startswith("ERROR:"):
            return {
                'sql': sql,
                'result': pd.DataFrame(),
                'success': False,
                'message': sql
            }
        is_valid, error_msg = validator.validate(sql)
        if not is_valid:
            return {
                'sql': sql,
                'result': pd.DataFrame(),
                'success': False,
                'message': f'SQL Validation Failed: {error_msg}'
            }
        sql = validator.sanitize_sql(sql)
        with st.spinner("Executing query..."):
            success, df, exec_message = executor.execute_query(sql)        
        return {
            'sql': sql,
            'result': df,
            'success': success,
            'message': exec_message if success else exec_message
        }    
    except Exception as e:
        return {
            'sql': '',
            'result': pd.DataFrame(),
            'success': False,
            'message': f'Unexpected error: {str(e)}'
        }

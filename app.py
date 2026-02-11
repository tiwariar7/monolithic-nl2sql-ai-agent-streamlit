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

def main():
    init_session_state()
    st.markdown('<div class="main-header">SQL Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions in natural language, get SQL queries and results automatically</div>', unsafe_allow_html=True)
    with st.sidebar:
        st.header("Configuration")        
        api_key = st.text_input(
            "Groq API Key ",
            type="password",
            help="REQUIRED: Get your free API key from https://console.groq.com/keys",
            placeholder="gsk_..."
        )        
        if api_key:
            model = st.selectbox(
                "Model",
                ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
                index=0,
                help="Select the Groq model to use"
            )
        else:
            st.warning("Please provide Groq API key to use AI-powered SQL generation")        
        st.divider()        
        st.header("Upload Datasets")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['csv', 'xlsx', 'xls', 'db'],
            help="Upload CSV, Excel, or SQLite database files",
            accept_multiple_files=True
        )        
        if uploaded_files:
            if st.button("Load All Files", use_container_width=True):
                success_count = 0
                fail_count = 0                
                for uploaded_file in uploaded_files:
                    with st.spinner(f"Loading {uploaded_file.name}..."):
                        success, message = load_uploaded_file(uploaded_file)
                        if success:
                            st.success(f"{uploaded_file.name}: {message}")
                            success_count += 1
                        else:
                            st.error(f"{uploaded_file.name}: {message}")
                            fail_count += 1                
                if success_count > 0:
                    st.success(f"Loaded {success_count} file(s) successfully!")
                if fail_count > 0:
                    st.warning(f"Failed to load {fail_count} file(s)")
        st.divider()
        if st.session_state.loaded_files:
            st.header("Loaded Files")            
            # Get table information
            conn = st.session_state.data_loader.get_connection()
            extractor = SchemaExtractor(conn)            
            for idx, file in enumerate(st.session_state.loaded_files, 1):
                # Try to get corresponding table info
                tables = st.session_state.data_loader.get_loaded_tables()
                if idx <= len(tables):
                    table_name = tables[idx - 1]
                    row_count = extractor.get_table_row_count(table_name)
                    st.text(f"{idx}. {file} → {table_name}")
                    if row_count is not None:
                        st.caption(f"   {row_count} rows")
                else:
                    st.text(f"{idx}. {file}")        
        st.divider()
        if st.button("Clear All Data", use_container_width=True):
            st.session_state.data_loader.close()
            st.session_state.data_loader = DataLoader()
            st.session_state.schema = {}
            st.session_state.loaded_files = []
            st.session_state.query_history = []
            st.success("All data cleared!")
            st.rerun()
    col1, col2 = st.columns([1, 1])    
    with col1:
        st.header("Database Schema")        
        if st.session_state.schema:
            conn = st.session_state.data_loader.get_connection()
            extractor = SchemaExtractor(conn)
            schema_display = extractor.format_schema_for_display(st.session_state.schema)
            st.markdown(schema_display)            
            table_count = len(st.session_state.schema)
            if table_count > 1:
                st.info(f"You have {table_count} tables loaded. You can query across multiple tables using JOIN.")
        else:
            st.info("Upload dataset(s) to get started")
        question = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Enter Your Question...",
            help="Ask a question in natural language about your data"
        )        
        col_a, col_b = st.columns([3, 1])
        with col_a:
            execute_query = st.button("Generate & Run Query", use_container_width=True, type="primary")
        with col_b:
            if st.button("History", use_container_width=True):
                st.session_state.show_history = not st.session_state.get('show_history', False)    
    if execute_query:
        if not question.strip():
            st.warning("Please enter a question")
        elif not st.session_state.schema:
            st.error("Please upload a dataset first")
        else:
            selected_model = model if api_key and 'model' in locals() else "llama-3.3-70b-versatile"
            result = process_natural_language_query(
                question, 
                api_key=api_key if api_key else None,
                model=selected_model
            )            
            st.session_state.query_history.append({
                'question': question,
                'sql': result['sql'],
                'success': result['success']
            })            
            st.divider()
            st.header("Results")
            st.subheader("Generated SQL Query")
            st.code(result['sql'], language='sql')
            st.subheader("Query Result")            
            if result['success']:
                st.success(result['message'])                
                if not result['result'].empty:
                    st.dataframe(result['result'], use_container_width=True)                    
                    csv = result['result'].to_csv(index=False)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No rows returned by the query")
            else:
                st.error(result['message'])
    if st.session_state.get('show_history', False) and st.session_state.query_history:
        st.divider()
        st.header("Query History")
        
        for idx, entry in enumerate(reversed(st.session_state.query_history[-10:]), 1):
            with st.expander(f"Query {idx}: {entry['question'][:50]}..."):
                st.markdown(f"**Question:** {entry['question']}")
                st.code(entry['sql'], language='sql')
                status = "Success" if entry['success'] else "Failed"
                st.markdown(f"**Status:** {status}")
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with Streamlit| AI by Groq </p>
    </div>
    """, unsafe_allow_html=True)

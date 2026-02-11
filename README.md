# monolithic-nl2sql-ai-agent-streamlit
A monolithic, production-oriented NL2SQL AI Agent that translates natural language questions into accurate SQL queries using dynamic schema reasoning, validates and executes queries securely, and provides real-time results through a Streamlit interface.

## Features

- **AI-Powered SQL Generation** - Convert natural language questions to SQL automatically using Groq API
- **Multiple Data Format Support** - Upload CSV, Excel (.xlsx/.xls), or SQLite database files
- **SQL Validation** - Automatic validation and sanitization of generated SQL queries
- **Schema Management** - Automatic schema extraction and display from uploaded data
- **Query History** - Keep track of recent queries and results
- **Interactive UI** - Clean, intuitive Streamlit interface for easy interaction
- **Data Export** - Download query results as CSV files

## Prerequisites

- Python 3.8 or higher
- Groq API key (get free key at https://console.groq.com/keys)

## Installation

1. **Clone or download the repository**
   ```bash
   gitclone https://github.com/tiwariar7/monolithic-nl2sql-ai-agent-streamlit.git
   cd "monolithic-nl2sql-ai-agent-streamlit"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Alternatively, install manually**
   ```bash
   pip install streamlit pandas sqlalchemy groq
   ```

## Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **In the sidebar:**
   - Enter your Groq API key
   - Select your preferred LLaMA model (llama-3.3-70b-versatile or llama-3.1-8b-instant)
   - Upload one or more CSV/Excel/SQLite files

3. **Ask questions:**
   - Type your natural language question in the text area
   - Click "Generate & Run Query"
   - View the generated SQL, results, and download data if needed

4. **View history:**
   - Click the "History" button to see previous queries
   - Each history entry shows the question, generated SQL, and success status

## File Structure

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application and UI |
| `sql_agent.py` | Core SQL generation logic using Groq API |
| `data_loader.py` | Handles file upload and database operations |
| `schema_extractor.py` | Extracts database schema information |
| `sql_validator.py` | Validates and sanitizes SQL queries |
| `db_executor.py` | Executes SQL queries and returns results |
| `sql_agent_helper.py` | Helper functions for SQL generation |
| `requirements.txt` | Python dependencies |
| `data/` | Sample data files for testing |

## Sample Data

The `data/` directory includes sample CSV files:
- `customers.csv` - Customer information
- `orders.csv` - Order records
- `sample_employees.csv` - Employee data

## API Configuration

### Groq API Models

Currently supported models:
- `llama-3.3-70b-versatile` - Larger, more capable model (recommended)
- `llama-3.1-8b-instant` - Faster, lighter weight model

Get your API key at: https://console.groq.com/keys

## How It Works

1. Upload your data (CSV, Excel, or SQLite)
2. The app extracts the database schema automatically
3. Ask a natural language question
4. SQL Agent generates an appropriate SQL query using Groq API
5. The query is validated for security and correctness
6. The query executes against your data
7. Results are displayed and can be exported


## Security

- SQL queries are automatically validated before execution
- Dangerous operations are sanitized
- User inputs are parameterized to prevent SQL injection
- Database operations are isolated and temporary

## Troubleshooting

**"No database loaded" error**
- Make sure you've uploaded a file and clicked "Load All Files"

**"Groq API Error"**
- Verify your API key is correct
- Check your Groq account quota and usage limits

**Query fails to execute**
- Check the SQL validation error message
- Ensure your question matches the loaded data structure
- Review the generated SQL for correctness

## Requirements

See `requirements.txt` for all dependencies:
- streamlit
- pandas
- sqlalchemy
- groq

## License

This project is provided as-is for educational and practical use.

## Support

For issues or feature requests, please check the application logs and verify:
1. Groq API key is valid
2. Data files are properly formatted
3. Questions are clear and specific

---

**Built with Streamlit | AI by Groq**

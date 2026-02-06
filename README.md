# 🤖 Text-to-SQL Pipeline

An AI-powered pipeline that converts natural language questions into SQL queries using LangChain, Google Gemini 2.0 Flash, and LangGraph.

## 📋 Overview

This project provides multiple interfaces to query your database in plain English:
- **Streamlit Web UI**: Interactive web dashboard
- **CLI**: Command-line interface for quick queries
- **Python API**: Import and use programmatically
- **Jupyter Notebook**: Experimental/educational approach

## 🏗️ Architecture

```
┌─────────────────────┐
│  User Query (NLP)   │
└──────────┬──────────┘
           │
    ┌──────▼───────┐
    │   LLM Agent  │ (Gemini 2.0 Flash)
    │  (LangGraph) │
    └──────┬───────┘
           │
    ┌──────▼──────────────┐
    │  Tool Execution     │
    │  • ListTables       │
    │  • DescribeTable    │
    │  • ExecuteQuery     │
    │  • QueryChecker     │
    └──────┬──────────────┘
           │
    ┌──────▼──────────┐
    │  MySQL Database  │
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │  Results        │
    └─────────────────┘
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone/navigate to project directory
cd c:\Users\lenovo\Desktop\Projects\Text-To-SQL

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Settings

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your credentials
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=vaibhav
# DB_NAME=regional_sales_data
# GOOGLE_API_KEY=your_api_key
```

### 3. Run the Application

#### Option A: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser.

#### Option B: CLI - Interactive Mode
```bash
python cli.py --interactive
```

#### Option C: CLI - Single Query
```bash
python cli.py "How many products are in the database?"
python cli.py --verbose "List top 5 customers by sales"
python cli.py --format json "What is the average order value?"
```

#### Option D: Jupyter Notebook
```bash
jupyter notebook "Agentic Approach.ipynb"
```

#### Option E: Python API
```python
from pipeline import create_pipeline

pipeline = create_pipeline()
result = pipeline.query("What are the top 5 regions by revenue?")
print(result["answer"])
pipeline.close()
```

## 📁 Project Structure

```
Text-To-SQL/
├── app.py                      # Streamlit web interface
├── pipeline.py                 # Core pipeline logic
├── cli.py                      # Command-line interface
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── Agentic Approach.ipynb     # Jupyter notebook (experimental)
├── Data_CSV/                  # Sample data files
│   ├── 2017_Budgets.csv
│   ├── Customers.csv
│   ├── Products.csv
│   ├── Regions.csv
│   ├── sales_order.csv
│   └── State_Regions.csv
└── logs/                      # Application logs
    └── text_to_sql.log

```

## 🔧 Configuration

### Database Connection
Edit `config.py` or `.env` file:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": "3306",
    "username": "root",
    "password": "vaibhav",
    "database": "regional_sales_data",
}
```

### LLM Settings
```python
LLM_CONFIG = {
    "model": "gemini-2.0-flash",
    "provider": "google_genai",
    "api_key": "your_api_key",
}
```

### Agent Settings
```python
AGENT_CONFIG = {
    "max_iterations": 10,
    "verbose": True,
    "top_k": 5,  # Results per query
}
```

## 📊 Available Tools

The agent has access to 4 SQL tools:

1. **List SQL Database Tool**: Get available tables
2. **Describe SQL Database Tool**: Get table schemas and info
3. **Query SQL Database Tool**: Execute SQL queries safely
4. **Query SQL Checker Tool**: Validate queries before execution

## 🧪 Example Queries

```
"How many products are in the database?"
"List the top 5 customers by total spending"
"What is the average order value per region?"
"Show me products in the Electronics category"
"Which region has the most sales this year?"
"Give me a breakdown of sales by product category"
"How many orders were placed in the last month?"
"What is the revenue trend over the last quarters?"
```

## 📝 API Reference

### TextToSQLPipeline Class

```python
from pipeline import create_pipeline

pipeline = create_pipeline()

# Query the database
result = pipeline.query(
    question="Your question here",
    verbose=False  # Set True for detailed output
)

# Get database information
db_info = pipeline.get_database_info()

# Close connection
pipeline.close()
```

### Return Format

```python
{
    "question": "User's question",
    "timestamp": "ISO timestamp",
    "status": "success|error",
    "answer": "LLM-generated answer",
    "steps": [
        {
            "type": "Message type",
            "content": "Step details"
        }
    ]
}
```

## 🐛 Troubleshooting

### Database Connection Issues
```
Error: "Can't connect to MySQL server"
Solution:
1. Verify MySQL is running: mysql -u root -p
2. Check connection string in config.py
3. Ensure database exists: CREATE DATABASE regional_sales_data;
```

### API Key Issues
```
Error: "Invalid API key"
Solution:
1. Get Google API key from https://makersuite.google.com/app/apikey
2. Update .env file with correct key
3. Restart the application
```

### Missing Packages
```
Error: "No module named 'langchain'"
Solution:
pip install -r requirements.txt
```

### Port Already in Use (Streamlit)
```
Error: "Port 8501 already in use"
Solution:
streamlit run app.py --server.port 8502
```

## 📚 Data Files

CSV files in `Data_CSV/` should be imported into MySQL:
- `Customers.csv`: Customer information
- `Products.csv`: Product catalog
- `sales_order.csv`: Sales transactions
- `Regions.csv`: Geographic regions
- `State_Regions.csv`: State-region mapping
- `2017_Budgets.csv`: Budget data

Import example:
```bash
# In MySQL
LOAD DATA LOCAL INFILE 'C:/path/to/Customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

## 🔐 Security Notes

- Never commit `.env` files with real credentials
- Use environment variables for sensitive data
- Validate all user inputs before executing
- Use prepared statements (implemented by default)
- Consider adding authentication for web interface in production

## 🌟 Features

- ✅ Natural language to SQL conversion
- ✅ Multi-interface (Web, CLI, API, Notebook)
- ✅ Comprehensive logging
- ✅ Error handling and recovery
- ✅ Query history tracking
- ✅ Database introspection
- ✅ ReAct agent architecture
- ✅ Safe SQL execution

## 🚧 Future Enhancements

- [ ] Multi-database support (PostgreSQL, SQLite, etc.)
- [ ] Query caching for performance
- [ ] Advanced authentication
- [ ] Database write capabilities
- [ ] Export results (CSV, JSON, PDF)
- [ ] Query performance optimization suggestions
- [ ] Conversation history and context
- [ ] Custom tool development
- [ ] Docker containerization

## 📞 Support

For issues or questions:
1. Check logs in `logs/text_to_sql.log`
2. Review configuration in `config.py`
3. Verify database connectivity
4. Check API key validity

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Powered by [Google Gemini](https://gemini.google.com)
- Graph orchestration from [LangGraph](https://langgraph.ai)
- UI framework [Streamlit](https://streamlit.io)

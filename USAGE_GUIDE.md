# Text-to-SQL Pipeline - Complete Usage Guide

This guide demonstrates how to use the Text-to-SQL pipeline across different interfaces.

## Table of Contents
1. [Web Interface (Streamlit)](#web-interface)
2. [Command-Line Interface (CLI)](#cli)
3. [Python API](#python-api)
4. [Jupyter Notebook](#jupyter-notebook)
5. [Advanced Usage](#advanced-usage)

---

## Web Interface (Streamlit)

### Starting the Web Server
```bash
streamlit run app.py
```

The web interface opens at `http://localhost:8501` with:
- **Main Query Box**: Enter natural language questions
- **Sidebar**: Database info, query history
- **Tabs**: Answer, Steps, Raw Data

### Features
- Auto-loading query history
- One-click history clearing
- Pretty-printed query steps
- JSON export capability

---

## CLI Interface

### Interactive Mode
```bash
python cli.py --interactive
```

Features:
- Continuous query loop
- Built-in help command
- Formatted output display
- Easy exit

### Single Query Mode
```bash
# Basic query
python cli.py "How many products are there?"

# Verbose output
python cli.py --verbose "List top customers"

# JSON format
python cli.py --format json "Total sales by region?"
```

### Commands
- `exit`: Quit the application
- `help`: Show available commands
- Any other text is treated as a query

---

## Python API

### Basic Usage
```python
from pipeline import create_pipeline

# Initialize pipeline
pipeline = create_pipeline()

# Execute query
result = pipeline.query("How many customers do we have?")

# Access results
print(result["status"])      # "success" or "error"
print(result["answer"])       # The answer text
print(result["steps"])        # List of execution steps

# Clean up
pipeline.close()
```

### Get Database Information
```python
# Get available tables and schemas
db_info = pipeline.get_database_info()

print("Tables:", db_info["tables"])
print("Dialect:", db_info["dialect"])
print("Table Info:")
print(db_info["table_info"])
```

### Error Handling
```python
from pipeline import create_pipeline

pipeline = create_pipeline()

try:
    result = pipeline.query("Your question")
    if result["status"] == "error":
        print(f"Error: {result['error']}")
    else:
        print(result["answer"])
except Exception as e:
    print(f"Pipeline error: {e}")
finally:
    pipeline.close()
```

### Batch Processing
```python
from pipeline import create_pipeline

pipeline = create_pipeline()

questions = [
    "How many products are there?",
    "List top 5 customers",
    "What is the total revenue?"
]

results = []
for question in questions:
    result = pipeline.query(question)
    results.append(result)
    print(f"Q: {question}")
    print(f"A: {result['answer']}\n")

pipeline.close()
```

---

## Jupyter Notebook

### Using the Demo Notebook
1. Open: `Agentic Approach.ipynb`
2. Run cells in order

### Cell Descriptions

**Cell 1**: Setup imports
```python
from langchain_community.utilities import SQLDatabase
```

**Cell 2**: Database configuration
```python
mysql_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
```

**Cell 3**: Initialize database
```python
db = SQLDatabase.from_uri(mysql_uri)
```

**Cell 4**: Initialize LLM
```python
from langchain.chat_models import init_chat_model
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
```

**Cell 5**: Create agent
```python
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_react_agent(llm, toolkit.get_tools())
```

**Cell 6**: Execute query
```python
events = agent_executor.stream(
    {"messages": [("user", "Your question")]},
    stream_mode="values"
)
```

---

## Advanced Usage

### Custom Configuration
```python
from config import DB_CONFIG, LLM_CONFIG, AGENT_CONFIG

# Modify configuration
DB_CONFIG["host"] = "remote.server.com"
LLM_CONFIG["model"] = "gemini-1.5-pro"
AGENT_CONFIG["max_iterations"] = 15
```

### Verbose Execution
```python
from pipeline import create_pipeline

pipeline = create_pipeline()

# Get detailed execution steps
result = pipeline.query("Your question", verbose=True)

# Print execution flow
for i, step in enumerate(result["steps"], 1):
    print(f"Step {i}: {step['type']}")
    print(step['content'])
```

### Logging Configuration
Logs are written to `logs/text_to_sql.log`

View logs:
```bash
tail -f logs/text_to_sql.log  # Unix/Mac
type logs/text_to_sql.log     # Windows
```

### Multiple Queries with State
```python
from pipeline import create_pipeline

pipeline = create_pipeline()

# Simulate conversation flow
queries = [
    "How many regions do we have?",
    "Which region has the highest sales?",
    "What products are sold in that region?"
]

for q in queries:
    result = pipeline.query(q)
    print(f"Q: {q}")
    print(f"A: {result['answer']}\n")

pipeline.close()
```

### Response Parsing
```python
result = pipeline.query("Show me top 5 products")

# Extract data from answer
answer = result["answer"]

# Process based on status
if result["status"] == "success":
    # You can parse the answer string for structured data
    if "product" in result["answer"].lower():
        print("Query returned product data")
else:
    # Handle error
    print(f"Error: {result.get('error')}")
```

### Integration Example
```python
from pipeline import create_pipeline
import json

class DatabaseQueryHandler:
    def __init__(self):
        self.pipeline = create_pipeline()
    
    def answer_question(self, question):
        result = self.pipeline.query(question)
        return {
            "success": result["status"] == "success",
            "answer": result.get("answer"),
            "error": result.get("error")
        }
    
    def __del__(self):
        self.pipeline.close()

# Usage
handler = DatabaseQueryHandler()
response = handler.answer_question("Total revenue by quarter?")
print(json.dumps(response, indent=2))
```

---

## Environment Variables

Create or update `.env` file:

```
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=vaibhav
DB_NAME=regional_sales_data

# API Keys
GOOGLE_API_KEY=your_api_key

# Agent
AGENT_MAX_ITERATIONS=10
AGENT_VERBOSE=true
```

---

## Troubleshooting

### Issue: Database Connection Error
```
Solution:
1. Verify MySQL is running
2. Check credentials in .env or config.py
3. Ensure database exists
```

### Issue: API Rate Limits
```
Solution:
1. Add delays between requests
2. Use caching for repeated queries
3. Check API quota
```

### Issue: Slow Queries
```
Solution:
1. Reduce query complexity
2. Use AGENT_CONFIG["top_k"] = 3 for fewer results
3. Add database indexes
```

### Issue: Port Already in Use
```
Solution (for Streamlit):
streamlit run app.py --server.port 8502
```

---

## Performance Tips

1. **Batch Queries**: Execute multiple questions in one session
2. **Reuse Pipeline**: Don't create/close pipeline for each query
3. **Limit Results**: Use `top_k` setting to limit results
4. **Database Indexes**: Index frequently queried columns
5. **Connection Pooling**: Reuse database connections

---

## Example Queries to Try

```
"How many products are in each category?"
"Show me the top 10 customers by revenue"
"What is the average order value?"
"How many new customers did we gain this month?"
"Which region had the highest growth?"
"List all orders from the last 7 days"
"Show me the product mix by region"
"What is our customer retention rate?"
```

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Configure `.env` file
3. ✅ Test connection: `python cli.py "Test query"`
4. ✅ Start web UI: `streamlit run app.py`
5. ✅ Integrate into your application

---

For more information, see README.md

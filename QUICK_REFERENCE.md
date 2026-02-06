# 🚀 Text-to-SQL Pipeline - Quick Reference Card

## Installation (First Time)

### Windows
```bash
run.bat
```

### Mac/Linux
```bash
make setup
```

### Manual
```bash
pip install -r requirements.txt
python setup.py
```

---

## Basic Usage

### Web Interface
```bash
streamlit run app.py
# Opens: http://localhost:8501
```

### Command Line - Single Query
```bash
python cli.py "How many products?"
python cli.py --verbose "List top customers"
python cli.py --format json "Total sales?"
```

### Interactive CLI
```bash
python cli.py --interactive
# Type 'exit' to quit
```

### Python Code
```python
from pipeline import create_pipeline

pipeline = create_pipeline()
result = pipeline.query("Your question here")
print(result["answer"])
pipeline.close()
```

---

## Configuration

### Edit .env File
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=vaibhav
DB_NAME=regional_sales_data
GOOGLE_API_KEY=your_api_key_here
```

### Or Edit config.py
```python
DB_CONFIG = {
    "host": "localhost",
    "port": "3306",
    ...
}
```

---

## Common Commands

| Task | Command |
|------|---------|
| Start web UI | `streamlit run app.py` |
| Interactive CLI | `python cli.py --interactive` |
| Single query | `python cli.py "question"` |
| Run tests | `python test_pipeline.py` |
| View logs | `tail -f logs/text_to_sql.log` |
| Docker start | `docker-compose up` |
| Help | `python cli.py --help` |

---

## Example Queries

```
"How many products are in the database?"
"List the top 5 customers by sales"
"What is the total revenue by region?"
"Show sales by product category"
"Which region has the most orders?"
"Average order value per customer?"
```

---

## Troubleshooting

### Database Won't Connect
```bash
# Check MySQL is running
mysql -u root -p

# Verify credentials in .env
cat .env

# Test connection from Python
python -c "from pipeline import create_pipeline; create_pipeline()"
```

### API Key Issues
```bash
# Get new key from: https://makersuite.google.com/app/apikey
# Update .env file
# Restart application
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install -r requirements.txt
python setup.py
```

---

## Project Structure

```
├── app.py                 # Web UI
├── cli.py                 # Command line
├── pipeline.py            # Core logic
├── config.py              # Settings
├── setup.py               # Setup script
├── test_pipeline.py       # Tests
├── requirements.txt       # Dependencies
├── .env                   # Credentials (create from .env.example)
├── README.md              # Full documentation
├── USAGE_GUIDE.md         # Detailed usage
├── DEPLOYMENT.md          # Deployment guide
└── Data_CSV/              # Sample data files
```

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| DB_HOST | Database server | localhost |
| DB_PORT | Database port | 3306 |
| DB_USER | Database user | root |
| DB_PASSWORD | Database password | vaibhav |
| DB_NAME | Database name | regional_sales_data |
| GOOGLE_API_KEY | Gemini API key | AIza... |

---

## Docker Quick Start

```bash
# Build image
docker build -t text-to-sql .

# Run with compose
docker-compose up

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Python API Quick Reference

```python
from pipeline import create_pipeline

# Initialize
pipeline = create_pipeline()

# Execute query
result = pipeline.query("Your question")

# Access results
result["status"]      # "success" or "error"
result["answer"]      # The response text
result["steps"]       # Execution steps list
result["timestamp"]   # ISO timestamp

# Get database info
info = pipeline.get_database_info()
info["tables"]        # List of table names
info["table_info"]    # Schema information

# Cleanup
pipeline.close()
```

---

## Response Format

```python
{
    "question": "User's question",
    "timestamp": "2026-02-06T10:30:00",
    "status": "success",  # or "error"
    "answer": "The answer text",
    "steps": [
        {
            "type": "HumanMessage|AgentMessage|ToolMessage",
            "content": "Step content"
        }
    ],
    "error": None  # If status is "error"
}
```

---

## Files at a Glance

| File | Purpose | Run With |
|------|---------|----------|
| app.py | Web UI | `streamlit run app.py` |
| cli.py | CLI tool | `python cli.py` |
| pipeline.py | Core logic | `from pipeline import create_pipeline` |
| setup.py | Setup | `python setup.py` |
| test_pipeline.py | Tests | `python test_pipeline.py` |

---

## Services & Ports

| Service | Port | URL |
|---------|------|-----|
| Streamlit | 8501 | http://localhost:8501 |
| MySQL | 3306 | localhost:3306 |
| API | - | Python module |

---

## Logging

Logs are saved to: `logs/text_to_sql.log`

View logs:
```bash
# Real-time
tail -f logs/text_to_sql.log

# Last 100 lines
tail -100 logs/text_to_sql.log

# Search for errors
grep ERROR logs/text_to_sql.log
```

---

## Getting Help

1. **Check README.md** for full documentation
2. **See USAGE_GUIDE.md** for detailed examples
3. **Read DEPLOYMENT.md** for production setup
4. **Run test_pipeline.py** to diagnose issues
5. **Check logs** in logs/text_to_sql.log

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| DB connection error | Check MySQL running, verify .env |
| API key invalid | Get new key, update .env |
| Port in use | Use --server.port 8502 |
| Missing packages | Run: `pip install -r requirements.txt` |
| Slow queries | Reduce top_k in AGENT_CONFIG |

---

## Resources

- 📖 Documentation: See README.md
- 🚀 Deployment: See DEPLOYMENT.md  
- 📚 Usage: See USAGE_GUIDE.md
- 🧪 Tests: Run test_pipeline.py
- 📦 Components: See PIPELINE_COMPONENTS.md

---

**Version**: 1.0  
**Last Updated**: February 6, 2026  
**Status**: Production Ready

Print this card for quick reference! 📋

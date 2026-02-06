"""Core pipeline for Text-to-SQL agent"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain import hub

from config import DB_CONFIG, LLM_CONFIG, AGENT_CONFIG, LOG_CONFIG, get_mysql_uri

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["level"]),
    format=LOG_CONFIG["format"],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_CONFIG["file"])
    ]
)
logger = logging.getLogger(__name__)


class TextToSQLPipeline:
    """Main pipeline for converting natural language queries to SQL"""
    
    def __init__(self):
        """Initialize the pipeline"""
        self.db = None
        self.llm = None
        self.agent_executor = None
        self.toolkit = None
        self.system_message = None
        
        logger.info("Initializing Text-to-SQL Pipeline")
        self._initialize()
    
    def _initialize(self):
        """Initialize all components"""
        try:
            # Initialize database
            logger.info(f"Connecting to database: {DB_CONFIG['database']}")
            mysql_uri = get_mysql_uri()
            self.db = SQLDatabase.from_uri(mysql_uri)
            logger.info(f"Database connected. Available tables: {self.db.get_usable_table_names()}")
            
            # Initialize LLM
            logger.info(f"Initializing LLM: {LLM_CONFIG['model']}")
            self.llm = init_chat_model(
                LLM_CONFIG["model"],
                model_provider=LLM_CONFIG["provider"]
            )
            logger.info("LLM initialized successfully")
            
            # Initialize toolkit
            self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            tools = self.toolkit.get_tools()
            logger.info(f"SQLDatabaseToolkit initialized with {len(tools)} tools")
            
            # Load system prompt
            logger.info("Loading system prompt template")
            prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
            self.system_message = prompt_template.format(
                dialect="mysql",
                top_k=AGENT_CONFIG["top_k"]
            )
            
            # Create agent executor
            logger.info("Creating ReAct agent executor")
            self.agent_executor = create_react_agent(
                self.llm,
                tools,
                prompt=self.system_message,
                state_modifier=None
            )
            logger.info("Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing pipeline: {str(e)}")
            raise
    
    def query(self, question: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Execute a natural language query
        
        Args:
            question: Natural language question
            verbose: Print intermediate steps
            
        Returns:
            Dictionary containing the response and metadata
        """
        if not self.agent_executor:
            raise RuntimeError("Pipeline not properly initialized")
        
        logger.info(f"Processing query: {question}")
        
        try:
            response_data = {
                "question": question,
                "timestamp": datetime.now().isoformat(),
                "status": "processing",
                "answer": None,
                "steps": []
            }
            
            # Execute query
            events = self.agent_executor.stream(
                {"messages": [("user", question)]},
                stream_mode="values",
            )
            
            for event in events:
                last_message = event["messages"][-1]
                
                if verbose:
                    last_message.pretty_print()
                
                response_data["steps"].append({
                    "type": type(last_message).__name__,
                    "content": str(last_message.content)
                })
            
            # Extract final answer
            if response_data["steps"]:
                final_step = response_data["steps"][-1]
                response_data["answer"] = final_step["content"]
                response_data["status"] = "success"
            
            logger.info(f"Query processed successfully")
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            response_data["status"] = "error"
            response_data["error"] = str(e)
            return response_data
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get information about available tables and schemas"""
        if not self.db:
            raise RuntimeError("Database not connected")
        
        try:
            tables = self.db.get_usable_table_names()
            info = {
                "tables": tables,
                "dialect": self.db.dialect,
                "table_info": self.db.get_table_info()
            }
            logger.info(f"Retrieved database info for {len(tables)} tables")
            return info
        except Exception as e:
            logger.error(f"Error retrieving database info: {str(e)}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.db:
            try:
                self.db.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.warning(f"Error closing database: {str(e)}")


def create_pipeline() -> TextToSQLPipeline:
    """Factory function to create pipeline instance"""
    return TextToSQLPipeline()

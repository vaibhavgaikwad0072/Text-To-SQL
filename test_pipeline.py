"""Testing suite for Text-to-SQL Pipeline"""

import sys
import json
from pathlib import Path
from typing import List, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def run_all(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("Text-to-SQL Pipeline Test Suite")
        print("="*60 + "\n")
        
        self.test_imports()
        self.test_config()
        self.test_database_connection()
        self.test_pipeline_initialization()
        self.test_sample_queries()
        
        self.print_summary()
    
    def test_imports(self):
        """Test if all required packages are installed"""
        print("🧪 Testing imports...")
        try:
            import langchain
            import streamlit
            import pymysql
            import dotenv
            import langgraph
            print("✅ All imports successful\n")
            self.tests_passed += 1
        except ImportError as e:
            print(f"❌ Import error: {e}\n")
            self.tests_failed += 1
            self.results.append(("Imports", str(e)))
    
    def test_config(self):
        """Test configuration loading"""
        print("🧪 Testing configuration...")
        try:
            from config import DB_CONFIG, LLM_CONFIG, get_mysql_uri
            
            # Verify config structure
            assert "host" in DB_CONFIG
            assert "database" in DB_CONFIG
            assert "model" in LLM_CONFIG
            assert "api_key" in LLM_CONFIG
            
            uri = get_mysql_uri()
            assert "mysql" in uri
            
            print(f"✅ Configuration loaded successfully")
            print(f"   Database: {DB_CONFIG['database']}")
            print(f"   LLM: {LLM_CONFIG['model']}\n")
            self.tests_passed += 1
        except Exception as e:
            print(f"❌ Configuration error: {e}\n")
            self.tests_failed += 1
            self.results.append(("Configuration", str(e)))
    
    def test_database_connection(self):
        """Test database connectivity"""
        print("🧪 Testing database connection...")
        try:
            from config import get_mysql_uri
            from langchain_community.utilities import SQLDatabase
            
            mysql_uri = get_mysql_uri()
            db = SQLDatabase.from_uri(mysql_uri)
            tables = db.get_usable_table_names()
            
            print(f"✅ Database connected successfully")
            print(f"   Tables: {', '.join(tables) if tables else 'None found'}\n")
            
            db.close()
            self.tests_passed += 1
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            print(f"   Make sure MySQL is running and credentials are correct\n")
            self.tests_failed += 1
            self.results.append(("Database Connection", str(e)))
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        print("🧪 Testing pipeline initialization...")
        try:
            from pipeline import create_pipeline
            
            pipeline = create_pipeline()
            
            print(f"✅ Pipeline initialized successfully")
            
            # Get database info
            db_info = pipeline.get_database_info()
            print(f"   Available tables: {len(db_info['tables'])}")
            
            pipeline.close()
            self.tests_passed += 1
        except Exception as e:
            print(f"❌ Pipeline initialization error: {e}\n")
            self.tests_failed += 1
            self.results.append(("Pipeline Init", str(e)))
    
    def test_sample_queries(self):
        """Test sample queries"""
        print("🧪 Testing sample queries...")
        
        sample_queries = [
            "Hello, are you working?",
            "How many products are there?",
            "List the available tables",
        ]
        
        try:
            from pipeline import create_pipeline
            
            pipeline = create_pipeline()
            passed = 0
            failed = 0
            
            for i, query in enumerate(sample_queries, 1):
                try:
                    print(f"\n   Query {i}: {query}")
                    result = pipeline.query(query, verbose=False)
                    
                    if result["status"] == "success":
                        print(f"   ✓ Status: Success")
                        print(f"   Answer: {result['answer'][:100]}...")
                        passed += 1
                    else:
                        print(f"   ✗ Status: {result['status']}")
                        if "error" in result:
                            print(f"   Error: {result['error']}")
                        failed += 1
                except Exception as e:
                    print(f"   ✗ Error: {e}")
                    failed += 1
            
            pipeline.close()
            
            print(f"\n✅ Query testing completed: {passed}/{len(sample_queries)} passed")
            if failed == 0:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            
        except Exception as e:
            print(f"❌ Sample query error: {e}\n")
            self.tests_failed += 1
            self.results.append(("Sample Queries", str(e)))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 Test Summary")
        print("="*60)
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"Total: {self.tests_passed + self.tests_failed}")
        
        if self.tests_failed > 0:
            print("\n❌ Failed Tests:")
            for test_name, error in self.results:
                print(f"  • {test_name}: {error}")
        
        print("="*60 + "\n")
        
        return self.tests_failed == 0


def main():
    """Run test suite"""
    suite = TestSuite()
    success = suite.run_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

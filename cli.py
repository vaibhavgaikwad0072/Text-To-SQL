"""Command-line interface for Text-to-SQL Pipeline"""

import argparse
import json
from pipeline import create_pipeline
from tabulate import tabulate
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Text-to-SQL Query Interface")
    parser.add_argument(
        "query",
        type=str,
        help="Natural language query"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed output"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = create_pipeline()
    
    try:
        if args.interactive:
            interactive_mode(pipeline)
        else:
            result = pipeline.query(args.query, verbose=args.verbose)
            
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print_text_result(result, args.verbose)
    finally:
        pipeline.close()


def interactive_mode(pipeline):
    """Interactive query mode"""
    print("\n" + "="*60)
    print("Text-to-SQL Interactive Mode")
    print("Type 'exit' to quit, 'help' for commands")
    print("="*60 + "\n")
    
    # Display database info
    try:
        db_info = pipeline.get_database_info()
        print(f"Connected to database with tables: {', '.join(db_info['tables'])}\n")
    except Exception as e:
        print(f"Error getting database info: {e}\n")
    
    while True:
        try:
            query = input("\n📝 Enter your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() == "exit":
                print("Goodbye!")
                break
            
            if query.lower() == "help":
                print("""
Available commands:
  - exit: Quit the application
  - help: Show this help message
  - Or ask any question about your database!
                """)
                continue
            
            print("\ Processing...")
            result = pipeline.query(query, verbose=False)
            print_text_result(result, verbose=False)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_text_result(result, verbose=False):
    """Print result in human-readable format"""
    print("\n" + "="*60)
    print(f"Status: {result['status'].upper()}")
    print("="*60)
    
    if result["status"] == "error":
        print(f" Error: {result.get('error', 'Unknown error')}")
    else:
        print(f"\n Question: {result['question']}")
        print(f"\n Answer:\n{result['answer']}")
        
        if verbose and result["steps"]:
            print(f"\n Execution Steps ({len(result['steps'])} steps):")
            print("-" * 60)
            for i, step in enumerate(result["steps"], 1):
                print(f"\nStep {i}: {step['type']}")
                print(f"Content: {step['content'][:200]}...")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

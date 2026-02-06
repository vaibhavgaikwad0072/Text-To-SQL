"""Streamlit web interface for Text-to-SQL Pipeline"""

import streamlit as st
import json
from datetime import datetime
import logging

from pipeline import create_pipeline

# Setup page config
st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if "pipeline" not in st.session_state:
    st.session_state.pipeline = create_pipeline()

if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")
    
    # Database Info
    st.subheader("Database Info")
    try:
        db_info = st.session_state.pipeline.get_database_info()
        st.success("✓ Database Connected")
        with st.expander("View Tables"):
            for table in db_info["tables"]:
                st.write(f"• {table}")
    except Exception as e:
        st.error(f"✗ Database Error: {str(e)}")
    
    st.markdown("---")
    
    # Query History
    st.subheader("Query History")
    if st.session_state.query_history:
        if st.button("🗑️ Clear History"):
            st.session_state.query_history = []
            st.rerun()
        
        for i, item in enumerate(reversed(st.session_state.query_history), 1):
            with st.expander(f"{i}. {item['question'][:50]}..."):
                st.write(f"**Status**: {item['status']}")
                st.write(f"**Time**: {item['timestamp']}")
                if item['answer']:
                    st.write(f"**Answer**: {item['answer']}")
    else:
        st.info("No queries yet")

# Main content
st.title("🤖 Text-to-SQL Agent")
st.markdown("""
Convert natural language questions to SQL queries automatically!
Ask questions about your database in plain English.
""")

st.markdown("---")

# Query input
col1, col2 = st.columns([4, 1])
with col1:
    user_question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What are the top 5 products by sales?",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("🔍 Query", use_container_width=True)

# Process query
if submit_button and user_question:
    with st.spinner("Processing your question..."):
        try:
            result = st.session_state.pipeline.query(user_question, verbose=False)
            st.session_state.query_history.append(result)
            
            # Display results
            if result["status"] == "success":
                st.success("✓ Query Processed Successfully")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["Answer", "Steps", "Raw Data"])
                
                with tab1:
                    st.markdown("### Answer")
                    st.write(result["answer"])
                
                with tab2:
                    st.markdown("### Execution Steps")
                    for i, step in enumerate(result["steps"], 1):
                        with st.expander(f"Step {i}: {step['type']}"):
                            st.code(step["content"], language="text")
                
                with tab3:
                    st.markdown("### Raw Response Data")
                    st.json(result)
                    
            elif result["status"] == "error":
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                st.write(result)
                
        except Exception as e:
            st.error(f"❌ Pipeline Error: {str(e)}")
            logger.error(f"Error in pipeline: {str(e)}", exc_info=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    Powered by LangChain, Google Gemini 2.0 Flash, and LangGraph
    </div>
    """,
    unsafe_allow_html=True
)

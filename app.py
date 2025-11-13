"""Streamlit app for Dumroo Admin Panel AI Query System."""
import streamlit as st
import os
from dotenv import load_dotenv
from access_control import DEMO_ADMINS
from data_manager import DataManager
from query_agent import QueryAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Dumroo Admin Panel - AI Query",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Dumroo Admin Panel - AI Query System")
st.markdown("Ask questions about student data in plain English")

# Sidebar for admin selection and API key
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key"
    )
    
    st.divider()
    
    # Admin selection
    st.header("👤 Admin Login")
    admin_id = st.selectbox(
        "Select Admin",
        options=list(DEMO_ADMINS.keys()),
        format_func=lambda x: f"{DEMO_ADMINS[x].name} ({x})"
    )
    
    admin_role = DEMO_ADMINS[admin_id]
    
    st.info(f"""
    **Access Scope:**  
    {admin_role.get_scope_description()}
    
    You can only access data within your assigned scope.
    """)
    
    st.divider()
    
    st.header("💡 Example Queries")
    st.markdown("""
    - Which students haven't submitted their homework yet?
    - Show me performance data for Grade 8 from last week
    - List all upcoming quizzes scheduled for next week
    - Who are my students?
    """)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'current_admin' not in st.session_state:
    st.session_state.current_admin = None

# Reinitialize agent if admin changed or API key provided
if api_key and (st.session_state.current_admin != admin_id or st.session_state.agent is None):
    try:
        # Validate API key format
        if not api_key.startswith('sk-'):
            st.error("Invalid API key format. OpenAI API keys start with 'sk-'")
        else:
            with st.spinner("Initializing AI agent..."):
                data_manager = DataManager()
                st.session_state.agent = QueryAgent(data_manager, admin_role, api_key)
                st.session_state.current_admin = admin_id
                st.session_state.messages = []  # Clear chat history on admin change
                logger.info(f"Agent initialized for admin: {admin_id}")
    except FileNotFoundError as e:
        st.error(f"Data file not found: {str(e)}")
        logger.error(f"Data file error: {str(e)}")
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        logger.error(f"Agent initialization error: {str(e)}", exc_info=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about student data..."):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
    elif st.session_state.agent is None:
        st.error("Agent not initialized. Please check your API key.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.agent.query(prompt)
                    st.markdown(response)
                    # Add assistant message
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Query error: {str(e)}", exc_info=True)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    if st.session_state.agent:
        st.session_state.agent.memory.clear()
    st.rerun()

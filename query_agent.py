"""AI agent for natural language query processing."""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from data_manager import DataManager
import logging

logger = logging.getLogger(__name__)


class QueryAgent:
    """Agent that processes natural language queries about student data."""
    
    def __init__(self, data_manager, admin_role, api_key):
        self.data_manager = data_manager
        self.admin_role = admin_role
        
        if not api_key:
            raise ValueError("API key is required")
        
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                api_key=api_key,
                request_timeout=30
            )
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            self.agent_executor = self._create_agent()
            logger.info("QueryAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize QueryAgent: {str(e)}")
            raise
    
    def _create_tools(self):
        """Create tools for the agent to use."""
        
        def get_students_no_homework(query: str) -> str:
            """Find students who haven't submitted their homework."""
            df = self.data_manager.query_students_no_homework(self.admin_role)
            if df.empty:
                return "No students found or no access to data."
            return df[['name', 'grade', 'class', 'homework_date']].to_string(index=False)
        
        def get_performance_data(query: str) -> str:
            """Get performance data. Query should mention grade number."""
            import re
            grade_match = re.search(r'grade\s*(\d+)', query.lower())
            if not grade_match:
                return "Please specify a grade number (e.g., Grade 8)"
            
            grade = int(grade_match.group(1))
            df = self.data_manager.query_performance_by_grade(self.admin_role, grade)
            if df.empty:
                return f"No performance data found for Grade {grade} or no access."
            return df[['name', 'grade', 'class', 'quiz_score', 'quiz_date']].to_string(index=False)
        
        def get_upcoming_quizzes(query: str) -> str:
            """Get upcoming quizzes scheduled for next week."""
            df = self.data_manager.query_upcoming_quizzes(self.admin_role)
            if df.empty:
                return "No upcoming quizzes found or no access to data."
            return df[['title', 'grade', 'class', 'scheduled_date']].to_string(index=False)
        
        def get_all_students(query: str) -> str:
            """Get all accessible students."""
            df = self.data_manager.get_filtered_students(self.admin_role)
            if df.empty:
                return "No students accessible."
            return df[['name', 'grade', 'class', 'region']].to_string(index=False)
        
        return [
            Tool(
                name="students_no_homework",
                func=get_students_no_homework,
                description="Use this to find students who haven't submitted homework"
            ),
            Tool(
                name="performance_data",
                func=get_performance_data,
                description="Use this to get quiz performance data for a specific grade"
            ),
            Tool(
                name="upcoming_quizzes",
                func=get_upcoming_quizzes,
                description="Use this to get upcoming quizzes scheduled for next week"
            ),
            Tool(
                name="all_students",
                func=get_all_students,
                description="Use this to list all students you have access to"
            )
        ]
    
    def _create_agent(self):
        """Create the agent executor."""
        tools = self._create_tools()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an AI assistant for the Dumroo Admin Panel. 
You help admins query student data using natural language.

Current admin scope: {self.admin_role.get_scope_description()}

Important: This admin can ONLY access data within their assigned scope. 
They cannot access platform-wide data or other admins' data.

When answering queries:
1. Use the appropriate tool to fetch data
2. Present results in a clear, readable format
3. If no data is found, explain it might be due to access restrictions
4. Be helpful and conversational"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def query(self, question):
        """Process a natural language query."""
        if not question or not question.strip():
            return "Please provide a valid question."
        
        try:
            logger.info(f"Processing query: {question[:100]}...")
            response = self.agent_executor.invoke({"input": question})
            logger.info("Query processed successfully")
            return response['output']
        except Exception as e:
            error_msg = f"I encountered an error while processing your query. Please try rephrasing or contact support if the issue persists."
            logger.error(f"Query processing error: {str(e)}", exc_info=True)
            return error_msg

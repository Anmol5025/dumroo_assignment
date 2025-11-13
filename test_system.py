"""Test script to verify the system is working correctly."""
import os
from dotenv import load_dotenv
from access_control import DEMO_ADMINS
from data_manager import DataManager
from query_agent import QueryAgent

def test_data_manager():
    """Test data manager functionality."""
    print("Testing DataManager...")
    try:
        dm = DataManager()
        admin = DEMO_ADMINS['admin1']
        
        students = dm.get_filtered_students(admin)
        print(f"✓ Found {len(students)} students for {admin.name}")
        
        quizzes = dm.get_filtered_quizzes(admin)
        print(f"✓ Found {len(quizzes)} quizzes for {admin.name}")
        
        no_homework = dm.query_students_no_homework(admin)
        print(f"✓ Found {len(no_homework)} students without homework")
        
        return True
    except Exception as e:
        print(f"✗ DataManager test failed: {str(e)}")
        return False

def test_query_agent():
    """Test query agent functionality."""
    print("\nTesting QueryAgent...")
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("✗ No API key found in .env file")
        return False
    
    try:
        dm = DataManager()
        admin = DEMO_ADMINS['admin1']
        agent = QueryAgent(dm, admin, api_key)
        
        print(f"✓ Agent initialized for {admin.name}")
        
        # Test a simple query
        print("\nTesting query: 'Who are my students?'")
        response = agent.query("Who are my students?")
        print(f"Response: {response[:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ QueryAgent test failed: {str(e)}")
        return False

def test_access_control():
    """Test access control functionality."""
    print("\nTesting Access Control...")
    try:
        admin1 = DEMO_ADMINS['admin1']
        admin2 = DEMO_ADMINS['admin2']
        
        # Test student from admin1's scope
        student_grade8 = {'grade': 8, 'region': 'North'}
        assert admin1.can_access_student(student_grade8), "Admin1 should access Grade 8 North"
        assert not admin2.can_access_student(student_grade8), "Admin2 should NOT access Grade 8 North"
        
        print("✓ Access control working correctly")
        return True
    except Exception as e:
        print(f"✗ Access control test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Dumroo Admin Panel - System Tests")
    print("=" * 60)
    
    results = []
    results.append(("Data Manager", test_data_manager()))
    results.append(("Access Control", test_access_control()))
    results.append(("Query Agent", test_query_agent()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! System is ready.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 60)

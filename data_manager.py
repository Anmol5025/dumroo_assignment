"""Data management with role-based filtering."""
import json
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)


class DataManager:
    """Manages data access with role-based filtering."""
    
    def __init__(self, data_file="data.json"):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            if 'students' not in self.data or 'quizzes' not in self.data:
                raise ValueError("Invalid data format: missing 'students' or 'quizzes' key")
            
            self.students_df = pd.DataFrame(self.data['students'])
            self.quizzes_df = pd.DataFrame(self.data['quizzes'])
            logger.info(f"DataManager initialized with {len(self.students_df)} students and {len(self.quizzes_df)} quizzes")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def get_filtered_students(self, admin_role):
        """Get students accessible to this admin."""
        try:
            filtered = [s for s in self.data['students'] if admin_role.can_access_student(s)]
            logger.debug(f"Filtered {len(filtered)} students for admin {admin_role.admin_id}")
            return pd.DataFrame(filtered) if filtered else pd.DataFrame()
        except Exception as e:
            logger.error(f"Error filtering students: {str(e)}")
            return pd.DataFrame()
    
    def get_filtered_quizzes(self, admin_role):
        """Get quizzes accessible to this admin."""
        try:
            filtered = [q for q in self.data['quizzes'] if admin_role.can_access_quiz(q)]
            logger.debug(f"Filtered {len(filtered)} quizzes for admin {admin_role.admin_id}")
            return pd.DataFrame(filtered) if filtered else pd.DataFrame()
        except Exception as e:
            logger.error(f"Error filtering quizzes: {str(e)}")
            return pd.DataFrame()
    
    def query_students_no_homework(self, admin_role):
        """Find students who haven't submitted homework."""
        df = self.get_filtered_students(admin_role)
        if df.empty:
            return df
        return df[df['homework_submitted'] == False]
    
    def query_performance_by_grade(self, admin_role, grade, days_back=7):
        """Get performance data for a specific grade from recent days."""
        try:
            df = self.get_filtered_students(admin_role)
            if df.empty:
                return df
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            df['quiz_date'] = pd.to_datetime(df['quiz_date'], errors='coerce')
            
            result = df[
                (df['grade'] == grade) & 
                (df['quiz_date'] >= cutoff_date)
            ]
            return result
        except Exception as e:
            logger.error(f"Error querying performance data: {str(e)}")
            return pd.DataFrame()
    
    def query_upcoming_quizzes(self, admin_role, days_ahead=7):
        """Get upcoming quizzes scheduled within next N days."""
        try:
            df = self.get_filtered_quizzes(admin_role)
            if df.empty:
                return df
            
            today = datetime.now()
            future_date = today + timedelta(days=days_ahead)
            df['scheduled_date'] = pd.to_datetime(df['scheduled_date'], errors='coerce')
            
            result = df[
                (df['scheduled_date'] >= today) & 
                (df['scheduled_date'] <= future_date) &
                (df['status'] == 'upcoming')
            ]
            return result
        except Exception as e:
            logger.error(f"Error querying upcoming quizzes: {str(e)}")
            return pd.DataFrame()

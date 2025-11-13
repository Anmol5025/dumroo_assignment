"""Role-based access control for admin users."""

class AdminRole:
    """Represents an admin user with specific access scope."""
    
    def __init__(self, admin_id, name, grade=None, class_section=None, region=None):
        self.admin_id = admin_id
        self.name = name
        self.grade = grade
        self.class_section = class_section
        self.region = region
    
    def can_access_student(self, student):
        """Check if admin can access this student's data."""
        if self.grade and student.get('grade') != self.grade:
            return False
        if self.class_section and student.get('class') != self.class_section:
            return False
        if self.region and student.get('region') != self.region:
            return False
        return True
    
    def can_access_quiz(self, quiz):
        """Check if admin can access this quiz data."""
        if self.grade and quiz.get('grade') != self.grade:
            return False
        if self.class_section and quiz.get('class') != self.class_section:
            return False
        if self.region and quiz.get('region') != self.region:
            return False
        return True
    
    def get_scope_description(self):
        """Return a human-readable description of admin's scope."""
        parts = []
        if self.grade:
            parts.append(f"Grade {self.grade}")
        if self.class_section:
            parts.append(f"Class {self.class_section}")
        if self.region:
            parts.append(f"Region {self.region}")
        return ", ".join(parts) if parts else "All accessible data"


# Predefined admin roles for demo
DEMO_ADMINS = {
    "admin1": AdminRole("admin1", "John Doe", grade=8, region="North"),
    "admin2": AdminRole("admin2", "Jane Smith", grade=9, region="South"),
    "admin3": AdminRole("admin3", "Mike Johnson", grade=7, region="East"),
}

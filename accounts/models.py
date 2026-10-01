from django.contrib.auth import get_user_model
from django.db import models

UserProfile = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    section = models.CharField(max_length=10, blank=True, null=True)  # Only for students
    student_id = models.CharField(max_length=20, blank=True, null=True)  # Only for students
    department = models.CharField(max_length=50, blank=True, null=True)  # Only for teachers

    def __str__(self):
        return f"{self.user.username} - {self.role}"
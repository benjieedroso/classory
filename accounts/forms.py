from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        
class ProfileSetupStudent(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    section = forms.CharField(max_length=10, required=True)  # Only for students
    student_id = forms.CharField(max_length=20, required=False)  # Only for students

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'section', 'student_id']
        
        
class ProfileSetupTeacher(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    department = forms.CharField(max_length=50, required=False)  # Only for teachers

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'department']
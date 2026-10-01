from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    subject = forms.CharField(max_length=100, required=True)
    grade_level = forms.CharField(max_length=50, required=True)
    excel_file = forms.FileField(required=False, help_text="Upload an Excel file with student data (optional).")
    
    class Meta:
        model = Classroom
        fields = ['name', 'description', 'subject', 'grade_level', 'excel_file']
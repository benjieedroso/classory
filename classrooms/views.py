from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ClassroomForm
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.hashers import make_password
from .models import Classroom
from django.http import HttpResponse

#Excel handling
from io import BytesIO
from openpyxl import Workbook


import pandas as pd
# Mock data — no models yet, just for UI demonstration
MOCK_CLASSROOMS = [
    {
        "id": 1,
        "name": "Mathematics 101",
        "description": "Introduction to algebra, geometry and problem solving.",
        "teacher": "Mr. Alan Reyes",
        "students": 32,
        "subject": "Mathematics",
        "color": "blue",
    },
    {
        "id": 2,
        "name": "Science Explorers",
        "description": "Hands-on experiments covering physics, chemistry and biology.",
        "teacher": "Ms. Bella Cruz",
        "students": 28,
        "subject": "Science",
        "color": "yellow",
    },
    {
        "id": 3,
        "name": "English Literature",
        "description": "Reading, writing and analysing classic and modern texts.",
        "teacher": "Mr. Carlo Santos",
        "students": 30,
        "subject": "English",
        "color": "blue",
    },
]

# Mock student scores — only the current student sees their own
MOCK_STUDENT_SCORES = {
    "name": "Juan Dela Cruz",
    "section": "Grade 7 — Rizal",
    "scores": [
        {"test": "Quiz 1", "score": 18, "total": 20, "date": "Sep 15, 2026"},
        {"test": "Quiz 2", "score": 15, "total": 20, "date": "Sep 22, 2026"},
        {"test": "Assignment 1", "score": 45, "total": 50, "date": "Sep 28, 2026"},
        {"test": "Midterm Exam", "score": 88, "total": 100, "date": "Oct 5, 2026"},
    ],
}


@login_required
def dashboard_view(request):
    """Lists every classroom the logged-in user belongs to."""
    classrooms = Classroom.objects.all()  # In a real app, filter by user
    return render(request, "classrooms/dashboard.html", {"classrooms": classrooms})

@login_required
def create_classroom_view(request):
    """Teacher-only: create a classroom and import students from Excel."""
    
    if request.method == "POST":
        classroom_form = ClassroomForm(request.POST, request.FILES)
        if classroom_form.is_valid():
            # In a real app, save the classroom and handle the Excel file here
            df = pd.read_excel(request.FILES['excel_file']) if 'excel_file' in request.FILES else None
            
            data = df.to_dict(orient='records') if df is not None else []
            
            num_students = len(data)
            
            classroom = classroom_form.save(commit=False)
            classroom.students = num_students
            classroom.teacher = request.user.userprofile  # Assuming the logged-in user is a teacher
            classroom.save()
            
            
            for student in data:
                user = User.objects.create_user(
                    username=student['First Name'].lower() + student['Last Name'].lower(),
                    first_name=student['First Name'],
                    last_name=student['Last Name'],
                    email='',
                    password=make_password(student['Password'])  # Ensure to hash the password
                )
                UserProfile.objects.create(
                    user=user,
                    role='student',
                    section=student['Section'],
                    classroom=classroom
                )
            
            
            return redirect("classrooms:dashboard")
    
    
    
        
    return render(request, "classrooms/create_classroom.html")


def classroom_home_view(request, classroom_id):
    """The inside-classroom page — same UI for students and teachers."""
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom is None:
        return redirect("classrooms:dashboard")
    return render(request, "classrooms/classroom_home.html", {"classroom": classroom})


def upload_scores_view(request, classroom_id):
    """Teacher uploads an Excel file with student scores."""
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom is None:
        return redirect("classrooms:dashboard")

    if request.method == "POST":
        # In a real app, process the Excel file here
        return redirect("classrooms:upload_done", classroom_id=classroom_id)

    return render(request, "classrooms/upload_scores.html", {"classroom": classroom})


def upload_done_view(request, classroom_id):
    """Shows a success notification after score upload."""
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom is None:
        return redirect("classrooms:dashboard")
    return render(request, "classrooms/upload_done.html", {"classroom": classroom})


def student_scores_view(request, classroom_id):
    """Student sees their own scores only."""
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom is None:
        return redirect("classrooms:dashboard")
    return render(request, "classrooms/student_scores.html", {
        "classroom": classroom,
        "student": MOCK_STUDENT_SCORES,
    })

def build_excel_template(classroom):
    """Builds an Excel template with student IDs, names, and empty score column."""
    # In a real app, fetch students from the database
    
    
    df = pd.DataFrame(students)
    df["Score"] = ""  # Add an empty score column
    
    return df

def download_scores_view(request, classroom_id):
    """Download an Excel template with student IDs, names, and empty score column."""
    
    students = UserProfile.objects.filter(classroom_id=classroom_id, role='student').values('id', 'user__first_name', 'user__last_name')
    
    #Create an excel
    wb = Workbook()
    ws = wb.active
    
    ws.title = "Student Scores Template"
    
    headers = ["Student ID", "First Name", "Last Name", "Score"]
    ws.append(headers)
    
    for student in students:
        ws.append(
            [student['id'], student['user__first_name'], student['user__last_name'], ""]
        )
        
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    filename = f"Student Scores Template - Classroom {classroom_id}.xlsx"
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'  
    
    return response
    
    
    
    
    
    

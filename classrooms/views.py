from django.shortcuts import redirect, render
from .forms import CreateClassroomForm, UploadScoresForm


def dashboard_view(request):
    return render(request, "classrooms/dashboard.html", {"classrooms": []})


def create_classroom_view(request):
    return render(request, "classrooms/create_classroom.html", {"form": CreateClassroomForm()})


def classroom_home_view(request, classroom_id):
    classroom = {"id": classroom_id, "name": ""}
    return render(request, "classrooms/classroom_home.html", {"classroom": classroom})


def upload_scores_view(request, classroom_id):
    classroom = {"id": classroom_id, "name": ""}
    return render(request, "classrooms/upload_scores.html", {
        "classroom": classroom,
        "form": UploadScoresForm(),
    })


def upload_done_view(request, classroom_id):
    classroom = {"id": classroom_id, "name": ""}
    return render(request, "classrooms/upload_done.html", {"classroom": classroom})


def student_scores_view(request, classroom_id):
    classroom = {"id": classroom_id, "name": ""}
    student = {"name": "", "section": "", "scores": []}
    return render(request, "classrooms/student_scores.html", {
        "classroom": classroom,
        "student": student,
    })


def download_scores_view(request, classroom_id):
    return redirect("classrooms:home", classroom_id=classroom_id)

from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm, ProfileSetupStudentForm, ProfileSetupTeacherForm


def home(request):
    """Landing page — renders the login screen."""
    return render(request, "accounts/login.html", {"form": LoginForm()})


def login_view(request):
    return render(request, "accounts/login.html", {"form": LoginForm()})


def logout_view(request):
    return redirect("accounts:login")


def register_view(request):
    return render(request, "accounts/register.html", {"form": RegisterForm()})


def profile_setup_view(request, user_id):
    role = request.GET.get("role", "student")
    form = ProfileSetupTeacherForm() if role == "teacher" else ProfileSetupStudentForm()
    return render(request, "accounts/profile_setup.html", {
        "form": form,
        "role": role,
        "user_id": user_id,
    })


def register_done_view(request, role):
    if role == "teacher":
        return redirect("classrooms:create")
    return redirect("classrooms:dashboard")

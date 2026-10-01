from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, ProfileSetupStudent, ProfileSetupTeacher
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import logout, login


def home(request):
    """Landing page — sends everyone to the login screen."""
    return render(request, "accounts/login.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect("classrooms:dashboard")

    return render(request, "accounts/login.html")

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    # In a real application, you would use Django's logout function here.
    
    logout(request)
    return redirect("accounts:login")


def register_view(request):
    
    role = request.GET.get("role", "student")
    
    if request.method == "POST":
        user_reg_form = UserRegistrationForm(request.POST)
        if user_reg_form.is_valid():
            new_user = user_reg_form.save(commit=False)
            new_user.set_password(user_reg_form.cleaned_data["password"])
            new_user.role = user_reg_form.cleaned_data["role"]
            new_user.save()
            new_user_profile = UserProfile.objects.get_or_create(user=new_user, role=new_user.role)
            new_user_id = new_user.id
            return redirect("accounts:profile_setup", user_id=new_user_id)  # Redirect to register_done_view
  
    return render(request, "accounts/register.html")


def profile_setup_view(request, user_id):
    """Shown right after registration.

    Students fill in first name, last name and section.
    Teachers fill in first name and last name, then are sent to
    classroom creation.
    """
    user = User.objects.get(id=user_id)
    role = user.userprofile.role  # Assuming you have a UserProfile model linked to User
    
    if role == "student":
        if request.method == "POST":
            user_student_form = ProfileSetupStudent(request.POST, instance=user)
            if user_student_form.is_valid():
                user_student_form.save()
                return redirect("accounts:register_done", role=role)  # Redirect to register_done_view
        else:
            user_student_form = ProfileSetupStudent(instance=user)
        return render(request, "accounts/profile_setup.html", {"form": user_student_form, "role": role, "user": user})
    elif role == "teacher":
        if request.method == "POST":
            user_teacher_form = ProfileSetupTeacher(request.POST, instance=user)
            if user_teacher_form.is_valid():
                user_teacher_form.save()
                return redirect("accounts:register_done", role=role)  # Redirect to register_done_view
        else:
            user_teacher_form = ProfileSetupTeacher(instance=user)
        return render(request, "accounts/profile_setup.html", {"form": user_teacher_form, "role": role, "user": user})
    
    return render(request, "accounts/profile_setup.html", {"role": role, "user": user})


    


def register_done_view(request, role):
    """Decides where to send the user after profile setup."""
    if role == "teacher":
        return redirect("classrooms:create")
    return redirect("classrooms:dashboard")

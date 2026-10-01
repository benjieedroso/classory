from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile-setup/<int:user_id>/", views.profile_setup_view, name="profile_setup"),
    path("register-done/<str:role>/", views.register_done_view, name="register_done"),
]

from django.urls import path
from . import views

app_name = "classrooms"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("create/", views.create_classroom_view, name="create"),
    path("<int:classroom_id>/", views.classroom_home_view, name="home"),
    path("<int:classroom_id>/upload-scores/", views.upload_scores_view, name="upload_scores"),
    path("<int:classroom_id>/upload-done/", views.upload_done_view, name="upload_done"),
    path("<int:classroom_id>/scores/", views.student_scores_view, name="student_scores"),
    path("<int:classroom_id>/download/", views.download_scores_view, name="download_scores"),
]

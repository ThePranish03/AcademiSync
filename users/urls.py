from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("create-school/", views.create_school, name="create_school"),
    path("join-batch/", views.join_batch, name="join_batch"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer-dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("upload-material/<int:batch_id>/", views.upload_material, name="upload_material"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
     path("student-assignments/", views.student_assignments, name="student_assignments"),
    path("submit-assignment/<int:assignment_id>/", views.submit_assignment, name="submit_assignment"),
]

from django.urls import path
from . import views
from .views import upload_study_material, view_study_materials, submit_assignment, view_assignments
from .views import grade_assignment, enroll_trainer, enroll_student

urlpatterns = [
    path("", views.home, name="home"),  # Home Page
    path("select-role/", views.select_role, name="select_role"),  # Role Selection
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),  # Admin Page
    path("create-school/", views.create_school, name="create_school"),  # Create School
    path("view-schools/", views.view_schools, name="view_schools"),  # Display Existing Schools
    path("trainer-enroll/", views.trainer_enroll, name="trainer_enroll"),  # Trainer Enrollment
    path("student-enroll/", views.student_enroll, name="student_enroll"),  # Student Enrollment
    path("enroll-trainer/", views.enroll_trainer, name="enroll_trainer"),
    path("enroll-student/", views.enroll_student, name="enroll_student"),
    path("upload-study-material/", upload_study_material, name="upload_study_material"),
    path("view-study-materials/", view_study_materials, name="view_study_materials"),
    path("submit-assignment/", submit_assignment, name="submit_assignment"),
    path("view-assignments/", view_assignments, name="view_assignments"),
    path("grade-assignment/<int:assignment_id>/", views.grade_assignment, name="grade_assignment"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_signup/", views.admin_signup, name="admin_logout"),
]
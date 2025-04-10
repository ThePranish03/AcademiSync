from django.urls import path
from . import views
from .views import   submit_assignment, view_assignments
from .views import grade_assignment, enroll_trainer, enroll_student
from .views import upload_materials, view_study_materials, submit_assignment, view_assignments


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
    path("upload-material/", upload_materials, name="upload_material"),
    path("submit_assignment/", submit_assignment, name="submit_assignment"),
    path("view_assignments/", view_assignments, name="view_assignments"),
    path("grade_assignment/<int:assignment_id>/", views.grade_assignment, name="grade_assignment"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_signup/", views.admin_signup, name="admin_signup"),
]
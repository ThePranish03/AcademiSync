from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import string
from .models import School, Batch, Trainer, Student
from django.db import IntegrityError
from django.shortcuts import render
from .models import Batch

# Home Page
def home(request):
    return render(request, "home.html")

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def select_role(request):
    if request.method == "POST":
        role = request.POST.get("role")

        if role == "admin":
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to continue as an Admin.")
                return redirect("admin_login")  # Redirect to login page
            
            # Check if user is an admin
            if not request.user.is_staff:
                messages.error(request, "Only admins can access this section.")
                return redirect("home")

            return redirect("admin_dashboard")

        elif role == "trainer":
            return redirect("enroll_trainer")

        elif role == "student":
            return redirect("enroll_student")

    return render(request, "select_role.html")

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def admin_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Only allow staff (admins)
                login(request, user)
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Only admins can log in here.")
        else:
            messages.error(request, "Invalid credentials!")

    else:
        form = AuthenticationForm()
    
    return render(request, "admin_login.html", {"form": form})

from django.contrib.auth.models import User
from django.core.mail import send_mail  # Optional for email notifications

def admin_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_staff = False  # New admins need approval
        user.save()

        # Notify existing admins (optional)
        send_mail(
            "New Admin Request",
            f"A new admin {username} has registered. Approve them in the admin panel.",
            "your-email@example.com",
            ["admin@example.com"],  # Replace with actual admin emails
            fail_silently=True,
        )

        messages.success(request, "Admin sign-up request sent. Wait for approval.")
        return redirect("home")

    return render(request, "admin_signup.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Only admins can view this page.")
        return redirect("home")  # Redirect non-admins to home
    
    return render(request, "admin_dashboard.html")

import uuid
def generate_unique_batch_code():
    return str(uuid.uuid4())[:8]

def create_school(request):
    if request.method == "POST":
        batch_code = generate_unique_batch_code()

        # Ensure uniqueness by regenerating if code already exists
        while Batch.objects.filter(code=batch_code).exists():
            batch_code = generate_unique_batch_code()

        batch = Batch(code=batch_code)  
        batch.save()

        return render(request, "success.html", {"message": f"School created! Batch Code: {batch_code}"})

    return render(request, "create_school.html") 

# View Existing Schools
def view_schools(request):
    schools = School.objects.all()
    batches = Batch.objects.all()
    return render(request, "view_schools.html", {"schools": schools, "batches": batches})

# Trainer Enrollment
def trainer_enroll(request):
    if request.method == "POST":
        entered_code = request.POST["class_code"]
        batch = Batch.objects.filter(teacher_code=entered_code).first()
        if batch:
            return HttpResponse("Trainer enrolled successfully!")
        else:
            return HttpResponse("Invalid class code!")

    return render(request, "trainer_enroll.html")

# Student Enrollment
def student_enroll(request):
    if request.method == "POST":
        entered_code = request.POST["class_code"]
        batch = Batch.objects.filter(student_code=entered_code).first()
        if batch:
            return HttpResponse("Student enrolled successfully!")
        else:
            return HttpResponse("Invalid class code!")

    return render(request, "student_enroll.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Batch, Trainer, Student

def enroll_trainer(request):
    if request.method == "POST":
        code = request.POST.get("trainer_code")
        try:
            batch = Batch.objects.get(trainer_code=code)
            trainer, created = Trainer.objects.get_or_create(user=request.user)
            trainer.batch = batch
            trainer.save()
            messages.success(request, "You have successfully enrolled as a trainer!")
            return redirect("trainer_dashboard")
        except Batch.DoesNotExist:
            messages.error(request, "Invalid trainer code!")
    return render(request, "enroll_trainer.html")

def enroll_student(request):
    if request.method == "POST":
        code = request.POST.get("student_code")
        try:
            batch = Batch.objects.get(student_code=code)
            student, created = Student.objects.get_or_create(user=request.user)
            student.batch = batch
            student.save()
            messages.success(request, "You have successfully enrolled as a student!")
            return redirect("student_dashboard")
        except Batch.DoesNotExist:
            messages.error(request, "Invalid student code!")
    return render(request, "enroll_student.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudyMaterial, Assignment, Trainer, Student, Batch
from .forms import StudyMaterialForm, AssignmentForm,GradeAssignmentForm

@login_required
def upload_study_material(request):
    trainer = Trainer.objects.filter(user=request.user).first()
    if not trainer or not trainer.batch:
        messages.error(request, "You must be enrolled as a trainer to upload materials!")
        return redirect("trainer_dashboard")
    
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.batch = trainer.batch
            material.save()
            messages.success(request, "Study material uploaded successfully!")
            return redirect("trainer_dashboard")
    else:
        form = StudyMaterialForm()
    
    return render(request, "upload_study_material.html", {"form": form})

@login_required
def view_study_materials(request):
    student = Student.objects.filter(user=request.user).first()
    if not student or not student.batch:
        messages.error(request, "You must be enrolled as a student to view materials!")
        return redirect("student_dashboard")
    
    materials = StudyMaterial.objects.filter(batch=student.batch)
    return render(request, "view_study_materials.html", {"materials": materials})

@login_required
def submit_assignment(request):
    student = Student.objects.filter(user=request.user).first()
    if not student or not student.batch:
        messages.error(request, "You must be enrolled as a student to submit assignments!")
        return redirect("student_dashboard")
    
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.batch = student.batch
            assignment.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect("student_dashboard")
    else:
        form = AssignmentForm()
    
    return render(request, "submit_assignment.html", {"form": form})

@login_required
def view_assignments(request):
    trainer = Trainer.objects.filter(user=request.user).first()
    if not trainer or not trainer.batch:
        messages.error(request, "You must be enrolled as a trainer to view assignments!")
        return redirect("trainer_dashboard")
    
    assignments = Assignment.objects.filter(batch=trainer.batch)
    return render(request, "view_assignments.html", {"assignments": assignments})

@login_required
def grade_assignment(request, assignment_id):
    trainer = Trainer.objects.filter(user=request.user).first()
    if not trainer or not trainer.batch:
        messages.error(request, "You must be enrolled as a trainer to grade assignments!")
        return redirect("trainer_dashboard")

    assignment = Assignment.objects.get(id=assignment_id, batch=trainer.batch)
    
    if request.method == "POST":
        form = GradeAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment graded successfully!")
            return redirect("view_assignments")
    else:
        form = GradeAssignmentForm(instance=assignment)

    return render(request, "grade_assignment.html", {"form": form, "assignment": assignment})


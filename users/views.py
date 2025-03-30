from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import string
from .models import School, Batch, Trainer, Student
from django.db import IntegrityError
from django.shortcuts import render
from .models import Batch
from django.contrib.auth import get_user_model


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
        form = AuthenticationForm(request, data=request.POST)  # Ensure request is passed

        if form.is_valid():
            user = form.get_user()
            
            if user.is_staff:  # Check if the user is an admin
                login(request, user)
                messages.success(request, f"Welcome, {user.username}! Login successful!")
                return redirect("admin_dashboard")  # Redirect to the admin dashboard
            
            else:
                messages.error(request, "Only admins can log in here.")
        
        else:
            messages.error(request, "Invalid credentials!")

    else:
        form = AuthenticationForm()

    return render(request, "admin_login.html", {"form": form})

from django.contrib.auth.models import User
from django.core.mail import send_mail  # Optional for email notifications

CustomUser = get_user_model()  # Get the custom user model

def admin_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect("admin_signup")

        # Check if the email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect("admin_signup")

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.is_admin = True  # If you have an admin flag
        user.save()

        messages.success(request, "Admin account created successfully! You can now log in.")
        return redirect("admin_login")  # Redirect to login page

    return render(request, "admin_signup.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Only admins can view this page.")
        return redirect("home")  # Redirect non-admins to home
    
    return render(request, "admin_dashboard.html")

def generate_unique_code(model, field_name):
    while True:
        unique_code = str(uuid.uuid4().hex[:8])
        if not model.objects.filter(**{field_name: unique_code}).exists():
            return unique_code

def create_school(request):
    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()  # ✅ Save school first

            num_classes = school.num_classes
            for i in range(1, num_classes + 1):
                Batch.objects.create(
                    school=school,
                    class_name=f"Class {i}",
                    name=f"Batch {i}",
                    teacher_code=str(uuid.uuid4())[:8],  # ✅ Generate unique trainer code
                    student_code=str(uuid.uuid4())[:8],  # ✅ Generate unique student code
                    code=str(uuid.uuid4())[:8],  # ✅ Ensure batch code is unique
                    class_number=i
                )

            messages.success(request, "School and batches created successfully!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid data provided!")

    else:
        form = SchoolForm()

    return render(request, "create_school.html", {"form": form})

def view_schools(request):
    schools = School.objects.all()
    batches = Batch.objects.all()

    school_data = []

    for school in schools:
        related_batches = batches.filter(school=school)

        batch_details = [
            {
                "batch_name": batch.name,  # ✅ Use 'name' instead of 'batch_name'
                "class_name": batch.class_name,  # ✅ Correct field
                "teacher_code": batch.teacher_code,
                "student_code": batch.student_code,
                "class_number": batch.class_number,
            }
            for batch in related_batches
        ]

        school_data.append({
            "school_name": school.college_name,
            "college_code": school.college_code,
            "num_classes": school.num_classes,
            "batches": batch_details,
        })

    return render(request, "view_schools.html", {"school_data": school_data})


# Trainer Enrollment
def trainer_enroll(request):
    if request.method == "POST":
        entered_code = request.POST["class_code"]
        batch = Batch.objects.filter(teacher_code=entered_code).first()
        if batch:
            return render(request, "upload_materials.html", {"batch": batch})
        else:
            return HttpResponse("Invalid class code!")

    return render(request, "trainer_enroll.html")

# Student Enrollment
def student_enroll(request):
    if request.method == "POST":
        entered_code = request.POST["class_code"]
        batch = Batch.objects.filter(student_code=entered_code).first()
        if batch:
            return render(request,"view_assignments.html",{"batch":batch})
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
from .forms import SchoolForm
import uuid

@login_required
def upload_materials(request):
    trainer_batch = Batch.objects.filter(trainer=request.user).first()  
    if not trainer_batch:
        messages.error(request, "You are not assigned to any batch.")
        return redirect('dashboard')

    study_materials = StudyMaterial.objects.filter(batch=trainer_batch)
    assignments = Assignment.objects.filter(batch=trainer_batch)

    if request.method == "POST":
        if "submit_study" in request.POST:
            study_form = StudyMaterialForm(request.POST, request.FILES)
            if study_form.is_valid():
                study_material = study_form.save(commit=False)
                study_material.batch = trainer_batch
                study_material.save()
                messages.success(request, "Study material uploaded successfully!")
                return redirect('upload_materials')

        elif "submit_assignment" in request.POST:
            assignment_form = AssignmentForm(request.POST, request.FILES)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.batch = trainer_batch
                assignment.save()
                messages.success(request, "Assignment uploaded successfully!")
                return redirect('upload_materials')

    else:
        study_form = StudyMaterialForm()
        assignment_form = AssignmentForm()

    return render(request, "upload_materials.html", {
        "study_form": study_form,
        "assignment_form": assignment_form,
        "study_materials": study_materials,
        "assignments": assignments
    })


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
    user = request.user
    
    # Check if user is a student or trainer
    if hasattr(user, 'student'):
        batch = user.student.batch  # Student's batch
    elif hasattr(user, 'trainer'):
        batch = user.trainer.batch  # Trainer's batch
    else:
        batch = None

    if batch:
        assignments = Assignment.objects.filter(batch=batch)
        study_materials = StudyMaterial.objects.filter(batch=batch)
    else:
        assignments = []
        study_materials = []

    return render(request, "view_assignment.html", {
        "assignments": assignments,
        "study_materials": study_materials
    })

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


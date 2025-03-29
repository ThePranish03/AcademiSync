from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import School, Batch, Enrollment, Assignment
from .forms import CustomUserCreationForm, SchoolForm, BatchJoinForm, StudyMaterialForm, AssignmentSubmissionForm

def home(request):
    return render(request, "users/home.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def create_school(request):
    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.admin = request.user
            school.save()
            return redirect("dashboard")
    else:
        form = SchoolForm()
    return render(request, "users/create_school.html", {"form": form})

from django.http import HttpResponse

def join_batch(request):
    if request.method == "POST":
        form = BatchJoinForm(request.POST)
        if form.is_valid():
            batch_code = form.cleaned_data["batch_code"]
            try:
                batch = Batch.objects.get(teacher_code=batch_code) or Batch.objects.get(student_code=batch_code)
                Enrollment.objects.create(user=request.user, batch=batch)
                return redirect("dashboard")
            except Batch.DoesNotExist:
                return HttpResponse("Invalid Code. Try Again.")

    else:
        form = BatchJoinForm()

    return render(request, "users/join_batch.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return HttpResponse("Unauthorized", status=403)

    school = School.objects.filter(admin=request.user).first()
    batches = Batch.objects.filter(school=school) if school else None

    return render(request, "users/admin_dashboard.html", {"school": school, "batches": batches})

@login_required
def trainer_dashboard(request):
    if request.user.role != "trainer":
        return HttpResponse("Unauthorized", status=403)

    enrollments = Enrollment.objects.filter(user=request.user)
    batches = [enrollment.batch for enrollment in enrollments]

    return render(request, "users/trainer_dashboard.html", {"batches": batches})

@login_required
def upload_material(request, batch_id):
    if request.user.role != "trainer":
        return HttpResponse("Unauthorized", status=403)

    batch = Batch.objects.get(id=batch_id)

    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.trainer = request.user
            material.batch = batch
            material.save()
            return redirect("trainer_dashboard")

    else:
        form = StudyMaterialForm()

    return render(request, "users/upload_material.html", {"form": form, "batch": batch})

@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponse("Unauthorized", status=403)

    enrollments = Enrollment.objects.filter(user=request.user)
    batches = [enrollment.batch for enrollment in enrollments]
    materials = StudyMaterialForm.objects.filter(batch__in=batches)

    return render(request, "users/student_dashboard.html", {"batches": batches, "materials": materials})

@login_required
def student_assignments(request):
    if request.user.role != "student":
        return HttpResponse("Unauthorized", status=403)

    enrollments = Enrollment.objects.filter(user=request.user)
    batches = [enrollment.batch for enrollment in enrollments]
    assignments = Assignment.objects.filter(batch__in=batches)

    return render(request, "users/student_assignments.html", {"assignments": assignments})

@login_required
def submit_assignment(request, assignment_id):
    if request.user.role != "student":
        return HttpResponse("Unauthorized", status=403)

    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == "POST":
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            return redirect("student_assignments")

    else:
        form = AssignmentSubmissionForm()

    return render(request, "users/submit_assignment.html", {"form": form, "assignment": assignment})

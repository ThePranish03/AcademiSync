import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps
from django.conf import settings

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

# School Model
class School(models.Model):
    college_code = models.CharField(max_length=20, unique=True)
    college_name = models.CharField(max_length=255)
    num_classes = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.num_classes > 60:
            raise ValueError("A school can have a maximum of 60 classes.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.college_name

# Batch Model
class Batch(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="batches")
    class_name = models.CharField(max_length=100)
    teacher_code = models.CharField(max_length=10, unique=True, editable=False)
    student_code = models.CharField(max_length=10, unique=True, editable=False)
    class_number = models.IntegerField(default=1)  # Ensure this field exists
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    class Meta:
        verbose_name_plural = "batches"

    def save(self, *args, **kwargs):
        if not self.teacher_code:
            self.teacher_code = str(uuid.uuid4())[:8]  # Unique 8-char code
        if not self.student_code:
            self.student_code = str(uuid.uuid4())[:8]  # Unique 8-char code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_name} - {self.school.college_name}"

# Enrollment Model
class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enrollments")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="enrolled_users")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.batch.class_name}"


def get_assignment_submission_model():
    return apps.get_model('users', 'AssignmentSubmission')

class Trainer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch = models.ForeignKey('Batch', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch = models.ForeignKey('Batch', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class StudyMaterial(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="study_materials/")

    def __str__(self):
        return self.title

class Assignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="assignments/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(null=True, blank=True)  # or models.CharField()
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Assignment by {self.student.username} for {self.batch.name}"

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment}"

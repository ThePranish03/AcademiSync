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
    class_number = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, editable=False)  # ✅ Unique batch code

    def save(self, *args, **kwargs):
        # ✅ Generate unique codes if they don't exist
        if not self.teacher_code:
            self.teacher_code = str(uuid.uuid4())[:8]  # 8-character trainer code
        if not self.student_code:
            self.student_code = str(uuid.uuid4())[:8]  # 8-character student code
        if not self.code:
            self.code = str(uuid.uuid4())[:8]  # ✅ Unique batch code
        
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
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='assignments/')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, blank=True, null=True)  # New field
    feedback = models.TextField(blank=True, null=True)  # New field


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment}"

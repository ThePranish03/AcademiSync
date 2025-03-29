from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import School
from users.models import AssignmentSubmission, StudyMaterial
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['college_code', 'college_name', 'num_classes']

class BatchJoinForm(forms.Form):
    batch_code = forms.CharField(max_length=10, label="Enter Class Code")

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ["title", "file"]

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ["file"]

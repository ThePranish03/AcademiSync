from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, School
from users.models import AssignmentSubmission, StudyMaterial

# Form for creating a custom user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

# Form for managing school details
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['college_code', 'college_name', 'num_classes']

# Form for joining a batch using a batch code
class BatchJoinForm(forms.Form):
    batch_code = forms.CharField(max_length=10, label="Enter Class Code")

# Form for uploading study materials
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ["title", "file"]

# Form for submitting assignments
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ["file"]

from django import forms
from .models import StudyMaterial, Assignment

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ["title", "file"]

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["file"]

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["grade", "feedback"]

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect based on role
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  
    return render(request, 'login.html')

def home(request):  
    return render(request, 'users/home.html')


def dashboard(request):
    return render(request, 'dashboard.html')  

from django.shortcuts import render
from .models import Document
from .forms import DocumentForm

def upload_file(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves to Cloudinary
    else:
        form = DocumentForm()
    
    documents = Document.objects.all()  # Get all uploaded files
    return render(request, "upload.html", {"form": form, "documents": documents})

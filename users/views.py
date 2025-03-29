from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .forms import StudyMaterialForm, AssignmentForm

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

# def sample(request):
#     render(request, 'sample.html', {})


def home(request):  
    return render(request, 'users/home.html',{})


from django.template.loader import get_template
from django.http import HttpResponse

def template_test(request):
    try:
        template = get_template('users/home.html')
        return HttpResponse("Template found!")
    except:
        return HttpResponse("Template NOT found", status=500)

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib import messages
# from .models import StudentProfile
# from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from .forms import StudentProfileForm, CompanyProfileForm
from django.urls import reverse
import requests
from django.contrib.auth.decorators import login_required


def internship(request):
    return HttpResponseRedirect('http://127.0.0.1:5000/dashboard')

def posts(request):
    return HttpResponseRedirect('http://127.0.0.1:5000/company_dashboard')

def index1(request):
    username = request.GET.get('username', 'User')  # Default to 'User' if not provided
    role = request.GET.get('role', 'student')  # Default to 'student'
    return render(request, 'job_portal/index1.html', {'username': username, 'role': role})

def index2(request):
    username = request.GET.get('username', 'User')  # Default to 'User' if not provided
    role = request.GET.get('role', 'company')  # Default to 'company'
    return render(request, 'job_portal/index2.html', {'username': username, 'role': role})


def login_view(request):
    return  HttpResponseRedirect('http://127.0.0.1:5000/login')

def profile(request):
    return render(request, 'job_portal/profile1.html')

# def job(request):
#     return  HttpResponseRedirect('http://127.0.0.1:5000/dashboard')
#
# def post(request):
#     return  HttpResponseRedirect('http://127.0.0.1:5000/company_dashboard')

def candidate_registration(request):
    return HttpResponseRedirect('http://127.0.0.1:5000/signup')

def profile_success(request):
    return render(request, 'job_portal/profile_success.html')

def login_success(request):
    return render(request, 'job_portal/login_success.html')

def subscription(request):
    return HttpResponseRedirect('http://127.0.0.1:5000/subscribe')

# def candidate_registration(request):
#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registration successful!")
#             return redirect('profile_success')  # Replace with the name of the success URL
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = StudentProfileForm()
#
#     return render(request, 'job_portal/candidate_reg.html', {'form': form})
#
#
# class AdminLogin(LoginView):
#     template_name = 'job_portal/admin_login.html'
#
#
#     def form_valid(self, form):
#         user = form.get_user()
#         if user.is_authenticated:
#             if user.is_superuser:
#                 return redirect('/admin/')
#
#         return super().form_valid(form)


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         role = request.POST.get("role")
#
#         # Authenticate user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if role == "student":
#                 return redirect("login_success")  # Redirect to student dashboard
#             elif role == "employer":
#                 return redirect("login_success")  # Redirect to employer dashboard
#         else:
#             messages.error(request, "Invalid username or password")
#
#     return render(request, "job_portal/login.html")

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'job_portal/index.html')

# class Index1(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'job_portal/index1.html')

# def company_signup(request):
#     if request.method == 'POST':
#         form = CompanyProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Company profile has been created successfully!")
#             return redirect('profile_success')
#         else:
#             messages.error(request, "There were errors in your submission. Please correct them.")
#     else:
#         form = CompanyProfileForm()
#     return render(request, 'job_portal/employer_reg.html', {'form': form})




















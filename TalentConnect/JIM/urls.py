"""
URL configuration for JIM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin
from job_portal.views import  Index
from django.conf import settings
from django.conf.urls.static import static
from job_portal.views import candidate_registration, internship, profile_success, login_view, login_success, subscription, posts, index1, index2
from internship.views import student_form, organization_form_view

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('index1/', index1, name='index1'),
    path('index2/', index2, name='index2'),
    path('admin/',admin.site.urls),
    # path('admin-login/', AdminLogin.as_view(), name='admin_login'),
    path('create-profile/', candidate_registration, name='create_profile'),
    path('profile-success/', profile_success, name='profile_success'),
    # path('signup/', company_signup, name='company_signup'),
    path("login/", login_view, name="login"),
    path("login_success/", login_success, name="login_success"),
    # path('internship/', include('internship.urls')),
    path('intern/', internship, name='intern'),
    path('subscribe/', subscription, name='subscribe'),
    path('post/', posts, name='post'),
    path('profile/', student_form, name='profile'),
    path('employer/', organization_form_view, name='employer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
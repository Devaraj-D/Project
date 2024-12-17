from django.db import models

class StudentProfile(models.Model):
    # Basic Details
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = models.DateField()

    # Address
    door_no = models.CharField(max_length=10, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=10, null=True)

    # Education Qualification
    college = models.CharField(max_length=100, null=True)
    passing_year = models.IntegerField(null=True)
    qualification = models.CharField(max_length=100, null=True)
    percentage = models.FloatField(null=True)

    def __str__(self):
        return self.full_name

class Organization(models.Model):
    INDUSTRY_CHOICES = [
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('HR', 'Human Resources'),
        ('Marketing', 'Marketing'),
    ]

    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    number_of_employees = models.PositiveIntegerField()
    address = models.TextField()
    profile_image = models.ImageField(upload_to='organization_images/')
    website_url = models.URLField()
    business_registration_doc = models.FileField(upload_to='registration_docs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_name


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import StudentProfile, Organization
from django.http import HttpResponse

def student_form(request):
    if request.method == 'POST':
        # Extract data from POST request
        data = request.POST
        student_profile = StudentProfile(
            full_name=data.get('fullName'),
            email=data.get('email'),
            mobile=data.get('mobile'),
            gender=data.get('gender'),
            dob=data.get('dob'),
            door_no=data.get('doorNo'),
            street=data.get('street'),
            city=data.get('city'),
            state=data.get('state'),
            pincode=data.get('pincode'),
            college=data.get('college'),
            passing_year=data.get('passingYear'),
            qualification=data.get('qualification'),
            percentage=data.get('percentage')
        )
        student_profile.save()
        return JsonResponse({'message': 'Form submitted successfully!'})

    return render(request, 'internship/profile.html')



def organization_form_view(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name')
        employee_email = request.POST.get('employee_email')
        phone_number = request.POST.get('phone_number')
        industry_type = request.POST.get('industry_type')
        number_of_employees = request.POST.get('number_of_employees')
        address = request.POST.get('address')
        website_url = request.POST.get('website_url')
        profile_image = request.FILES.get('profile_image')
        business_registration_doc = request.FILES.get('business_registration_doc')

        # Save data to the model
        Organization.objects.create(
            employee_name=employee_name,
            employee_email=employee_email,
            phone_number=phone_number,
            industry_type=industry_type,
            number_of_employees=number_of_employees,
            address=address,
            profile_image=profile_image,
            website_url=website_url,
            business_registration_doc=business_registration_doc
        )
        return HttpResponse("Details submitted successfully!")
    return render(request, 'internship/employer.html')

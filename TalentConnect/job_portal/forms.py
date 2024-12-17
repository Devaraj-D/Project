# from django import forms
# from .models import StudentProfile, CompanyProfile
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User


# class StudentProfileForm(forms.ModelForm):
#     confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
#
#     class Meta:
#         model = StudentProfile
#         fields = ['name', 'email', 'mobile', 'gender', 'dob', 'stream', 'linkedin_url',
#                   'qualifications', 'skills', 'domain_preferences', 'cv', 'profile_image', 'password']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password != confirm_password:
#             raise ValidationError("The two password fields must match.")
#
#         return cleaned_data
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Clear default values by setting each field's initial value to None or empty
#         for field_name in self.fields:
#             if isinstance(self.fields[field_name], forms.fields.CharField):
#                 self.fields[field_name].initial = ''
#             elif isinstance(self.fields[field_name], forms.fields.DateField):
#                 self.fields[field_name].initial = None
#             elif isinstance(self.fields[field_name], forms.fields.ChoiceField):
#                 self.fields[field_name].initial = None
#             elif isinstance(self.fields[field_name], forms.ModelMultipleChoiceField):
#                 self.fields[field_name].initial = []
#             elif isinstance(self.fields[field_name], forms.FileField):
#                 self.fields[field_name].initial = None
#
#
# class CompanyProfileForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#
#     class Meta:
#         model = CompanyProfile
#         fields = [
#             'company_name', 'company_email', 'company_phone', 'industry', 'company_address',
#             'website_url', 'company_size', 'business_registration_document', 'profile_image', 'linkedin',
#             'password', 'confirm_password'
#         ]
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#
#         if password and confirm_password and password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data
#
#     def __init__(self, *args, **kwargs):
#         # Check if there's an instance and clear its data
#         kwargs['initial'] = {}  # Ensure no pre-populated initial data
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             # Reset each field's initial value explicitly
#             field.initial = ''















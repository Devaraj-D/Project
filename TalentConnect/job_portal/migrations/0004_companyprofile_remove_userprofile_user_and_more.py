# Generated by Django 4.2.16 on 2024-12-06 08:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0003_alter_studentprofile_domain_preferences_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(help_text='Enter the name of the company', max_length=200, unique=True)),
                ('company_email', models.EmailField(help_text='Enter the company email address', max_length=255, unique=True)),
                ('company_phone', models.CharField(help_text='Enter the company phone number', max_length=25)),
                ('industry', models.CharField(choices=[('IT', 'Information Technology'), ('FIN', 'Finance'), ('HR', 'Human Resources'), ('MKT', 'Marketing')], help_text='Select the industry the company belongs to', max_length=3)),
                ('company_address', models.TextField(help_text='Enter the company address')),
                ('website_url', models.URLField(blank=True, help_text="Enter the company's website URL", null=True)),
                ('company_size', models.IntegerField(help_text='Enter the number of employees in the company')),
                ('business_registration_document', models.FileField(blank=True, help_text="Upload the company's business registration document (PDF)", null=True, upload_to='company_documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('profile_image', models.ImageField(blank=True, help_text='Upload a profile image for the company', null=True, upload_to='company_images/')),
                ('linkedin', models.URLField(blank=True, help_text="Enter the company's LinkedIn URL", null=True)),
                ('twitter', models.URLField(blank=True, help_text="Enter the company's Twitter URL", null=True)),
            ],
            options={
                'verbose_name': 'Company Profile',
                'verbose_name_plural': 'Company Profiles',
            },
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

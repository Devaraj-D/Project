# Generated by Django 4.2.16 on 2024-12-15 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0007_rename_education_level_studentprofile_qualifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='institution_name',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='linkedin_url',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='qualifications',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='year_of_education',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='college',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='door_no',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='passing_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='percentage',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='pincode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='qualification',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

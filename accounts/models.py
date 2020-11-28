from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class Company(models.Model):
    company_name = models.CharField(max_length=100, default="")
    company_address = models.CharField(max_length=200, default="")
    company_password = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name


class User(AbstractUser):
    gender_choices = [
        ('Male', 'Erkek'),
        ('Female', 'Kadın')
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    bio = models.CharField(max_length=500, default='')
    gender = models.CharField(choices=gender_choices, max_length=10, default="male", null=True)
    city = models.CharField(max_length=20, default='')
    is_intern = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class InternUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    university = models.CharField(max_length=100)
    worked_day_count = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='accounts/images/', blank=True, null=True)
    own_projects = models.PositiveIntegerField(default=0)
    begin_of_internship = models.DateField(default=timezone.now().date())
    end_of_internship = models.DateField(default=timezone.now().date())
    company_id = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class EmployeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created_projects = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='accounts/images/', blank=True, null=True)
    company_id = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

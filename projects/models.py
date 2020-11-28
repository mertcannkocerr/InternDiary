from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from accounts.models import User, EmployeeUser, InternUser


class Project(models.Model):
    assigned_intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    assignee_employee = models.ForeignKey(EmployeeUser, on_delete=models.SET_NULL, null=True)
    assign_date = models.DateField(default=timezone.now().date())
    due_date = models.DateField(default=timezone.now().date())
    title = models.CharField(max_length=50, blank=True, default='')
    content = RichTextField(default='', blank=True)

    def __str__(self):
        return str(self.title)

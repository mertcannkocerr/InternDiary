from django.db import models
from django.utils import timezone
from accounts.models import User, EmployeeUser, InternUser
from ckeditor.fields import RichTextField


class WorkingDayRecord(models.Model):
    related_intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    text = RichTextField(default='', blank=True)
    date = models.DateField(default=timezone.now().date())
    enable = models.BooleanField(default=False)

    def is_enable(self):
        if self.enable:
            return True
        return False

    def __str__(self):
        return str(self.date) + " " + str(self.related_intern.user.username)

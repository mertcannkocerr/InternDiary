from django.contrib import admin
from .models import User, InternUser, EmployeeUser, Company


admin.site.register(User)
admin.site.register(InternUser)
admin.site.register(EmployeeUser)
admin.site.register(Company)

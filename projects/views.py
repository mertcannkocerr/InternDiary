import json

from .forms import CreateProjectForm, EditProjectForm
from .models import Project
from accounts.models import InternUser, EmployeeUser, User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View


# Only Employee Users can use this class
class ProjectHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):
        employee_user = EmployeeUser.objects.get(user_id=request.user.id)
        given_projects_by_employee = Project.objects.filter(assignee_employee_id=employee_user.id).order_by(
            '-due_date').reverse()

        args = {
            'employee_user': employee_user,
            'given_projects': given_projects_by_employee,
        }

        return render(request, 'projects/project_home_for_employee.html', args)

    def test_func(self):
        if not self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False


# Only Employee Users can use this class
class CreateProjectView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):

        all_interns = json.dumps(list(InternUser.objects.values_list('user__username', flat=True)))
        allInterns = InternUser.objects.all().filter(company_id=request.user.company.id)

        emp_user = get_object_or_404(EmployeeUser, user_id=request.user.id)
        create_project_form = CreateProjectForm(emp_user=emp_user)

        args = {
            'form': create_project_form,
            'all_interns': all_interns,
            'allInterns': allInterns,
            'emp_user': emp_user
        }
        return render(request, 'projects/create_project_for_employee.html', args)

    def post(self, request):

        emp_user = get_object_or_404(EmployeeUser, user_id=request.user.id)
        create_project_form = CreateProjectForm(request.POST, emp_user=emp_user)

        if create_project_form.is_valid():

            create_project_form.save(commit=False)

            if create_project_form.cleaned_data['assign_date'] > create_project_form.cleaned_data['due_date']:
                messages.error(request, "Invalid Dates Are Given.")
                return redirect('/projects/create')

            elif create_project_form.cleaned_data['assign_date'] < timezone.now().date():
                messages.error(request, "Invalid Assign Date Is Given.")
                return redirect('/projects/create')

            elif create_project_form.cleaned_data['due_date'] < timezone.now().date():
                messages.error(request, "Invalid Due Data Is Given")
                return redirect('/projects/create')

            else:
                create_project_form.save()

            assignee_employee = create_project_form.cleaned_data['assignee_employee']
            assignee_employee.created_projects += 1
            assignee_employee.save()

            assigned_intern = create_project_form.cleaned_data['assigned_intern']
            assigned_intern.own_projects += 1
            assigned_intern.save()

            messages.success(request, "Projeniz başarılı bir şekilde oluşturuldu.")
            return redirect('/projects')

        else:

            messages.error(request,
                           "Projeyi düzenlemeniz esnasında hata oluştu. Lütfen aşağıdaki her alanı doldurduğunuzdan"
                           " emin olun.".title().title())
            return redirect('/projects/create')

    def test_func(self):
        if not self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False


class EditProjectView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request, project_id):
        emp_user = get_object_or_404(EmployeeUser, user_id=request.user.id)
        all_project = Project.objects.filter(assignee_employee_id=emp_user.id)
        selected_project = get_object_or_404(Project, id=project_id)
        edit_project_form = EditProjectForm(emp_user=emp_user, instance=selected_project)
        all_interns = InternUser.objects.all().filter(company_id=request.user.company.id)
        last_intern = selected_project.assigned_intern

        args = {
            'form': edit_project_form,
            'all_interns': all_interns,
            'selected_project': selected_project,
            'emp_user': emp_user,
            'last_intern': last_intern
        }

        employees_project_ids = []
        for each_project in all_project:
            employees_project_ids.append(each_project.id)

        if project_id not in employees_project_ids:
            return redirect('/error/')

        return render(request, 'projects/edit_project.html', args)

    def post(self, request, project_id):
        emp_user = get_object_or_404(EmployeeUser, user_id=request.user.id)
        selected_project = get_object_or_404(Project, id=project_id)
        edit_project_form = EditProjectForm(request.POST, emp_user=emp_user, instance=selected_project)
        old_intern = selected_project.assigned_intern

        if edit_project_form.is_valid():
            edit_project_form.save(commit=False)

            if edit_project_form.cleaned_data['assign_date'] > edit_project_form.cleaned_data['due_date']:
                messages.warning(request, "Geçersiz tarih girişi yapıldı.".title())
                return redirect('/projects/edit/' + str(project_id))

            elif edit_project_form.cleaned_data['assign_date'] < timezone.now().date():
                messages.warning(request, "Girdiğiniz başlangıç tarihi geçersiz.".title())
                return redirect('/projects/edit/' + str(project_id))

            elif edit_project_form.cleaned_data['due_date'] < timezone.now().date():
                messages.warning(request, "Girdiğiniz Bitiş tarihi geçersiz.".title())
                return redirect('/projects/edit/' + str(project_id))
            else:
                edit_project_form.save()

            old_intern.own_projects -= 1
            old_intern.save()

            new_intern = edit_project_form.cleaned_data['assigned_intern']
            new_intern.own_projects += 1
            new_intern.save()

            messages.success(request, "Düzenlemeniz başarıyla kaydolmuştur")
            return redirect('/projects/')

        else:

            messages.error(request,
                           "Projeyi düzenlemeniz esnasında hata oluştu. Lütfen aşağıdaki her alanı doldurduğunuzdan emin olun.".title())

            return redirect('/projects/edit/' + str(project_id))

    def test_func(self):
        if not self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False


# Only Intern Users can use this class
class TakenProjectsView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):
        intern_user = InternUser.objects.get(user_id=request.user.id)
        taken_projects = Project.objects.filter(assigned_intern_id=intern_user.id).order_by('-due_date').reverse()

        args = {
            'intern_user': intern_user,
            'taken_projects': taken_projects
        }

        return render(request, 'projects/view_all_taken_projects_for_intern.html', args)

    def test_func(self):
        if self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        else:
            return False


# Only employee can delete projects
class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        assigned_intern = project.assigned_intern
        assigned_intern.own_projects -= 1
        assigned_intern.save()

        assignee_employee = project.assignee_employee
        assignee_employee.created_projects -= 1
        assignee_employee.save()

        if project.delete():
            pass
        else:
            messages.error(request, "Proje silmeniz esnasında bir hata oluştu.".title())

        return redirect('/projects/')

    def test_func(self):
        if not self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False

import operator

from .forms import DiaryUpdateForm
from .models import WorkingDayRecord
from accounts.models import InternUser
from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from operator import itemgetter


# Home Page for this app which is designed for both types of user.
class DiaryRecordsHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):

        # Interns should see their diary records for each day in this home page.
        # For avoiding superuser here we should check for if it is superuser or not

        if request.user.is_intern and not request.user.is_superuser:

            intern_user = get_object_or_404(InternUser, user_id=request.user.id)
            all_working_days = WorkingDayRecord.objects.filter(related_intern_id=intern_user.id).order_by('-date')

            current_date = timezone.now().date()
            wanted_working_days = []

            for record in all_working_days:
                if record.date == current_date or record.date < current_date:
                    wanted_working_days.append(record)

            args = {
                'user': request.user,
                'intern_user': intern_user,
                'Working_Day_Records': wanted_working_days,
                'today': current_date
            }

            return render(request, 'diaryRecords/diary_records_home.html', args)

        elif not request.user.is_intern and not request.user.is_superuser:

            all_interns = InternUser.objects.all().filter(company_id=request.user.company.id)
            sorted_interns_with_name = []

            # For clear view we should give elements in sorted order

            for intern in all_interns:
                each = []
                each.append(intern)
                all_name = intern.user.first_name + " " + intern.user.last_name
                each.append(all_name)
                sorted_interns_with_name.append(each)

            sorted_interns_with_name.sort(key=itemgetter(1))
            sorted_interns = []

            for each_list in sorted_interns_with_name:
                sorted_interns.append(each_list[0])

            today = timezone.now().date()

            args = {
                'today': today,
                'all_interns': sorted_interns,
            }

            return render(request, 'diaryRecords/diary_records_home.html', args)

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True


# Interns can make changes on allowed records
class RecordContentViewForIntern(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request, record_id):
        user = request.user
        intern_user = get_object_or_404(InternUser, user_id=request.user.id)
        all_records = WorkingDayRecord.objects.filter(related_intern_id=intern_user.id)
        selected_record = WorkingDayRecord.objects.get(id=record_id)
        today = timezone.now().date()

        interns_day_ids = []
        for each_record_id in all_records:
            interns_day_ids.append(each_record_id.id)

        if record_id not in interns_day_ids:
            return redirect('/error/')
        elif selected_record.date > today:
            return redirect('/error/')
        elif selected_record.date < today:
            return redirect('/error/')

        # Will give you a chance to show daily record only
        for record in all_records:
            if today == record.date:
                record.enable = True
                record.save()
            else:
                record.enable = False
                record.save()

        update_form = DiaryUpdateForm(instance=selected_record)

        args = {
            'user': user,
            'intern_user': intern_user,
            'record': selected_record,
            'form': update_form,
        }
        return render(request, 'diaryRecords/selected_diary_records_view_for_interns.html', args)

    def post(self, request, record_id):

        user = request.user
        intern_user = get_object_or_404(InternUser, user_id=request.user.id)
        all_records = WorkingDayRecord.objects.filter(related_intern_id=intern_user.id)
        current_record = WorkingDayRecord.objects.get(id=record_id)
        today = timezone.now().date()
        update_form = DiaryUpdateForm(request.POST, instance=current_record)

        if update_form.is_valid():
            messages.success(request, "Düzenlemeniz Başarı İle Kaydedildi.".title())
            update_form.save()
            return redirect('/diaryRecords/')
        else:

            messages.error(request,
                           "Düzenlemeniz esnasında hata oluştu. Lütfen bir kayıt girdiğinizden emin olun".title())
            args = {
                'messages': messages,
                'user': user,
                'intern_user': intern_user,
                'record': current_record,
                'form': update_form,
            }

            return render('diaryRecords/selected_diary_records_view_for_interns.html', args)

    def test_func(self):
        if self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False


# Employees could see all interns at homepage. After clicking on the specific intern
# app should show all records of given intern. Processes being done with class which is below.
class SelectedInternRecordsViewForEmployee(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = '/error/'

    def get(self, request, intern_id):

        selected_intern = get_object_or_404(InternUser, id=intern_id)
        selected_intern_all_working_days = WorkingDayRecord.objects.filter(related_intern=selected_intern.id).order_by(
            '-date')
        selected_intern_available_working_days = []

        for day in selected_intern_all_working_days:
            if day.date <= date.today():
                selected_intern_available_working_days.append(day)

        if selected_intern.company_id != request.user.company.id:
            return redirect('/error/')

        args = {
            'intern': selected_intern,
            'working_days': selected_intern_available_working_days,
        }

        return render(request, 'diaryRecords/selected_intern_all_records_for_employee.html', args)

    def test_func(self):
        if not self.request.user.is_intern and not self.request.user.is_superuser:
            return True
        return False

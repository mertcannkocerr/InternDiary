import json
from accounts.models import User, Company
from django.views import View
from diaryRecords.models import WorkingDayRecord
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from workalendar.europe import Turkey
from .models import InternUser, EmployeeUser
from .forms import (ExtendedUserCreationForm, InternProfileCreationForm, EmployeeEditProfileForm, InternEditProfileForm,
                    UserEditProfileForm, EmployeeProfileCreationForm, CompanyCreationForm)


# The following classes are responsible for performing simple operations about accounts such as login, registrations etc

class LoginRedirectionView(View):

    def get(self, request):
        return redirect('/accounts/login')


class RegisterInternView(View):

    def get(self, request):
        form = ExtendedUserCreationForm()
        profile_form = InternProfileCreationForm()
        all_companies = Company.objects.all()

        args = {
            'form': form,
            'profile_form': profile_form,
            'all_companies': all_companies,
        }

        return render(request, 'accounts/registerIntern.html', args)

    def post(self, request):
        form = ExtendedUserCreationForm(request.POST)
        profile_form = InternProfileCreationForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_intern = True

            # Checking request's email if there is a same E-Mail on DataBase.

            all_users_emails = []
            all_users = User.objects.all()

            for u in all_users:
                all_users_emails.append(u.email)

            for email in all_users_emails:
                if email == request.POST.get('email'):
                    messages.error(request,
                                   "Bu E-Mail adresine sahip bir kullanıcı zaten mevcut.Lütfen Farklı Bir E-Mail "
                                   "Adresi Seçiniz.".title())
                    return redirect("/accounts/register-intern")

            given_company = form.cleaned_data['company']

            # Checking registration to company. If passwords are same, give permission to registration.

            if given_company.company_password != request.POST.get('company_password'):
                messages.error(request, "Şirket Parolanız Maalesef Seçtiğiniz Şirketin Parolası İle Uyuşmuyor.".title())
                return redirect('/accounts/register-intern/')
            user.save()

            intern_profile = profile_form.save(commit=False)
            intern_profile.user = user
            intern_profile.image = profile_form.cleaned_data['image']

            intern_profile.save()

            current_date = timezone.now().date()
            selected_days = 0

            country = Turkey()

            # Creating diary records of intern automatically for each working day, except holidays of Turkey.

            last_day_of_work = timezone.now().date()
            while True:
                if selected_days == intern_profile.worked_day_count:
                    break

                elif country.is_working_day(current_date):
                    record = WorkingDayRecord.objects.create(text='', related_intern=intern_profile, date=current_date)
                    selected_days += 1

                current_date += timezone.timedelta(days=1)
                last_day_of_work = current_date

            intern_profile.begin_of_internship = timezone.now().date()
            intern_profile.end_of_internship = last_day_of_work - timezone.timedelta(days=1)

            intern_profile.company_id = user.company.id
            intern_profile.save()
            messages.success(request,
                             "Başarı ile kayıt oldunuz. Bu sayfadan giriş yapıp hesabınıza erişebilirsiniz.".title())

            return redirect('/accounts/login')

        else:
            # If form is not valid return spesific errors and redirect where corresponding page.


            all_users = User.objects.all()
            all_users_usernames = []

            for user in all_users:
                all_users_usernames.append(user.username)

            for username in all_users_usernames:
                if username == request.POST.get('username'):
                    messages.error(request, "Bu kullanıcı adına sahip bir kullanıcı zaten mevcut.Lütfen Farklı bir "
                                            "kullanıcı adı seçiniz.".title())
                    return redirect("/accounts/register-intern")

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, "Parolalar birbiri ile eşleşmiyor. Lütfen Aynı parolaları girdiğinizden emin "
                                        "olun".title())
                return redirect("/accounts/register-intern")

            messages.error(request,
                           "Kayıt esnasında bir hata oluştu. Lütfen tüm alanları doldurduğunuzdan emin olun".title())
            return redirect("/accounts/register-intern")


class RegisterEmployeeView(View):

    # The operations performed here are identically same as function above. Difference is that is for Employee

    def get(self, request):
        form = ExtendedUserCreationForm()
        profile_form = EmployeeProfileCreationForm()
        all_companies = Company.objects.all()

        args = {
            'form': form,
            'profile_form': profile_form,
            'all_companies': all_companies
        }

        return render(request, 'accounts/registerEmployee.html', args)

    def post(self, request):

        form = ExtendedUserCreationForm(request.POST)
        profile_form = EmployeeProfileCreationForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_intern = False

            all_users = User.objects.all()
            all_users_emails = []

            for u in all_users:
                all_users_emails.append(u.email)

            for email in all_users_emails:
                if email == request.POST.get('email'):
                    messages.error(request,
                                   "Bu E-Mail adresine sahip bir kullanıcı zaten mevcut.Lütfen Farklı bir "
                                   "E-Mail adresi seçiniz.".title())
                    return redirect("/accounts/register-employee")

            given_company = form.cleaned_data['company']

            if given_company.company_password != request.POST.get('company_password'):
                messages.error(request, "Şirket Parolanız Maalesef Seçtiğiniz Şirketin Parolası İle Uyuşmuyor.".title())
                return redirect('/accounts/register-employee/')

            user.save()

            employee_profile = profile_form.save(commit=False)
            employee_profile.user = user
            employee_profile.image = profile_form.cleaned_data['image']

            messages.success(request,
                             "Başarı ile kayıt oldunuz. Bu sayfadan giriş yapıp hesabınıza erişebilirsiniz.".title())

            employee_profile.company_id = user.company.id
            employee_profile.save()

            return redirect('/accounts/login')

        else:

            all_users = User.objects.all()
            all_users_usernames = []

            for user in all_users:
                all_users_usernames.append(user.username)

            for username in all_users_usernames:
                if username == request.POST.get('username'):
                    messages.error(request,
                                   "Bu kullanıcı adına sahip bir kullanıcı zaten mevcut.Lütfen Farklı bir kullanıcı "
                                   "adı seçiniz.".title())
                    return redirect("/accounts/register-employee")

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request,
                               "Parolalar birbiri ile eşleşmiyor. Lütfen Aynı parolaları girdiğinizden emin olun".title())
                return redirect("/accounts/register-employee")

            messages.error(request,
                           "Kayıt esnasında bir hata oluştu. Lütfen tüm alanları doldurduğunuzdan emin olun".title())
            return redirect('/accounts/register-employee/')


class RegisterCompanyView(View):

    # Actually that is not user type, that is just for each intern and employee to show which company they belongs.

    def get(self, request):
        company_form = CompanyCreationForm()

        args = {
            'company_form': company_form,
        }

        return render(request, 'accounts/registerCompany.html')

    def post(self, request):
        company_form = CompanyCreationForm(request.POST)
        all_companies = Company.objects.all()

        for each_company in all_companies:
            if each_company.company_name == request.POST.get('company_name'):
                messages.error(request, "Bu isme sahip bir şirket zaten bulunuyor.".title())
                return redirect('/accounts/register-company')
            else:
                pass

        if company_form.is_valid():
            company_form.save(commit=False)
            if request.POST.get('creation_password') == "6378.6378":
                company = company_form.save(commit=False)
                if company_form.cleaned_data['company_password'] != request.POST.get('password_confirm'):
                    messages.error(request,
                                   "Şirket Parolası ve Parola Tekrar alanındaki şifreler uyuşmuyor. Lütfen tekrar deneyiniz".title())
                    return redirect('/accounts/register-company')
                else:
                    company.company_password = company_form.cleaned_data['company_password']

                company.save()
                messages.success(request, "Şirket profiliniz başarılı bir şekilde oluşturuldu.")
                return redirect('/accounts/login')
            else:
                messages.error(request, "Girilen Şirket Oluşturma Parolası Yanlış".title())
                return redirect('/accounts/register-company')
        else:
            messages.error(request,
                           "Kayıt esnasında bir hata oluştu. Lütfen alanların tamamını dikkatli bir şekilde doldurun".title())
            return redirect('/accounts/register-company')


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):

        args = {
            'user': request.user
        }

        if request.user.is_intern and not request.user.is_superuser:
            args['intern_user'] = InternUser.objects.get(user_id=request.user.id)

        elif not request.user.is_intern and not request.user.is_superuser:
            args['employee_user'] = EmployeeUser.objects.get(user_id=request.user.id)

        return render(request, 'accounts/profile.html', args)

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True


class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/error/'

    def get(self, request):

        if request.user.is_intern and not request.user.is_superuser:
            user_form = UserEditProfileForm(instance=request.user)
            intern_form = InternEditProfileForm(instance=request.user.internuser)
            json_city = json.dumps(request.user.city)
            json_university = json.dumps(request.user.internuser.university)

            args = {
                'user_form': user_form,
                'intern_form': intern_form,
                'intern_user': request.user.internuser,
                'city_intern': json_city,
                'university': json_university,
            }

            return render(request, 'accounts/edit_profile.html', args)

        elif not request.user.is_intern and not request.user.is_superuser:
            user_form = UserEditProfileForm(instance=request.user)
            employee_form = EmployeeEditProfileForm(instance=request.user.employeeuser)
            json_city = json.dumps(request.user.city)

            args = {
                'user_form': user_form,
                'employee_form': employee_form,
                'employee_user': request.user.employeeuser,
                'city_employee': json_city,

            }

            return render(request, 'accounts/edit_profile.html', args)

    def post(self, request):

        if request.user.is_intern and not request.user.is_superuser:
            user_form = UserEditProfileForm(request.POST, instance=request.user)
            intern_form = InternEditProfileForm(request.POST, instance=request.user.internuser)

            if user_form.is_valid() and intern_form.is_valid():
                all_users = User.objects.all()
                all_users_emails = []

                for user in all_users:
                    all_users_emails.append(user.email)

                for email in all_users_emails:
                    if request.POST.get('email') == email:
                        if request.user.email == request.POST.get('email'):
                            pass
                        else:
                            messages.error(request,
                                           "Bu E-Mail adresine sahip bir kullanıcı zaten mevcut.Lütfen Farklı bir E-Mail adresi seçiniz.".title())
                            return redirect('/accounts/profile/edit')

                user_form.save()

                intern = intern_form.save(commit=False)
                if request.FILES.get('image'):
                    intern.image = request.FILES['image']
                intern.save()

                messages.success(request, "Profiliniz Başarılı Bir Şekilde güncellendi".title())

                return redirect('/accounts/profile')
            else:

                all_users = User.objects.all()
                all_users_names = []

                for user in all_users:
                    if request.POST.get('username') == user.username:
                        messages.error(request,
                                       "Bu kullanıcı adına sahip başka bir kullanıcı zaten mevcut. Lütfen Başka bir kullanıcı adı seçiniz.".title())
                        return redirect('/accounts/profile/edit')

                messages.error(request,
                               "Profil Düzenlemesi esnasında bir hata oluştu.Lütfen tüm bilgileri doğru girdiğinizden emin olun ve tekrardan deneyin.".title())
                return redirect('/accounts/profile/edit')

        elif not request.user.is_intern and not request.user.is_superuser:

            user_form = UserEditProfileForm(request.POST, instance=request.user)
            employee_form = EmployeeEditProfileForm(request.POST, instance=request.user.employeeuser)

            if user_form.is_valid() and employee_form.is_valid():
                all_users = User.objects.all()
                for user in all_users:
                    if request.POST.get('email') == user.email:
                        if request.user.email == request.POST.get('email'):
                            pass
                        else:
                            messages.error(request,
                                           "Bu E-Mail adresine sahip bir kullanıcı zaten mevcut.Lütfen Farklı bir E-Mail adresi seçiniz.")
                            return redirect('/accounts/profile/edit')

                user_form.save()
                employee = employee_form.save(commit=False)

                if request.FILES.get('image'):
                    employee.image = request.FILES['image']

                messages.success(request, "Profiliniz Başarılı Bir Şekilde güncellendi".title())
                employee.save()
                return redirect('/accounts/profile')

            else:
                all_users = User.objects.all()
                all_users_names = []

                for user in all_users:
                    if request.POST.get('username') == user.username:
                        messages.error(request,
                                       "Bu kullanıcı adına sahip başka bir kullanıcı zaten mevcut. Lütfen Başka bir "
                                       "kullanıcı adı seçiniz.".title())
                        return redirect('/accounts/profile/edit')

                messages.error(request,
                               "Profil Düzenlemesi esnasında bir hata oluştu.Lütfen tüm bilgileri doğru girdiğinizden "
                               "emin olun ve tekrardan deneyin.".title())

                return redirect('/accounts/profile/edit')

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True


class LoginView(View):

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            return redirect('/accounts/profile')

        else:
            messages.warning(request,
                             "Girmiş olduğunuz kullanıcı adı ve parola ile eşleşen bir hesap bulunamadı. Lütfen "
                             "Tekrar deneyiniz.".title())
            return redirect('/accounts/login')

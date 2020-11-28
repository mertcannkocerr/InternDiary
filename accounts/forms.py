from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from .models import InternUser, User, EmployeeUser, Company


# The following forms are designed for profile creating.

class ExtendedUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ExtendedUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['gender'].required = True
        self.fields['city'].required = True
        self.fields['bio'].required = True

    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    widgets = {
        'bio': forms.Textarea(),
    }

    class Meta:

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'city',
            'password1',
            'password2',
            'gender',
            'company'

        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.bio = self.cleaned_data['bio']
        user.gender = self.cleaned_data['gender']
        user.city = self.cleaned_data['city']

        if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            user.password = make_password(self.cleaned_data['password1'])
        else:
            raise ValueError("Girilen şifreler aynı değil".title())

        if commit:
            user.save()
        return user


class InternProfileCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InternProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['university'].required = True
        self.fields['worked_day_count'].required = True
        self.fields['image'].required = False

        self.fields['university'].label = "Üniversite"
        self.fields['worked_day_count'].label = "Staj Süresi"
        self.fields['image'].label = "Profil Fotoğrafı"

    class Meta:
        university = forms.CharField(widget=forms.TextInput(attrs={'class': 'internUserCreation'}), required=True)
        worked_day_count = forms.IntegerField(widget=forms.EmailInput(attrs={'class': 'internUserCreation'}),
                                              required=True)
        model = InternUser
        fields = (
            'university',
            'worked_day_count',
            'image'
        )


class EmployeeProfileCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileCreationForm, self).__init__(*args, **kwargs)

        self.fields['image'].required = False

    class Meta:
        model = EmployeeUser
        fields = (
            'image',
        )


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'company_name',
            'company_address',
            'company_password'
        )


# The following forms are designed for profile editing.

class UserEditProfileForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

        self.fields['username'].label = "Kullanıcı Adınız"

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['gender'].required = True
        self.fields['city'].required = False
        self.fields['bio'].required = False

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'gender',
            'city',
            'password'
        )

        widgets = {
            'bio': forms.Textarea()
        }


class InternEditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = InternUser
        fields = (
            'university',
            'image'
        )


class EmployeeEditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = EmployeeUser
        fields = (
            'image',
        )

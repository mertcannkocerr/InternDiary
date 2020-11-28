from django import forms
from .models import Project
from tempus_dominus.widgets import DatePicker
from django.utils import timezone

class CreateProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        emp_user = kwargs.pop('emp_user')
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        self.fields['assignee_employee'].required = True
        self.fields['assignee_employee'].initial = emp_user.id

        self.fields['assigned_intern'].required = True

        self.fields['assign_date'].required = True
        self.fields['assign_date'].label = "Başlangıç Tarihi"
        self.fields['assign_date'].initial = ""

        self.fields['due_date'].required = True
        self.fields['due_date'].label = "Bitiş Tarihi"
        self.fields['due_date'].initial = ""

        self.fields['title'].required = True
        self.fields['title'].label = "Başlık"

        self.fields['content'].required = True
        self.fields['content'].label = "Proje İçeriği"

        self.fields['due_date'].widget.attrs.update({'class': 'datepickers'})
        self.fields['assign_date'].widget.attrs.update({'class': 'datepickers'})

        self.fields['assigned_intern'].widget.attrs.update({'class': 'autobox'})

    class Meta:
        model = Project
        fields = (
            'assigned_intern',
            'assignee_employee',
            'assign_date',
            'due_date',
            'title',
            'content'
        )


        widgets = {
            'assignee_employee': forms.HiddenInput,
            'assigned_intern': forms.TextInput,
        }


class EditProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        emp_user = kwargs.pop('emp_user')
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.fields['assignee_employee'].required = True
        self.fields['assignee_employee'].initial = emp_user.id
        self.fields['assigned_intern'].label = "Görevlendirilecek Stajer"
        self.fields['assigned_intern'].required = True
        self.fields['assign_date'].widget.attrs['readonly'] = True
        self.fields['assign_date'].label = "Başlangıç Tarihi"
        self.fields['due_date'].required = True
        self.fields['due_date'].label = "Bitiş Tarihi"
        self.fields['title'].required = True
        self.fields['title'].label = "Başlık"
        self.fields['content'].required = True
        self.fields['content'].label = "Proje İçeriği"

    class Meta:
        model = Project
        fields = (
            'assigned_intern',
            'assignee_employee',
            'assign_date',
            'due_date',
            'title',
            'content'
        )

        widgets = {
            'assignee_employee': forms.HiddenInput,
        }

        today = str(timezone.now().date())
        due_date = forms.DateField(

            widget=DatePicker(
                options={
                    'minDate': today
                }
            )
        )

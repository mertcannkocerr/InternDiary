from django import forms
from .models import WorkingDayRecord


class DiaryUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DiaryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = False
        self.fields['text'].label = ""

    class Meta:
        model = WorkingDayRecord
        fields = (
            'related_intern',
            'text'
        )
        widgets = {'related_intern': forms.HiddenInput()}

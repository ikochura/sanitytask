from django import forms

from .models import Check


class CheckForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CheckForm, self).__init__(*args, **kwargs)
        self.initial['hidden_result'] = True

    class Meta:
        model = Check
        fields = ['check_task', 'user', 'comment', 'hidden_result']
        exclude = ['check_task', 'date']
        widgets = {
            'hidden_result': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'result': forms.CheckboxInput(attrs={"style": "size: 200px"})
        }

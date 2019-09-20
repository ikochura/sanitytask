from django import forms
from django.contrib.auth.models import Group, User

from sanitytask.models import CheckGroup, CheckTask, Check, Client, Shift


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.filter(name__in=['Users', 'Staff']))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username',
                  'password']

        label = {
            'password': 'Password'
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, **kwargs):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role')
        u = super(UserForm, self).save()
        u.groups.set([role])

        u.set_password(password)
        u.save()
        return u


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email']


class PasswordChangeForm(forms.Form):
    old_password_flag = True
    new_passwords_flag = True
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput())
    new_password = forms.CharField(label="New Password", min_length=6, widget=forms.PasswordInput())
    re_new_password = forms.CharField(label="Confirm New Password", min_length=6, widget=forms.PasswordInput())

    def set_old_password_flag(self):
        self.old_password_flag = False
        return 0

    def set_new_password_flag(self):
        self.new_passwords_flag = False
        return 0

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password:
            raise forms.ValidationError("You must enter your old password.")
        if not self.old_password_flag:
            raise forms.ValidationError("The old password that you have entered is wrong.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        if not new_password:
            raise forms.ValidationError("You must enter your new password.")

        if not self.new_passwords_flag:
            raise forms.ValidationError("Your passwords didn't match.")
        return new_password

    def clean_re_new_password(self):
        re_new_password = self.cleaned_data.get('re_new_password')
        if not re_new_password:
            raise forms.ValidationError("You must re-type new password")
        return re_new_password


class CheckGroupForm(forms.ModelForm):
    class Meta:
        model = CheckGroup
        fields = ('name', 'client',)


class CheckTaskForm(forms.ModelForm):
    class Meta:
        model = CheckTask
        fields = ('name_task', 'check_group',)


class ChecksForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('date', 'result', 'hidden_result', 'user', 'check_task', 'comment',)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'user',)


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ('user', 'checkgroup', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',)
        labels = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday',
                  'sat': 'Saturday',
                  'sun': 'Sunday', }

from datetime import date

from django import forms
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from web.models import (ParentProfile, Child, Doctor)


class LoginForm(AuthenticationForm):
    pass


class DoctorForm(forms.ModelForm):
    
    class Meta:
        model = Doctor
        exclude = ('child', )


class ChildForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = SelectDateWidget(years=range(
            date.today().year-15, date.today().year-2, 1),
            attrs={'class':'form-control'}, 
            empty_label=('Year', 'Month', 'Date')
        )
    
    class Meta:
        model = Child
        exclude = ('parent', )


class UserForm(forms.ModelForm):
    password_again = forms.CharField(min_length=8, strip=False, widget=forms.PasswordInput())

    def clean_password_again(self):
        if self.cleaned_data["password"] != self.cleaned_data["password_again"]:
            raise forms.ValidationError(_('Two passwords do not match. Please try again!'), code='invalid')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email', )


class ParentProfileForm(forms.ModelForm):
    
    class Meta:
        model = ParentProfile
        exclude = ('user', )
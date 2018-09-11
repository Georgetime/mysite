# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import Score, Assignment
from django.utils import timezone
from datetime import datetime
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

# class LoginForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.widgets.TextInput(
#             attrs={'class': "form-control", 'placeholder': 'Enter Your UserName'},),
#         label='UserName',
#         max_length=160,
#     )
#     password = forms.CharField(
#         widget=forms.widgets.PasswordInput(
#             attrs={'class': "form-control", 'placeholder': 'Enter Your Password'},
#             render_value=True),
#         label='PassWord',
#     )

class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("This email does not exist.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                        raise forms.ValidationError("This username does not exist. Please register first.")

        return username

class RegistrationForm(forms.Form):
    type_choices = (
        (1, '教师'),
        (0, '学生'),
    )

    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email', )
    user_type = forms.ChoiceField(label='user_type', choices=type_choices)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 2:
            raise forms.ValidationError("Your username must be at least 2 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists.")
        else:
            raise forms.ValidationError("Please enter a valid email.")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2

class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone', max_length=50, required=False)

class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    # Use clean methods to define custom validation rules
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")
        return password2

def make_score_form(assignment_id):
    """
    
    :param employee: 
    :return: 
    Returns a Score form for the given assignment,
    restricting the Project choices.
    """
    class ScoreForm(forms.ModelForm):
        assignment = forms.ModelChoiceField(queryset=Assignment.objects.get(pk=assignment_id)),
        class Meta:
            model = Score
            exclude = {}
            widgets = {
                'description': forms.TextInput(attrs={'cols': 20, 'rows': 1}),
            }

    return ScoreForm

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_title', 'assignment_detail', 'finish_date', 'schedule')
        widgets = {
            'schedule': forms.TextInput()
        }

    def clean_assignment_title(self):
        assignment_title = self.cleaned_data.get('assignment_title')
        if Assignment.objects.filter(assignment_title=assignment_title):
            raise forms.ValidationError("作业名称已经存在，请检查名称！")
        return assignment_title

    def clean_finish_date(self):
        finish_date = self.cleaned_data.get('finish_date')
        if finish_date < datetime.today().date():
            raise forms.ValidationError("完成时间需要大于现在时间！")
        return finish_date



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'student_id',
            'email',
            'course',
            'year_level',
            'password1',
            'password2',
        ]
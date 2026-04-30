from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=100, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.country = self.cleaned_data['country']
        user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user
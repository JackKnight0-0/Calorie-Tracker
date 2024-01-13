from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile


class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'autocomplete': 'username', 'placeholder': 'Username'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'autocomplete': 'email', 'placeholder': 'Email'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if EmailAddress.objects.filter(email=email).exclude(user=self.instance).exists():
            self.add_error('email', 'This email already taken!')
        return email


class UserProfileChangeAvatar(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)

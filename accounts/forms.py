from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from accounts.models import UserProfile


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    Birth_Date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = User
        fields = ['username', 'Birth_Date', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Οι κωδικοί δεν ταιριάζουν.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """Φόρμα για αλλαγή στοιχείων χρήστη"""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileImageForm(forms.ModelForm):
    """Φόρμα για αλλαγή εικόνας προφίλ"""
    class Meta:
        model = UserProfile
        fields = ["profile_image"]

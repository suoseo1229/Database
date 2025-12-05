from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    number = forms.CharField(
        max_length=30,
        label="학번",
        widget=forms.TextInput(attrs={
            "class": "...",
            "placeholder": "학번 (필수)"
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_number(self):
        number = self.cleaned_data.get("number")
        if Profile.objects.filter(number=number).exists():
            raise forms.ValidationError("이미 사용중인 학번입니다.")
        return number

    def save(self, commit=True):
        user = super().save(commit)
        number = self.cleaned_data.get("number")

        if commit:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.number = number
            profile.save()

        return user
    
class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        label='전화번호',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '010-1234-5678'})
    )

    birth = forms.DateField(
        label='생년월일',
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )

    class Meta:
        model = Profile 
        fields = ['number', 'birth', 'phone', 'location']

                                

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='현재 비밀번호(필수)', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='변경 비밀번호', required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='변경 비밀번호 확인', required=False, widget=forms.PasswordInput)

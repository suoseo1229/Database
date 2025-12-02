from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    nickname = forms.CharField(
        max_length=30,
        required=False,
        label="닉네임",
        widget=forms.TextInput(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm",
            "placeholder": "닉네임 (선택)",
        }),
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
    
    def save(self, commit=True):
        user = super().save(commit)
        nickname = self.cleaned_data.get("nickname")
        if commit:
            profile, crated = Profile.objects.get_or_create(user=user)
            if nickname:
            # Profile은 시그널로 자동 생성되니까 가져와서 닉네임만 세팅
                user.profile.nickname = nickname
                user.profile.save()
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
        fields = ['nickname', 'birth', 'phone', 'location']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        user = self.instance.user 
        if nickname:
            if Profile.objects.exclude(user=user).filter(nickname=nickname).exists():
                raise ValidationError('이미 사용중인 닉네임')
            return nickname
                                

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='현재 비밀번호(필수)', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='변경 비밀번호', required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='변경 비밀번호 확인', required=False, widget=forms.PasswordInput)

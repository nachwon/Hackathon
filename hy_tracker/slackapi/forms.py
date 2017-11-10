from django import forms

from .models import UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = (
            'name', 'steamId64'
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': '이름'
                },

            ),
            'steamId64': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': '64-bit 스팀 아이디'
                },
            )
        }
        labels = {
            'name': '',
            'steamId64': '',
        }
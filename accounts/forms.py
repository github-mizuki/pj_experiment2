import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if User.objects.filter(email=email, is_active=True):
            raise forms.ValidationError('そのEmailアドレスは使用できません')
        if not all((re.search('[0-9]', password), re.search('[a-z]', password), re.search('[A-Z]', password))):
            raise forms.ValidationError('Passwordには数字・英小文字・英大文字が必須です')
        if len(password) < 8:
            raise forms.ValidationError('Passwordは8文字以上にしてください')
        if password != confirm_password:
            raise forms.ValidationError('Passwordが異なります')
        User.objects.filter(email=email, is_active=False).delete()

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
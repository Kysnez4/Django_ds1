from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class LoginUserForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
        })
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите номер телефона',
        })
    )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите страну',
        })
    )
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        })
    )

    class Meta:
        model = User
        fields = ('username','email', 'phone', 'country', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль',
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not phone.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры')
        return phone
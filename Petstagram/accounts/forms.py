from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from Petstagram.accounts.models import PetstagramUser


class PetstagramUserCreateForm(UserCreationForm):
    class Meta:
        model = PetstagramUser
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'Прякор',
    }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password',
        'placeholder': 'Парола',
    }))


class PetstagramUserEditForm(forms.ModelForm):
    profile_pic = forms.ImageField(
        label="Снимка:",
        widget=forms.FileInput,
        required=False
    )
    class Meta:
        model = PetstagramUser
        fields = ('username', 'first_name',
                  'last_name', 'email',
                  'profile_pic', 'gender')
        exclude = ('password',)
        labels = {'username': 'Прякор:',
                  'first_name': 'Име:',
                  'last_name': 'Фамилия:',
                  'email': 'Имейл:',

                  'gender': 'Пол:'}
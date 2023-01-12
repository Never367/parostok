from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, \
    UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm

from account.models import Profile


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Ел. пошта',
                             widget=forms.EmailInput(
                                 attrs={'autofocus': True,
                                        'id': 'Login1',
                                        'class': 'form-control'}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'id': 'Login2',
                                          'class': 'form-control',
                                          }),
    )
    error_messages = {
        'invalid_login': 'Будь ласка, введіть правильні імена '
                         'користувача та пароль. Зауважте, що '
                         'обидва поля можуть бути чутливими до '
                         'регістру',
        'inactive': "Цей запис користувача неактивний. "
                    "Будь-ласка, підтвердіть ел. пошту або "
                    "зв'яжіться з адміністратором сайту",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                    self.confirm_login_allowed(user_temp)
                except User.DoesNotExist:
                    raise self.get_invalid_login_error()
                raise self.get_invalid_login_error()

        return self.cleaned_data


class PasswordChangeFormBase(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'autofocus': True,
                                          'class': 'form-control'
                                          }),
    )
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Новий пароль (підтвердження)",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
    )


class PasswordResetFormBase(PasswordResetForm):
    email = forms.EmailField(
        label="Ел. пошта",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class': 'form-control'})
    )


class SetPasswordFormBase(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Підтвердження нового пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Повторіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Ел. пошта',
        }
        error_messages = {
            'username': {'unique': 'Користувач з такою ел. адресою вже зареєстрований'}
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Паролі не збігаються.')
        password_validation.validate_password(cd['password2'])
        return cd['password2']


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'required': True}),
            'username': forms.EmailInput(attrs={'class': 'form-control',
                                                'required': True}),
        }
        labels = {
            'username': 'Ел. пошта'
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'city', 'address', 'postal_code']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'pattern': '\\+38\\d{10}',
                                                   'placeholder': '+380501111111',
                                                   'value': '+380'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

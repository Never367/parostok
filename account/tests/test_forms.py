from django.test import TestCase
from django import forms

from account.forms import LoginForm, PasswordChangeFormBase, PasswordResetFormBase
from account.tests.test_views import AbstractTestView


class LoginFormTest(AbstractTestView, TestCase):

    def test_form_date_field_label(self):
        form = LoginForm()
        username_field = form.fields['username']
        password_field = form.fields['password']
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertTrue(isinstance(username_field.widget, forms.EmailInput))
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LoginForm(data=self.credential)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank(self):
        self.credential['username'] = 'user'
        self.credential['password'] = '123'
        form = LoginForm(data=self.credential)
        self.assertFalse(form.is_valid())

    def test_form_errors(self):
        self.user.is_active = False
        self.user.save()
        form = LoginForm(data=self.credential)
        self.assertEqual(form.errors['__all__'],
                         form.error_messages['inactive'].split('/'))

        self.credential['username'] = 'user'
        self.credential['password'] = '123'
        form = LoginForm(data=self.credential)
        self.assertEqual(form.errors['__all__'],
                         form.error_messages['invalid_login'].split('/'))


class PasswordChangeFormBaseTest(AbstractTestView, TestCase):

    def test_form_date_field_label(self):
        form = PasswordChangeFormBase(user=self.user)
        old_password_field = form.fields['old_password']
        new_password1_field = form.fields['new_password1']
        new_password2_field = form.fields['new_password2']
        self.assertIn('old_password', form.fields)
        self.assertIn('new_password1', form.fields)
        self.assertIn('new_password2', form.fields)
        self.assertTrue(isinstance(old_password_field.widget, forms.PasswordInput))
        self.assertTrue(isinstance(new_password1_field.widget, forms.PasswordInput))
        self.assertTrue(isinstance(new_password2_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        data = {'old_password': '12345', 'new_password1': '12qwerty12',
                'new_password2': '12qwerty12'}
        form = PasswordChangeFormBase(user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank(self):
        data = {'old_password': '12345', 'new_password1': '12345',
                'new_password2': '12345'}
        form = PasswordChangeFormBase(user=self.user, data=data)
        self.assertFalse(form.is_valid())


class PasswordResetFormBaseTest(AbstractTestView, TestCase):

    def test_form_date_field_label(self):
        form = PasswordResetFormBase()
        email_field = form.fields['email']
        self.assertIn('email', form.fields)
        self.assertTrue(isinstance(email_field.widget, forms.EmailInput))

    def test_form_accepts_valid_input(self):
        data = {'email': 'test_user@test.com'}
        form = PasswordResetFormBase(data=data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank(self):
        data = {'email': 'test_user'}
        form = PasswordResetFormBase(data=data)
        self.assertFalse(form.is_valid())


class SetPasswordFormBaseTest(TestCase):

    pass

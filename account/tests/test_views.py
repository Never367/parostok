from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from account.models import Profile, WishList
from account.views import RegisterConfirmView
from main_app.models import Product
from main_app.tests.test_views import AbstractProductsViewTest
from orders.models import Order


class AbstractTestView:

    def setUp(self):
        self.credential = {'username': 'test_user', 'password': '12345',
                           'email': 'test_user@test.com'}
        self.user = User.objects.create_user(**self.credential)
        self.profile = Profile.objects.create(user=self.user, phone_number='test_number',
                               city='test_city', address='test_address',
                               postal_code='test_postal_code')
        self.wishlist = WishList.objects.create(user=self.user)


class AbstractTokenTestView:

    def setUp(self):
        self.credential = {'username': 'test_user', 'password': '12345'}
        user = User.objects.create_user(**self.credential)
        default_token_generator = PasswordResetTokenGenerator()
        self.token = default_token_generator.make_token(user)
        self.uidb64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
        self.client.login(**self.credential)


class LoginTestViewBaseTest(AbstractTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.post('/account/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_form(self):
        response = self.client.post(reverse('login'))
        login = self.client.login(**self.credential)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(login)
        self.assertFormError(response, 'form', 'username', "Це поле обов'язкове.")
        self.assertFormError(response, 'form', 'password', "Це поле обов'язкове.")


class LogoutTestViewBaseTest(AbstractTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')


class PasswordChangeTestViewBaseTest(AbstractTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.credential)
        response = self.client.post('/account/password-change/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.credential)
        response = self.client.post(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.credential)
        response = self.client.post(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/account/password-change/')


class PasswordResetViewBaseTest(AbstractTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.post('/account/password-reset/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.post(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.post(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')


class PasswordResetConfirmViewBaseTest(AbstractTokenTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.post(
            f'/account/password-reset/{self.uidb64}/{self.token}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.post(reverse('password_reset_confirm',
                                            args=[str(self.uidb64), str(self.token)]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.post(reverse('password_reset_confirm',
                                            args=[str(self.uidb64), str(self.token)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')


class RegisterViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_form(self):
        data = {'username': 'test_username', 'password': 'test_password',
                'password2': 'test_password'}
        response = self.client.post(reverse('register'), data=data)
        self.assertTrue(response, 200)


class RegisterConfirmViewTest(AbstractTokenTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(
            f'/account/register/{self.uidb64}/{self.token}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register_confirm',
                                           args=[str(self.uidb64), str(self.token)]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register_confirm',
                                           args=[str(self.uidb64), str(self.token)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register_confirm.html')

    def test_get_user(self):
        self.assertEqual(str(RegisterConfirmView.get_user(self, self.uidb64)),
                         'test_user')


class EditTest(AbstractTestView, TestCase):

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.credential)
        response = self.client.get('/account/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/edit.html')
        
    def test_form(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('edit'))
        self.assertContains(response, 'test_city')
        self.assertNotContains(response, 'test_name')

        data = {'first_name': 'test_name', 'last_name': 'test_last_name',
                'username': 'test_email', 'phone_number': 'test_number',
                'city': 'test_city', 'address': 'test_city',
                'postal_code': 'test_postal_code'}
        self.client.post(reverse('edit'), data=data)
        response = self.client.get(reverse('edit'))
        self.assertContains(response, 'test_name')


class OrdersTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credential = {'username': 'test_user', 'password': '12345'}
        cls.user = User.objects.create_user(**cls.credential)
        number_of_orders = 13
        for number in range(number_of_orders):
            Order.objects.create(user=cls.user, first_name='test_name',
                                 last_name='test_last_name',
                                 phone_number='test_number', email='test_email',
                                 city='test_city', address='test_address',
                                 postal_code='test_postal_code',
                                 delivery_type='pick_up')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.credential)
        response = self.client.get('/account/orders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/orders.html')

    def test_pagination_is_ten(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('orders' in response.context)
        self.assertTrue(response.context['orders'])
        self.assertTrue(len(response.context['orders']) == 10)

    def test_lists_all_orders(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        self.client.login(**self.credential)
        response = self.client.get(reverse('orders') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('orders' in response.context)
        self.assertTrue(response.context['orders'])
        self.assertTrue(len(response.context['orders']) == 3)
        
        
class WishListTest(AbstractProductsViewTest, TestCase):
    
    def setUp(self):
        self.credential = {'username': 'test_user', 'password': '12345'}
        self.user = User.objects.create_user(**self.credential)
        self.user_wish_list = WishList.objects.get_or_create(user=self.user)[0]
        self.client.login(**self.credential)
        for product in Product.objects.all():
            self.user_wish_list.product.add(product)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/wish_list/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/wish_list.html')

    def test_pagination_is_twelve(self):
        response = self.client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_wish_list' in response.context)
        self.assertTrue(response.context['user_wish_list'])
        self.assertTrue(len(response.context['user_wish_list']) == 12)

    def test_lists_all_orders(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('wish_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_wish_list' in response.context)
        self.assertTrue(response.context['user_wish_list'])
        self.assertTrue(len(response.context['user_wish_list']) == 3)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('wish_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/account/wish_list/')


class WishListAddRemoveTest(AbstractProductsViewTest, TestCase):

    def setUp(self):
        self.credential = {'username': 'test_user', 'password': '12345'}
        self.user = User.objects.create_user(**self.credential)
        self.user_wish_list = WishList.objects.get_or_create(user=self.user)[0]
        self.client.login(**self.credential)

    def test_view_url_exists_at_desired_location(self):
        response_add = self.client.post('/account/wish_list/add/1/',
                                    HTTP_REFERER='http://localhost/')
        self.assertEqual(response_add.status_code, 302)

        response_wish_list = self.client.get(reverse('wish_list'))
        self.assertContains(response_wish_list, 'product_name_0')

        response_remove = self.client.post('/account/wish_list/remove/1/',
                                    HTTP_REFERER='http://localhost/')
        self.assertEqual(response_remove.status_code, 302)

        response_wish_list = self.client.get(reverse('wish_list'))
        self.assertNotContains(response_wish_list, 'product_name_0')

    def test_view_url_accessible_by_name(self):
        response_add = self.client.post(reverse('wish_list_add', args=['1']),
                                        HTTP_REFERER='http://localhost/')
        self.assertEqual(response_add.status_code, 302)

        response_wish_list = self.client.get(reverse('wish_list'))
        self.assertContains(response_wish_list, 'product_name_0')

        response_remove = self.client.post(reverse('wish_list_remove', args=['1']),
                                           HTTP_REFERER='http://localhost/')
        self.assertEqual(response_remove.status_code, 302)

        response_wish_list = self.client.get(reverse('wish_list'))
        self.assertNotContains(response_wish_list, 'product_name_0')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response_add = self.client.post(reverse('wish_list_add', args=['1']))
        response_remove = self.client.post(reverse('wish_list_remove', args=['1']))
        self.assertEqual(response_add.status_code, 302)
        self.assertEqual(response_remove.status_code, 302)
        self.assertRedirects(response_add, '/?next=/account/wish_list/add/1/')
        self.assertRedirects(response_remove, '/?next=/account/wish_list/remove/1/')

from django.test import TestCase
from django.contrib.auth.models import User

from account.models import Profile, WishList


class AbstractUserTest:

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='test_username',
                                            password='test_password')
        cls.profile = Profile.objects.create(
            user=cls.user,
            phone_number='test_number',
            city='test_city',
            address='test_address',
            postal_code='test_postal_code'
        )
        cls.wish_list = WishList.objects.create(user=cls.user)


class ProfileModelTest(AbstractUserTest, TestCase):

    def test_str(self):
        self.assertEquals(str(self.profile), 'Профіль test_username')


class WishListModelTest(AbstractUserTest, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_username',
                                            password='test_password')

        cls.wish_list = WishList.objects.create(user=cls.user)

    def test_str(self):
        self.assertEquals(str(self.wish_list), 'Список бажань test_username')

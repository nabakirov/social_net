from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class UserSetUpTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'user@gmail.com',
            'password': 'pwd1',
        }
        self.user_data2 = {
            'email': 'user2@gmail.com',
            'password': 'pwd2',
        }

        self.user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password']
        )

        self.user2 = User.objects.create_user(
            email=self.user_data2['email'],
            password=self.user_data2['password']
        )
        self.token = RefreshToken.for_user(self.user)
        self.token2 = RefreshToken.for_user(self.user2)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token.access_token}'}
        self.auth_headers2 = {'HTTP_AUTHORIZATION': f'Bearer {self.token2.access_token}'}


class AuthTestCase(UserSetUpTestCase):
    def test_user_signup(self):
        sign_up_url = reverse('signup')

        data = {
            'email': 'user2testcase@gmail.com',
            'password': 'user2testcase'
        }

        db_user = User.objects.filter(email=data['email']).first()
        self.assertIsNone(db_user)
        r = self.client.post(sign_up_url, data)
        self.assertEqual(r.status_code, 200)
        db_user = User.objects.filter(email=data['email']).first()
        self.assertIsNotNone(db_user)
        pwd_ok = db_user.check_password(data['password'])
        self.assertIs(pwd_ok, True)

    def test_user_signup_missed_data(self):
        sign_up_url = reverse('signup')
        r = self.client.post(sign_up_url)
        self.assertEqual(r.status_code, 400)

    def test_user_signup_invalid_email(self):
        sign_up_url = reverse('signup')
        data = {
            'email': 'user2testcasom',
            'password': 'user2testcase'
        }
        r = self.client.post(sign_up_url, data=data)
        self.assertEqual(r.status_code, 400)

    def test_user_signup_miss_email(self):
        sign_up_url = reverse('signup')
        data = {
            'password': 'user2testcase'
        }
        r = self.client.post(sign_up_url, data=data)
        self.assertEqual(r.status_code, 400)

    def test_user_signup_miss_password(self):
        sign_up_url = reverse('signup')
        data = {
            'email': 'user2testcase@gmail.com',
        }
        r = self.client.post(sign_up_url, data=data)
        self.assertEqual(r.status_code, 400)

    def test_user_login(self):
        login_url = reverse('login')
        user_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }

        r = self.client.post(login_url, user_data)
        self.assertEqual(r.status_code, 200)

    def test_user_login_incorrect_credentials(self):
        login_url = reverse('login')
        user_data = {
            'email': self.user_data['email'],
            'password': 'invalid pass',
        }

        r = self.client.post(login_url, user_data)
        self.assertEqual(r.status_code, 400)


class ProfileTestCase(UserSetUpTestCase):

    def test_get_profile(self):
        url = reverse('profile')
        r = self.client.get(url, **self.auth_headers)
        self.assertEqual(r.status_code, 200)

    def test_profile_unauth(self):
        url = reverse('profile')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 401)
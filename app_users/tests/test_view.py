from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginPageTest(TestCase):
    def test_login_page(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')


class LogoutPageTest(TestCase):
    def test_logout_page(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')


class RegistrationPageTest(TestCase):
    def test_registration_page(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_register(self):
        self.client.post('/users/register/',
                         {'username': 'test_user',
                          'password1': 'pass@123',
                          'password2': 'pass@123',
                          })
        self.assertEqual(User.objects.last().username, 'test_user')


class UserDetailPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_admin')
        self.user.set_password('pass@123')
        self.user.save()

    def test_user_detail_page(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.get(reverse('user_detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail.html')


class UserEditPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_admin')
        self.user.set_password('pass@123')
        self.user.save()

    def test_user_edit_page(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.get(reverse('user_edit', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'users/user_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_user_edit(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.post(reverse('user_edit', kwargs={'pk': self.user.pk}),
                                    {
                                        'first_name': 'Ivan',
                                        'last_name': 'Petrov'
                                    })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.last_name, 'Petrov')


class UserStyleEditPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_admin')
        self.user.set_password('pass@123')
        self.user.save()

    def test_style_edit_page(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.get(reverse('style_edit', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'users/color_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_correct_style_edit(self):
        self.user.profile.balance = 100
        self.user.profile.save()
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.post(reverse('style_edit', kwargs={'pk': self.user.pk}),
                                    {'color': '#000999'})
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, 0)
        self.assertEqual(self.user.profile.color, '#000999')

    def test_uncorrect_style_edit(self):
        self.user.profile.balance = 10
        self.user.profile.save()
        self.client.login(username='test_admin', password='pass@123')
        self.client.post(reverse('style_edit', kwargs={'pk': self.user.pk}),
                                    {'color': '#000999'})
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, 10)
        self.assertEqual(self.user.profile.color, '#000000')

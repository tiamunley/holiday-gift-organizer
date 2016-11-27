from rest_framework import status
from holiday_app.models import HolidayUser
from holiday_app.tests.base import BasicTest


class UserCreateTests(BasicTest):
    """
    """

    def setUp(self):
        self.superuser = HolidayUser.objects.create_superuser('admin', 'john@snow.com', self.PW)

    def test_can_create_user(self):
        """
        """

        self.login(username='admin')
        user = {
            'username': 'user_a',
            'password': self.PW,
            'email':    'user@a.com'
        }

        response = self.client.post('/api/v1/user', user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del user['password']
        self.verify_built(user, response.data)

        self.logout()


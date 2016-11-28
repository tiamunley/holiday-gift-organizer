from rest_framework import status
from holiday_app.models import HolidayUser
from holiday_app.tests.base import BasicTest


class GiftCreateTests(BasicTest):
    """
    """

    def setUp(self):
        self.superuser = HolidayUser.objects.create_superuser('admin', 'john@snow.com', self.PW)

        self.login(username='admin')
        self.user_id = self.create_user()
        self.logout()

    def test_can_create_gift(self):
        """
        """

        self.login(username='user_a')
        recipient = {
            'name':     'Alexander Hamilton',
            'relation': 'family',
            'giver':    self.user_id
        }

        response = self.client.post('/api/v1/recipient', recipient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.verify_built(recipient, response.data)
        recipient_id = response.data['id']

        gift = {
            'status': 'bought',
            'item':   'Lego Kit',
            'notes':  'Here are some notes.',
            'cost':   '10.34'
        }

        response = self.client.post('/api/v1/recipient/%s/gift' % recipient_id, gift, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.verify_built(gift, response.data)

        self.logout()


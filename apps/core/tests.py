from django.test import TestCase

# Create your tests here.
from django.test import SimpleTestCase


class HelloViewTests(SimpleTestCase):
    def test_hello_view_returns_greeting(self):
        response = self.client.get('/hello/Alice/', HTTP_HOST='127.0.0.1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Hello, Alice!')

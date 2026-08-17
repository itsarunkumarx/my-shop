from django.test import TestCase, Client
from storeapp.models import Category, Product

class HomeViewTest(TestCase):
    def test_home_page(self):
        client = Client()
        response = client.get('/')
        print('Status code:', response.status_code)
        if response.status_code == 500:
            print('Context / Exception:', response.content.decode('utf-8')[:1000])
        self.assertEqual(response.status_code, 200)


import unittest
from pathlib import Path
import pybbox2

class TestBbox(unittest.TestCase):
    if Path('secret').exists:
        with open('secret', 'r') as file:
            password = file.read().strip()
    else:
        password = input('Please enter the box password: ')

    def setUp(self):
        pybbox2.Bbox(password=self.password)

    def test_check_authentication(self):
        box = pybbox2.Bbox(password=self.password)
        box.login()

    def test_url(self):
        box = pybbox2.Bbox(password=self.password)
        url = box.url('api_endpoint')
        self.assertEqual(url, 'https://mabbox.bytel.fr/api/v1/api_endpoint')

    def test_custom_hostname(self):
        box = pybbox2.Bbox(api_host='http://1.1.1.1', password=self.password)
        url = box.url('api_endpoint')
        self.assertEqual(url, 'http://1.1.1.1/api/v1/api_endpoint')

if __name__ == '__main__':
    unittest.main()

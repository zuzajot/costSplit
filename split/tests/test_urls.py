from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestUrls(SimpleTestCase):

    def test_create_group_url_is_resolved(self):
        url = reverse('')

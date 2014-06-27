# coding: utf-8
from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """
        GET / must return status code 200.
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Home must use template index.html
        """
        self.assertTemplateUsed(self.resp, 'core/base.html')

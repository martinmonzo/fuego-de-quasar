from django.test import TestCase

from rest_framework.test import APIClient


class BaseTestCaseAPIView(TestCase):

    def setUp(self):
        self.client = APIClient()

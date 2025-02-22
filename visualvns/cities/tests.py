from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve

from cities.views import top, cities_new, cities_edit, cities_detail

# Create your tests here.

class CreateCitiesTest(TestCase):
    def test_should_resolve_cities_new(self):
        found = resolve('/cities/new/')
        self.assertEqual(cities_new, found.func)

class CitiesDetailTest(TestCase):
    def test_should_resolve_cities_detail(self):
        found = resolve('/cities/1/')
        self.assertEqual(cities_detail, found.func)

class EditCitiesTest(TestCase):
    def test_should_resolve_cities_edit(self):
        found = resolve('/cities/1/edit/')
        self.assertEqual(cities_edit, found.func)

class TopPageTest(TestCase):
    def test_top_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_top_returns_expected_content(self):
        response = self.client.get("/")
        self.assertEqual(response.content, b"Hello World")

class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        request = HttpRequest()
        response = top(request)
        self.assertEqual(response.status_code, 200)

    def test_top_returns_expected_content(self):
        request = HttpRequest()
        response = top(request)
        self.assertEqual(response.content, b"Hello World")

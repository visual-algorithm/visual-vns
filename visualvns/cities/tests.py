from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.urls import resolve
from django.contrib.auth import get_user_model

from cities.models import City, Route, Salesman
from cities.views import top, city_new, city_edit, city_detail

# Create your tests here.

UserModel = get_user_model()

class TopPageRenderCityTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "top_secret_pass0001",
        )
        self.city = City.objects.create(
            city_name = "sample_name",
            address = "sample_address",
            description = "sample_description",
            # salesman = Salesman.objects.create(
            #     salesman_name = "sample_name",
            #     created_by = self.user
            # ),
            created_by = self.user
        )

    def test_should_return_city_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.city.city_name)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)

    

class CreateCityTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "top_secret_pass0001",
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get("/cities/new/")
        self.assertContains(response, "都市の登録", status_code=200)

    def test_create_city(self):
        data = {'city_name': '都市名', 'address': '住所', 'description': '備考'}
        self.client.post("/cities/new/", data)
        city = City.objects.get(city_name='都市名')
        self.assertEqual('住所', city.address)
        self.assertEqual('備考', city.description)


class CityDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "top_secret_pass0001",
        )
        self.city = City.objects.create(
            city_name = "sample_name",
            address = "sample_address",
            description = "sample_description",
            # salesman = Salesman.objects.create(
            #     salesman_name = "sample_name",
            #     created_by = self.user
            # ),
            created_by = self.user
        )

    def test_should_use_expected_template(self):
        response = self.client.get("/cities/%s/" % self.city.id)
        self.assertTemplateUsed(response, "cities/city_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/cities/%s/" % self.city.id)
        self.assertContains(response, self.city.city_name, status_code=200)

class EditCityTest(TestCase):
    def test_should_resolve_cities_edit(self):
        found = resolve('/cities/1/edit/')
        self.assertEqual(city_edit, found.func)

class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "ビジュアル VNS" ,status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "cities/top.html")

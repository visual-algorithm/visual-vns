from django.urls import resolve
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from routes.models import Route
from routes.views import top, route_new, route_detail, route_edit

# Create your tests here.

UserModel = get_user_model()

class TopPageRenderRouteTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@exmaple.com",
            password = "top_secret_pass0001",
        )
        self.route = Route.objects.create(
            title = "title1",
            depot = "ddd",
            spot1 = "ppp",spot2 = "ppp",spot3 = "ppp",
            spot4 = "ppp",spot5 = "ppp",spot6 = "ppp",
            spot7 = "ppp",spot8 = "ppp",spot9 = "ppp",
            spot10 = "ppp",spot11 = "ppp",spot12 = "ppp",
            spot13 = "ppp",spot14 = "ppp",spot15 = "ppp",
            spot16 = "ppp",spot17 = "ppp",spot18 = "ppp",
            spot19 = "ppp",spot20 = "ppp",
            description = "xxx",
            created_by = self.user,
        )
    
    def test_should_return_route_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.route.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class CreateRouteTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@exmaple.com",
            password = "top_secret_pass0001",
        )
    
    def test_render_creation_form(self):
        response = self.client.get("/routes/new/")
        self.assertContains(response, "ルートの登録", status_code=200)

    def test_create_route(self):
        data = {'title': 'タイトル', 'depot': '拠点',
                'spot1' : '訪問1','spot2' : '訪問2','spot3' : '訪問3',
                'spot4' : '訪問4','spot5' : '訪問5','spot6' : '訪問6',
                'spot7' : '訪問7','spot8' : '訪問8','spot9' : '訪問9',
                'spot10' : '訪問10','spot11' : '訪問11','spot12' : '訪問12',
                'spot13' : '訪問13','spot14' : '訪問14','spot15' : '訪問15',
                'spot16' : '訪問16','spot17' : '訪問17','spot18' : '訪問18',
                'spot19' : '訪問19','spot20' : '訪問20',
                'description': '備考'}
        self.client.get("/routes/new/", data)
        route = Route.objects.get(title = 'タイトル')
        self.assertEqual('拠点', route.depot)
        self.assertEqual('備考', route.description)
    
    

class RouteDetailTest(TestCase):
    def test_should_resolve_route_detail(self):
        found = resolve("/routes/1/")
        self.assertEqual(route_detail, found.func)

class EditRouteTest(TestCase):
    def test_should_resolve_route_edit(self):
        found = resolve("/routes/1/edit/")
        self.assertEqual(route_edit, found.func)



class TopPageTest(TestCase):
    def test_top_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "ビジュアル VNS", status_code=200)

    def test_top_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "routes/top.html")

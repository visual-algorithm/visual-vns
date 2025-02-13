from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from visualapp.models import Cource
from visualapp.views import top

# Create your tests here.

UserModel = get_user_model()

class TopPageRenderVisualappTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = 'test_user',
            email="test@exmaple.com",
            password="top_secret_pass0001",
        )
        self.cource = Cource.objects.create(
            title = 'サンプル2',
            start = '埼玉県秩父市宮側町1-8',
            spot1 = '埼玉県秩父市番場町1-1',
            spot2 = '埼玉県秩父市熊木熊木町8-15',
            spot3 = '埼玉県秩父郡小鹿野町長留2518'
        )
    
    def test_should_return_cource_title(self):
        request = RequestFactory().get('/')
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.cource.title)

class CourceDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "secret",
        )
        self.cource = Cource.objects.create(
            title = 'サンプル2',
            start = '埼玉県秩父市宮側町1-8',
            spot1 = '埼玉県秩父市番場町1-1',
            spot2 = '埼玉県秩父市熊木熊木町8-15',
            spot3 = '埼玉県秩父郡小鹿野町長留2518',
        )
    
    def test_should_use_expected_template(self):
        response = self.client.get("/visualapp/%s/" % self.cource.id)
        self.assertTemplateUsed(response, "visualapp/cource_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/visualapp/%s/" % self.cource.id)
        self.assertContains(response, self.cource.title, status_code=200)

class CreateCourceTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "secret",
        )
        self.cource = Cource.objects.create(
            title = 'サンプル2',
            start = '埼玉県秩父市宮側町1-8',
            spot1 = '埼玉県秩父市番場町1-1',
            spot2 = '埼玉県秩父市熊木熊木町8-15',
            spot3 = '埼玉県秩父郡小鹿野町長留2518',
        )

    def test_render_creation_form(self):
        response = self.client.get("/visualapp/new/")
        self.assertContains(response, "コースの登録", status_code=200)

    def test_create_snippet(self):
        data = {'title': 'タイトル', 'start': 'スタート', 'spot1': '訪問1', 'spot2': '訪問2', 'spot3': '訪問3'}
        self.client.post("/visualapp/new/", data)
        cource = Cource.objects.get(title='タイトル')
        self.assertEqual('スタート', cource.start)
        self.assertEqual('訪問1', cource.spot1)
        self.assertEqual('訪問2', cource.spot2)
        self.assertEqual('訪問3', cource.spot3)

class TopPageTest(TestCase):
    def test_top_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, 'ビジュアルVNS' ,status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'visualapp/top.html')

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Salesman, Route
from .forms import CityForm, SalesmanForm, RouteForm
from .serializers import CitySerializer, SalesmanSerializer, RouteSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Salesmanの登録と一覧
def salesman_list(request):
    salesmen = Salesman.objects.all()
    if request.method == "POST":
        form = SalesmanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesman_list')
    else:
        form = SalesmanForm()
    return render(request, 'salesman_list.html', {'salesmen': salesmen, 'form': form})

# Cityの登録と一覧
def city_list(request):
    cities = City.objects.all()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_list')
    else:
        form = CityForm()
    return render(request, 'city_list.html', {'cities': cities, 'form': form})

# Routeの登録と一覧
def route_list(request):
    routes = Route.objects.all()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm()
    return render(request, 'route_list.html', {'routes': routes, 'form': form})

class SalesmanViewSet(viewsets.ModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        cities = data.pop("cities", [])
        salesmen = data.pop("salesmen", [])

        route = Route.objects.create(name=data["name"])
        route.cities.set(cities)  # ManyToManyField のセット
        route.salesmen.set(salesmen)
        # route.description = data["description"]

        serializer = self.get_serializer(route)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@csrf_exempt
def api_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("受信したデータ:", data)

            # 🔹 送信された City ID と Salesman ID をチェック
            # existing_cities = list(City.objects.filter(id__in=data["cities"]))
            # existing_salesmen = list(Salesman.objects.filter(id__in=data["salesmen"]))

            # if len(existing_cities) != len(data["cities"]):
            #     return JsonResponse({"error": "存在しないCity IDが含まれています"}, status=400)
            # if len(existing_salesmen) != len(data["salesmen"]):
            #     return JsonResponse({"error": "存在しないSalesman IDが含まれています"}, status=400)

            # 🔹 Routeを作成
            route = Route.objects.create(name=data["name"])
            route.cities.set(data["cities"])  # ManyToManyField に関連付け
            route.salesmen.set(data["salesmen"])  # ManyToManyField に関連付け

            return JsonResponse({
                "message": "ok",
                "route_id": route.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "無効なJSONデータ"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "POSTメソッドを使用してください"}, status=405)

@csrf_exempt
def api_delete_route(request, route_id):
    if request.method == "DELETE":
        try:
            route = get_object_or_404(Route, id=route_id)  # ID に対応する Route を取得
            route.delete()  # 削除
            return JsonResponse({"message": f"Route ID {route_id} を削除しました"}, status=204)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "DELETEメソッドを使用してください"}, status=405)

@csrf_exempt
def api_update_route(request, route_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("受信したデータ:", data)

            # 🔹 指定された ID の Route を取得
            route = get_object_or_404(Route, id=route_id)

            # 🔹 送信された City ID と Salesman ID をチェック
            # existing_cities = list(City.objects.filter(id__in=data["cities"]))
            # existing_salesmen = list(Salesman.objects.filter(id__in=data["salesmen"]))

            # if len(existing_cities) != len(data["cities"]):
            #     return JsonResponse({"error": "存在しないCity IDが含まれています"}, status=400)
            # if len(existing_salesmen) != len(data["salesmen"]):
            #     return JsonResponse({"error": "存在しないSalesman IDが含まれています"}, status=400)

            # 🔹 Routeの情報を更新
            route.name = data["name"]
            route.cities.set(data["cities"])  # ManyToManyField に関連付け
            route.salesmen.set(data["salesmen"])  # ManyToManyField に関連付け
            route.save()

            return JsonResponse({
                "message": f"Route ID {route_id} を更新しました",
                "route_id": route.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "無効なJSONデータ"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "PUTメソッドを使用してください"}, status=405)


@csrf_exempt
def api_get_routes(request):
    if request.method == "GET":
        try:
            routes = Route.objects.all()

            # 🔹 cities と salesmen をリストとしてまとめる
            route_list = [
                {
                    "id": route.uuid,
                    "name": route.name,
                    "cities_id": list(route.cities.values_list("id", flat=True)),  # ManyToManyField をリスト化
                    "salesmen_id": list(route.salesmen.values_list("id", flat=True)),  # ManyToManyField をリスト化
                    "description": route.description,  # 🔹 description を追加
                    "created_by": route.created_by.username,  # 🔹 作成者を返す
                    "created_at": route.created_at.isoformat(),  # 🔹 日付をISOフォーマットで返す
                    "update_at": route.update_at.isoformat(),  # 🔹 更新日時を追加
                }
                for route in routes
            ]

            return JsonResponse(route_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "GETメソッドを使用してください"}, status=405)


@csrf_exempt
def api_get_cities(request):
    if request.method == "GET":
        try:
            cities = City.objects.all()

            # 🔹 各 City に紐づく Salesman をリストとしてまとめる
            city_list = [
                {
                    "id": city.id,
                    "name": city.name,
                    "salesman_id": city.salesman.id
                }
                for city in cities
            ]

            return JsonResponse(city_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "GETメソッドを使用してください"}, status=405)

@csrf_exempt
def api_get_salesmen(request):
    if request.method == "GET":
        try:
            salesmen = Salesman.objects.all()

            # 🔹 cities と salesmen をリストとしてまとめる
            salesman_list = [
                {
                    "id": salesman.id,
                    "name": salesman.name,
                }
                for salesman in salesmen
            ]

            return JsonResponse(salesman_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "GETメソッドを使用してください"}, status=405)

@csrf_exempt
def api_set_route(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            route_name = data.get("name", "")
            city_ids = data.get("cities_id", [])
            salesman_ids = data.get("salesmen_id", [])

            if not route_name:
                return JsonResponse({"error": "Route名が必要です"}, status=400)

            # Route を作成
            route = Route.objects.create(name=route_name)
            route.cities.set(City.objects.filter(id__in=city_ids))
            route.salesmen.set(Salesman.objects.filter(id__in=salesman_ids))
            route.save()

            return JsonResponse({"success": "Route が追加されました"}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "POSTメソッドを使用してください"}, status=405)

@csrf_exempt
def api_delete_route(request, route_id):
    if request.method == "DELETE":
        try:
            route = Route.objects.get(id=route_id)
            route.delete()
            return JsonResponse({"success": "Route が削除されました"}, status=200)

        except Route.DoesNotExist:
            return JsonResponse({"error": "指定された Route は存在しません"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "DELETEメソッドを使用してください"}, status=405)

@csrf_exempt
def api_delete_city(request, city_id):
    if request.method == "DELETE":
        try:
            city = City.objects.get(id=city_id)
            city.delete()
            return JsonResponse({"success": "City が削除されました"}, status=200)

        except Route.DoesNotExist:
            return JsonResponse({"error": "指定された City は存在しません"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "DELETEメソッドを使用してください"}, status=405)



@csrf_exempt
def api_solve(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            route = Route.objects.create(name=data['name'])
            route.cities.set(City.objects.filter(id__in=data["cities_id"]))
            route.salesmen.set(Salesman.objects.filter(id__in=data["salesmen_id"]))
            routes = Route.objects.all()
            route.save()

            # 🔹 HTML テンプレートをレンダリング
            html_content = render(request, "result.html", {"route": route}).content.decode("utf-8")

            return JsonResponse({"html": html_content}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"サーバーエラー: {str(e)}"}, status=500)

    return JsonResponse({"error": "POSTメソッドを使用してください"}, status=405)
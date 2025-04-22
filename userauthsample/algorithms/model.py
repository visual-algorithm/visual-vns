import googlemaps
import pandas as pd
import itertools
import time

import folium
import polyline

from algorithms import algorithm

class model():
    API_KEY = "AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08"
    gmaps = googlemaps.Client(key=API_KEY)

    salesman_number = 0
    city_number = 0
    addresses = []
    exclusive_cities = [[]]
    shared_cities = []
    distance_matrix = []
    route_id = ""
    

    def __init__(self, route_id, salesman_number, city_number, addresses, exclusive_cities, shared_cities):
        self.route_id = route_id
        self.salesman_number = salesman_number
        self.city_number = city_number
        self.addresses = addresses
        self.exclusive_cities = exclusive_cities
        self.shared_cities = shared_cities


    def get_distance(self, origin, destination, mode="driving"):
        """
        Google Maps Directions API を使って2点間の距離を取得する。

        :param origin: 出発地点の住所または緯度経度
        :param destination: 目的地の住所または緯度経度
        :param mode: 移動手段 ("driving", "walking", "bicycling", "transit")
        :return: 距離（メートル）または None（エラー時）
        """
        try:
            directions = self.gmaps.directions(origin, destination, mode=mode)

            if not directions:
                return None  # ルートが見つからない場合

            route = directions[0]['legs'][0]  # 最初のルートの距離情報を取得
            distance = route["distance"]["value"]  # 距離（メートル）

            return distance

        except googlemaps.exceptions.Timeout:
            print(f"Timeout: {origin} → {destination}")
            return None

        except googlemaps.exceptions.ApiError as e:
            print(f"API Error: {e}")
            return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_distance_matrix(self, addresses, mode="driving", delay=1):
        matrix = {addr: {addr: 0 for addr in addresses} for addr in addresses}  # 初期化 (同じ地点は距離0)

        for origin, destination in itertools.combinations_with_replacement(addresses, 2):
            if origin == destination:
                continue  # 同じ地点なら計算不要

            distance = self.get_distance(origin, destination, mode)
            if distance is None:
                distance = float("inf")  # 取得失敗時は無限大とする

            # 対称性を利用して両方向にセット
            matrix[origin][destination] = distance
            matrix[destination][origin] = distance

            time.sleep(delay)  # APIリクエスト制限を回避するために待機

        # DataFrameに変換
        df = pd.DataFrame(matrix)
        return df.values.tolist()
    
    def solve(self):
        self.distance_matrix = self.get_distance_matrix(self.addresses)
        algo = algorithm.VNS(self.salesman_number, self.city_number, self.distance_matrix, self.exclusive_cities, self.shared_cities)
        optimal_solution = algo.evaluation()

        return optimal_solution

    def get_data(self) -> list:
        optimal = self.solve()

        optimal_address = [[]]
        routes = []

        for route in optimal:
            optimal_address.append([""] * (len(route)))

        del optimal_address[0]


        for i in range(len(optimal)):
            for j in range(len(optimal[i])):
                optimal_address[i][j] = self.addresses[optimal[i][j]]

        for route in optimal_address:
            del(route[0])
            del(route[len(route)-1])

        for i in range(len(optimal_address)):
            d = {"start": self.addresses[0], "waypoints": optimal_address[i], "end": self.addresses[0]}
            routes.append(d)

        # カラーリスト（ルートごとに異なる色を適用）
        colors = ["blue", "red", "green", "purple", "orange"]

        # すべてのルートの座標を格納するリスト
        all_points = []

        # すべてのルートを処理
        for i, route in enumerate(routes):
            # Google Maps API で経路を取得
            directions = self.gmaps.directions(
                origin=route["start"],
                destination=route["end"],
                waypoints=route["waypoints"],
                mode="driving",
                language="ja"
            )

            # 経路データから座標を取得
            route_points = polyline.decode(directions[0]["overview_polyline"]["points"])
            all_points.extend(route_points)  # すべての座標をリストに追加

        # 🌍 地図の表示範囲をすべてのルートが収まるように調整
        sw = [min(p[0] for p in all_points), min(p[1] for p in all_points)]  # 南西端
        ne = [max(p[0] for p in all_points), max(p[1] for p in all_points)]  # 北東端

        # 地図の初期化（適切な拡大率で表示）
        m = folium.Map(location=[(sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2], zoom_start=6)

        # 再度すべてのルートを描画
        for i, route in enumerate(routes):
            directions = self.gmaps.directions(
                origin=route["start"],
                destination=route["end"],
                waypoints=route["waypoints"],
                mode="driving",
                language="ja"
            )

            route_points = polyline.decode(directions[0]["overview_polyline"]["points"])

            # 経路を地図に描画
            folium.PolyLine(
                route_points,
                color=colors[i % len(colors)],  # ルートごとに色を変更
                weight=5,
                opacity=0.7,
                tooltip=f"ルート{i+1}: {route['start']} → {', '.join(route['waypoints'])} → {route['end']}"
            ).add_to(m)

            # 出発地・目的地マーカー
            folium.Marker(route_points[0], popup=f"出発地: {route['start']}", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(route_points[-1], popup=f"目的地: {route['end']}", icon=folium.Icon(color="red")).add_to(m)

        # 地図の表示範囲をすべてのルートが収まるように調整
        m.fit_bounds([sw, ne])

        # 地図をHTMLとして保存
        # name = 'authsample/static/'+str(self.route_id)+'.html'

        name = 'authsample/templates/authsample/'+str(self.route_id)+'.html'

        m.save(name)

        return optimal
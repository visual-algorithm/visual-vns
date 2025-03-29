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
        """
        指定した複数の住所間の距離行列を取得する。

        :param addresses: 住所のリスト（例: ["東京駅", "大阪駅", "名古屋駅"]）
        :param mode: 移動手段 ("driving", "walking", "bicycling", "transit")
        :param delay: APIリクエスト間の待機時間（秒）
        :return: 距離行列（DataFrame）
        """
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

        # self.distance_matrix = [[0, 501104, 348075, 455263, 35945, 22454, 348241, 1088857, 489746, 157664], 
        #                         [501104, 0, 174159, 53994, 483225, 495014, 864145, 611033, 307271, 654311], 
        #                         [348075, 174159, 0, 126017, 329791, 341580, 710711, 759611, 244148, 500877], 
        #                         [455263, 53994, 126017, 0, 437271, 449060, 818191, 638629, 261317, 608357], 
        #                         [35945, 483225, 329791, 437271, 0, 9106, 384538, 1071321, 413909, 195810], 
        #                         [22454, 495014, 341580, 449060, 9106, 0, 374907, 1082652, 515497, 186179], 
        #                         [348241, 864145, 710711, 818191, 384538, 374907, 0, 1451928, 559899, 262260], 
        #                         [1088857, 611033, 759611, 638629, 1071321, 1082652, 1451928, 0, 870890, 1241467], 
        #                         [489746, 307271, 244148, 261317, 413909, 515497, 559899, 870890, 0, 508102], 
        #                         [157664, 654311, 500877, 608357, 195810, 186179, 262260, 1241467, 508102, 0]
        #                         ]

        # print(self.distance_matrix)
        algo = algorithm.VNS(self.salesman_number, self.city_number, self.distance_matrix, self.exclusive_cities, self.shared_cities)
        optimal_solution = algo.evaluation()
        print(optimal_solution)

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


        # 📍 ルートのセット（出発地・経由地・目的地）
        # ex_routes = [
        #     {
        #         "start": "埼玉県秩父市宮側町1-8",
        #         "waypoints": ["埼玉県秩父郡小鹿野町長留2518", "埼玉県秩父市熊木熊木町8-15"],
        #         "end": "埼玉県秩父市宮側町1-8"
        #     },
        #     {
        #         "start": "埼玉県秩父市宮側町1-8",
        #         "waypoints": ["埼玉県秩父市番場町1-1"],
        #         "end": "埼玉県秩父市宮側町1-8"
        #     }
        # ]

        # 🌈 カラーリスト（ルートごとに異なる色を適用）
        colors = ["blue", "red", "green", "purple", "orange"]

        # 📌 すべてのルートの座標を格納するリスト
        all_points = []

        # 🔄 すべてのルートを処理
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
        name = 'restpractice/static/'+str(self.route_id)+'.html'
        m.save(name)

        return optimal


# addresses = ["東京駅", "大阪駅", "名古屋駅"]
# salesman_number = 2
# city_number = 10
# addresses = ["東京駅", "大阪駅", "名古屋駅", "京都駅", "新横浜駅", "川崎駅", "仙台駅", "博多駅", "金沢駅", "日光駅"]

# exclusive_cities = [[1,2], [3,4]]
# shared_cities = [5,6,7,8,9]



# m = model(2, 10, addresses, exclusive_cities, shared_cities)
# m.solve()

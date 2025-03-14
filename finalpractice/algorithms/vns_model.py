import googlemaps
import googlemaps.distance_matrix
import folium
import polyline

from algorithms import algorithm
import copy

class model():
    API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'
    google_client: googlemaps.Client

    origin = ""
    waypoints = []
    cities = []
    exclusive_cities = [[]]
    shared_cities = []
    algo: algorithm.VNS
    dis_matrix: list[list]

    def __init__(self, origin: str, waypoints: list[str], salesman_number: int, exclusive_cities, shared_cities):
        self.origin = origin
        self.waypoints = waypoints
        self.cities = copy.deepcopy(waypoints)
        self.cities.insert(0, origin)
        self.google_client = googlemaps.Client(key=self.API_KEY)
        self.exclusive_cities = exclusive_cities
        self.shared_cities = shared_cities

        result = googlemaps.distance_matrix.distance_matrix(self.google_client, self.waypoints, self.waypoints)
        mtrx = [[0]*len(self.cities) for i in range((len(self.cities)))]

        result = "a"

        if "rows" in result:
            for i, row in enumerate(result["rows"]):
                for j, element in enumerate(row["elements"]):
                    if element["status"] == "OK":
                        distance = element["distance"]["text"]
                        duration = element["duration"]["text"]
                        distance = str(distance)
                        if ' m' in distance:
                            contents = distance.split(' ')
                            val = float(contents[0]) * 0.001
                            if val < 0.01:
                                val = 0.0
                            distance = str(val) +' km'
                            
                        distance = str(distance).replace(' km', '')

                        mtrx[i][j] = float(distance)
                    else:
                        print(f"  → 目的地: {self.destinations[j]}, ルートが見つかりません。")
        #else:
        #    print("APIレスポンスに問題があります。")

        # mtrx = [[0.0, 0.4, 1.1, 6.5], [0.5, 0.0, 1.0, 5.8], [1.1, 1.4, 0.0, 5.7], [6.5, 6.7, 5.8, 0.0]]
        self.dis_matrix = mtrx
        self.algo = algorithm.VNS(salesman_number, self.dis_matrix)
        

    def solve(self):
        algo = algorithm.VNS(2, self.dis_matrix)
        algo.set_cities(self.exclusive_cities, self.shared_cities)
        solution = algo.evaluation()
        return solution
    
    def get_data(self):
        optimal = self.solve()

        print(self.origin)

        optimal_address = [[]]
        routes = []

        for route in optimal:
            optimal_address.append([""] * (len(route)))

        del optimal_address[0]


        for i in range(len(optimal)):
            for j in range(len(optimal[i])):
                optimal_address[i][j] = self.cities[optimal[i][j]]

        for route in optimal_address:
            del(route[0])
            del(route[len(route)-1])

        for i in range(len(optimal_address)):
            d = {"start": self.origin, "waypoints": optimal_address[i], "end": self.origin}
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
            directions = self.google_client.directions(
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
            directions = self.google_client.directions(
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
        m.save("practice/static/multiple_routes_map.html")

        # print("✅ 地図を multiple_routes_map.html に保存しました！（ルートが全て見える状態）")


# origin = "埼玉県秩父市宮側町1-8"
# waypoints = ["埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]

# m = model(origin, waypoints, 2, [[1], [2]], [3])

# m.get_data()
import googlemaps
import folium
import polyline

# 🔑 Google Maps APIキーを設定
API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'
gmaps = googlemaps.Client(key=API_KEY)

# 📍 ルートのセット（出発地・経由地・目的地）
routes = [
    {
        "start": "埼玉県秩父市宮側町1-8",
        "waypoints": ["埼玉県秩父郡小鹿野町長留2518", "埼玉県秩父市熊木熊木町8-15"],
        "end": "埼玉県秩父市宮側町1-8"
    },
    {
        "start": "埼玉県秩父市宮側町1-8",
        "waypoints": ["埼玉県秩父市番場町1-1"],
        "end": "埼玉県秩父市宮側町1-8"
    }
]

# 🌈 カラーリスト（ルートごとに異なる色を適用）
colors = ["blue", "red", "green", "purple", "orange"]

# 📌 すべてのルートの座標を格納するリスト
all_points = []

# 🔄 すべてのルートを処理
for i, route in enumerate(routes):
    # Google Maps API で経路を取得
    directions = gmaps.directions(
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
    directions = gmaps.directions(
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
m.save("multiple_routes_map.html")

print("✅ 地図を multiple_routes_map.html に保存しました！（ルートが全て見える状態）")

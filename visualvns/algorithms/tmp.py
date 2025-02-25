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

# 地図の初期化（最初の出発地を中心）
m = folium.Map(location=[35.681236, 139.767125], zoom_start=14)

# 🌈 カラーリスト（ルートごとに異なる色を適用）
colors = ["blue", "red", "green", "purple", "orange"]

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

# 地図をHTMLとして保存
m.save("multiple_routes_map.html")

print("✅ 地図を multiple_routes_map.html に保存しました！")

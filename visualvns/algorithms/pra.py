import googlemaps
import folium
import polyline

# Google Maps APIキー（取得したものに置き換えてください）
API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'

# googlemaps クライアントの初期化
gmaps = googlemaps.Client(key=API_KEY)

def get_directions(origin, destination, waypoints):
    """Google Maps Directions API から経路情報を取得"""
    directions = gmaps.directions(
        origin, 
        destination, 
        waypoints=waypoints,
        mode="driving",
        optimize_waypoints=True
    )

    if directions:
        return directions[0]  # 最適なルートを取得
    else:
        print("ルートが見つかりませんでした。")
        return None

def plot_route_on_map(route, map_filename="route_map.html"):
    """取得したルート情報を folium を使って地図上に描画"""
    # 地図の中心を出発地に設定
    start_location = route["legs"][0]["start_location"]
    map_center = [start_location["lat"], start_location["lng"]]
    route_map = folium.Map(location=map_center, zoom_start=14)

    # ポリラインデータ（エンコードされた経路）をデコードして座標リストに変換
    polyline_points = polyline.decode(route["overview_polyline"]["points"])

    # ポリライン（ルート）を地図上に描画
    folium.PolyLine(polyline_points, color="blue", weight=5, opacity=0.7).add_to(route_map)

    # 出発地をマーカー表示
    folium.Marker(
        location=[route["legs"][0]["start_location"]["lat"], route["legs"][0]["start_location"]["lng"]],
        popup="出発地",
        icon=folium.Icon(color="green"),
    ).add_to(route_map)

    # 経由地と目的地をマーカー表示
    for leg in route["legs"]:
        folium.Marker(
            location=[leg["end_location"]["lat"], leg["end_location"]["lng"]],
            popup=leg["end_address"],
            icon=folium.Icon(color="red"),
        ).add_to(route_map)

    # HTMLファイルに保存
    route_map.save(map_filename)
    print(f"地図を {map_filename} に保存しました。ブラウザで開いて確認できます。")

# 出発地・目的地・経由地を設定
origin = "埼玉県秩父市宮側町1-8"
destination = "埼玉県秩父市宮側町1-8"
waypoints = ["埼玉県秩父郡小鹿野町長留2518", "埼玉県秩父市熊木熊木町8-15"]

# 経路を取得
route_data = get_directions(origin, destination, waypoints)

if route_data:
    # 取得した経路を地図にプロット
    plot_route_on_map(route_data)

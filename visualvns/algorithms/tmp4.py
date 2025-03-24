import googlemaps
import pandas as pd
import itertools
import time

# Google Maps APIキー（自分のAPIキーを入力）
API_KEY = "AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08"

# Google Maps クライアントの作成
gmaps = googlemaps.Client(key=API_KEY)

def get_distance(origin, destination, mode="driving"):
    print("called.")
    """
    Google Maps Directions API を使って2点間の距離を取得する。

    :param origin: 出発地点の住所または緯度経度
    :param destination: 目的地の住所または緯度経度
    :param mode: 移動手段 ("driving", "walking", "bicycling", "transit")
    :return: 距離（メートル）または None（エラー時）
    """
    try:
        directions = gmaps.directions(origin, destination, mode=mode)

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

def get_distance_matrix(addresses, mode="driving", delay=1):
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

        distance = get_distance(origin, destination, mode)
        if distance is None:
            distance = float("inf")  # 取得失敗時は無限大とする

        # 対称性を利用して両方向にセット
        matrix[origin][destination] = distance
        matrix[destination][origin] = distance

        time.sleep(delay)  # APIリクエスト制限を回避するために待機

    # DataFrameに変換
    df = pd.DataFrame(matrix)
    return df

# 使用例
# addresses = ["東京駅", "大阪駅", "名古屋駅"]
addresses = ["東京駅", "大阪駅", "名古屋駅", "京都駅", "新横浜駅", "川崎駅", "仙台駅", "博多駅", "金沢駅", "日光駅"]
distance_matrix = get_distance_matrix(addresses)

# 結果の表示
print(distance_matrix)

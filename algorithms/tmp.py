import googlemaps.client
import googlemaps.distance_matrix

# APIキーを設定
API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'
# API_KEY = 'AIzaSyB6VVjbVyUr9WsIzgymu0SwDwT_FoPmrKU'
gc = googlemaps.Client(key=API_KEY)
# 出発地と目的地を設定
# origins = ["埼玉県秩父市宮側町1-8", "埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]
origins = ["埼玉県秩父市宮側町1-8"]
destinations = ["埼玉県秩父市宮側町1-8", "埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]

# Distance Matrix API を呼び出す
result = googlemaps.distance_matrix.distance_matrix(client=gc, origins=origins, destinations=destinations, mode="driving")

W = [[0]*len(destinations) for i in range(len(destinations))]

# if "rows" in result:
#     for i, row in enumerate(result["rows"]):
#         print(f"\n出発地: {origins[i]}")
#         for j, element in enumerate(row["elements"]):
#             if element["status"] == "OK":
#                 distance = element["distance"]["text"]
#                 duration = element["duration"]["text"]
#                 print(f"  → 目的地: {destinations[j]}, 距離: {distance}, 所要時間: {duration}")
#                 # distance = str(distance)
#                 # if ' m' in distance:
#                 #     contents = distance.split(' ')
#                 #     val = float(contents[0]) * 0.001
#                 #     distance = str(val) +' km'
#                 # distance = str(distance).replace(' km', '')
#                 # W[0][i] = float(distance)
#             else:
#                 print(f"  → 目的地: {destinations[j]}, ルートが見つかりません。")
# else:
#     print("APIレスポンスに問題があります。")

# 結果を表示
if "rows" in result and result["rows"]:
    row = result["rows"][0]  # 出発地は1つなので `rows[0]` のみ
    for i, element in enumerate(row["elements"]):
        if element["status"] == "OK":
            distance = element["distance"]["text"]
            duration = element["duration"]["text"]
            distance = str(distance)
            if ' m' in distance:
                contents = distance.split(' ')
                val = float(contents[0]) * 0.001
                distance = str(val) +' km'
            distance = str(distance).replace(' km', '')
            W[0][i] = float(distance)
        else:
            print(f"  → 目的地: {destinations[i]}, ルートが見つかりません。")
else:
    print("APIレスポンスに問題があります。")
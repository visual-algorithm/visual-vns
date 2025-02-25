import googlemaps
import googlemaps.distance_matrix

import algorithm

class model():
    API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'
    google_client: googlemaps.Client

    origins = []
    destinations: list
    dis_matrix: list[list]

    def __init__(self, origin:str, waypoints :list[str]):
        self.google_client = googlemaps.Client(key=self.API_KEY)
        self.origins.append(origin)
        for c in waypoints:
            self.origins.append(c)
        self.destinations = self.origins

        # result = googlemaps.distance_matrix.distance_matrix(self.google_client, self.origins, self.destinations)
        # mtrx = [[0]*len(self.destinations) for i in range((len(self.destinations)))]

        # if "rows" in result:
        #     for i, row in enumerate(result["rows"]):
        #         for j, element in enumerate(row["elements"]):
        #             if element["status"] == "OK":
        #                 distance = element["distance"]["text"]
        #                 duration = element["duration"]["text"]
        #                 distance = str(distance)
        #                 if ' m' in distance:
        #                     contents = distance.split(' ')
        #                     val = float(contents[0]) * 0.001
        #                     if val < 0.01:
        #                         val = 0.0
        #                     distance = str(val) +' km'
                            
        #                 distance = str(distance).replace(' km', '')

        #                 mtrx[i][j] = float(distance)
        #             else:
        #                 print(f"  → 目的地: {self.destinations[j]}, ルートが見つかりません。")
        # else:
        #     print("APIレスポンスに問題があります。")

        mtrx = [[0.0, 0.4, 1.1, 6.5], [0.5, 0.0, 1.0, 5.8], [1.1, 1.4, 0.0, 5.7], [6.5, 6.7, 5.8, 0.0]]
        self.dis_matrix = mtrx
        

    def solve(self):
        algo = algorithm.VNS(2, self.dis_matrix)
        algo.set_cities([[1], [2]], [3])
        solution = algo.evaluation()
        return solution


origin = "埼玉県秩父市宮側町1-8"
waypoints = ["埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]
m = model(origin, waypoints)
optimal = m.solve()

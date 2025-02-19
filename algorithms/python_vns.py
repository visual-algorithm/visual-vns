import random
import copy
import googlemaps.client
import googlemaps.distance_matrix


CTTY_NUMBER = 10
SALESMAN_NUMBER = 2
DEPOT_NUMBER = 0

W = [
    [0, 21.4709, 12.0416, 19.2354, 23.4307, 14.2127, 17.4642, 10.6301, 12.8062, 10, 13.4536, ],
    [21.4709, 0, 18.1108, 12.2066, 5.09902, 10.0499, 36.7696, 31.9061, 22.8254, 27.5862, 21.0238, ],
    [12.0416, 18.1108, 0, 9.43398, 17.2627, 8.06226, 29.1204, 21.0238, 23.0868, 22.0227, 22.8473, ],
    [19.2354, 12.2066, 9.43398, 0, 9.21954, 6, 36.6742, 29.4109, 27.0185, 28.4605, 26.0192, ],
    [23.4307, 5.09902, 17.2627, 9.21954, 0, 9.84886, 39.8246, 34.0588, 26.9258, 30.8058, 25.2982, ],
    [14.2127, 10.0499, 8.06226, 6, 9.84886, 0, 31.3847, 24.7588, 21.0238, 22.8473, 20.025, ],
    [17.4642, 36.7696, 29.1204, 36.6742, 39.8246, 31.3847, 0, 9.05539, 16.1555, 9.21954, 18.3848, ],
    [10.6301, 31.9061, 21.0238, 29.4109, 34.0588, 24.7588, 9.05539, 0, 16.2788, 8.544, 18.1108, ],
    [12.8062, 22.8254, 23.0868, 27.0185, 26.9258, 21.0238, 16.1555, 16.2788, 0, 8, 2.23607, ],
    [10, 27.5862, 22.0227, 28.4605, 30.8058, 22.8473, 9.21954, 8.544, 8, 0, 10.0499, ],
    [13.4536, 21.0238, 22.8473, 26.0192, 25.2982, 20.025, 18.3848, 18.1108, 2.23607, 10.0499, 0, ],
]

T = [
    [1],
    [2],
]

shared_cities = [3]

def greedy_initialization():
    k = 0
    v = 0
    tk = []
    R = [[] for i in range(SALESMAN_NUMBER)] 
    while k < SALESMAN_NUMBER:
        tk = T[k]
        rk = []
        v = DEPOT_NUMBER
        rk.append(DEPOT_NUMBER)
        for i in range(len(T[k])):
            closest_length = 10000000
            closest_city = DEPOT_NUMBER
            for j in range(len(tk)):
                pos1 = v
                pos2 = tk[j]
                tkj_length = W[pos1][pos2]
                if tkj_length < closest_length:
                    closest_length = tkj_length
                    closest_city = pos2
                
            rk.append(closest_city)
            v = closest_city
            tk.remove(closest_city)
        rk.append(DEPOT_NUMBER)
        R[k] = rk
        k = k + 1
    
    ex_route = []
    new_route = []
    better_routes = [[] for i in range(SALESMAN_NUMBER)]
    ex_route_lengths = [0] * SALESMAN_NUMBER
    new_route_lengths = [0] * SALESMAN_NUMBER
    min_route_lengths = [100000] * SALESMAN_NUMBER
    for i in range(len(shared_cities)):
        ex_route = []
        new_route = []
        better_routes = [[] for i in range(SALESMAN_NUMBER)]
        ex_route_lengths = [0] * SALESMAN_NUMBER
        new_route_lengths = [0] * SALESMAN_NUMBER
        min_route_lengths = [100000] * SALESMAN_NUMBER
        k = 0
        while k < SALESMAN_NUMBER:
            ex_route = R[k]
            for j in range(1, len(ex_route)):
                ex_route_lengths[k] += W[ex_route[j-1]][ex_route[j]]
            for j in range(1, len(ex_route)):
                new_route = copy.deepcopy(R[k]) #参照渡しになってる！
                new_route_lengths[k] = 0
                a = shared_cities[i]
                new_route.insert(j, a)
                for l in range(1, len(new_route)):
                    new_route_lengths[k] += W[new_route[l-1]][new_route[l]]
                if new_route_lengths[k] < min_route_lengths[k]:
                    min_route_lengths[k] = new_route_lengths[k]
                    better_routes[k] = new_route
            k = k + 1
        dif = 0
        min_dif = 100000
        min_salesman = 0
        for j in range(len(min_route_lengths)):
            dif = min_route_lengths[j] - ex_route_lengths[j]
            if dif < min_dif:
                min_dif = dif
                min_salesman = j
        R[min_salesman] = better_routes[min_salesman]
    return R

def shaking(x, s_max):
    N = [[[]]]
    new_x = [[] for i in range(SALESMAN_NUMBER)]
    cities_numbers = []
    for route in x:
        cities_numbers.append(len(route))

    minimum_cities_number = min(cities_numbers)
    minimum_cities_index = cities_numbers.index(min(cities_numbers))
    maximum_cities_index = cities_numbers.index(max(cities_numbers))

    s = k = pos1 = pos2 = relocated_city_number = r = 0

    while s < s_max:
        new_x = copy.deepcopy(x)
        r = random.random()
        k = random.randint(0, SALESMAN_NUMBER-1)
        rk = copy.deepcopy(x[k])
        if minimum_cities_number <= 3:
            k = maximum_cities_index
            rk = copy.deepcopy(x[k])
        if r < 0.5: 
            pos1 = random.randint(1, len(rk)-2)
            pos2 = random.randint(1, len(rk)-2)
            while pos1 == pos2:
                pos2 = random.randint(1, len(rk)-2)
            if pos1 > pos2:
                tmp = pos1
                pos1 = pos2
                pos2 = tmp
            tmp = rk[pos1]
            rk[pos1] = rk[pos2]
            rk[pos2] = tmp
            new_x[k] = copy.deepcopy(rk)
            
        else:
            pos1 = random.randint(1, len(rk)-2)
            relocated_city_number = rk[pos1]
            rk.remove(relocated_city_number)
            pos2 = random.randint(1, len(rk)-2)
            rk.insert(pos2, relocated_city_number)
            new_x[k] = copy.deepcopy(rk)
        N.append(new_x)
        s = s + 1
    fitnesses = [0] * s_max
    route_lengths = [0] * s_max

    del N[0]
    for i in range(len(N)):
        for j in range(len(N[i])):
            for l in range(1, len(N[i][j])):
                route_lengths[i] += W[N[i][j][l]][N[i][j][l-1]]

    for i in range(len(route_lengths)):
        fitnesses[i] = 1 / (1 + route_lengths[i])
    
    total = 0
    for i in range(len(fitnesses)):
        total += fitnesses[i]
    
    c_sum = [0] * len(fitnesses)
    c_sum[0] = fitnesses[0]
    for i in range(1, len(fitnesses)):
        c_sum[i] = c_sum[i - 1] + fitnesses[i]
    
    trial = 100
    c_sum.insert(0, 0)
    count = [0] * len(c_sum)
    for i in range(trial):
        r = random.random() * total
        low = 0
        high = len(c_sum) - 1
        mid = 0
        while low <= high:
            mid = int((low + high) / 2)
            if c_sum[mid] <= r and r <= c_sum[mid+1]:
                break
            elif c_sum[mid+1] < r:
                low = mid + 1
            else:
                high = mid - 1
        count[mid + 1] += 1
    del count[0]

    best_index = count.index(max(count))
    

    return N[best_index]

def local_search(x):
    exclusive_S = [[] for i in range(SALESMAN_NUMBER)]
    shared_S = []
    rest_x = [[] for i in range(SALESMAN_NUMBER)]
    k = 0
    η = 0.1
    r = 0
    removed_city = 0
    for i in range(len(x)):
        rest_x[i] = copy.deepcopy(x[i])
        for j in range(1, len(x[i])-1):
            r = random.random()
            if r < η:
                removed_city = x[i][j]
                rest_x[i].remove(removed_city)
                if removed_city in shared_cities:
                    shared_S.append(removed_city)
                else:
                    exclusive_S[i].append(removed_city)

    k = a = 0
    new_route = []
    exclusive_better_routes = [[] for i in range(SALESMAN_NUMBER)]

    exclusive_better_routes = rest_x

    for i in range(len(exclusive_S)):
        for j in range(len(exclusive_S[i])):
            min_length = [100000] * SALESMAN_NUMBER
            for l in range(1, len(rest_x[i])):
                ex_length = [0] * SALESMAN_NUMBER
                new_route = copy.deepcopy(rest_x[i])
                a = exclusive_S[i][j]
                new_route.insert(l, a)
                for o in range(1, len(new_route)):
                    ex_length[i] += W[new_route[o-1]][new_route[o]]
                if ex_length[i] < min_length[i]:
                    min_length[i] = ex_length[i]
                    exclusive_better_routes[i] = copy.deepcopy(new_route)
            rest_x = copy.deepcopy(exclusive_better_routes)
    
    better_routes = [[] for i in range(SALESMAN_NUMBER)]
    best_routes = [[] for i in range(SALESMAN_NUMBER)]
    new_length = [0] * SALESMAN_NUMBER

    best_routes = copy.deepcopy(rest_x)
    for i in range(len(shared_S)):
        ex_length = [0] * SALESMAN_NUMBER
        new_length = [0] * SALESMAN_NUMBER
        min_length = [100000] * SALESMAN_NUMBER
        k = 0
        while k < SALESMAN_NUMBER:
            better_routes[k] = copy.deepcopy(best_routes[k])
            for j in range(1, len(better_routes)):
                new_route = copy.deepcopy(best_routes[k])
                new_length[k] = 0
                a = shared_S[i]
                new_route.insert(j, a)

                for l in range(1, len(new_route)):
                    new_length[k] += W[new_route[l-1]][new_route[l]]
                
                if new_length[k] < min_length[k]:
                    min_length[k] = new_length[k]
                    better_routes[k] = copy.deepcopy(new_route)
            k = k + 1
        
        dif = 0
        min_dif = 100000
        min_salesman = 0
        for j in range(0, len(min_length)):
            dif = min_length[j] - ex_length[j]
            if dif < min_dif:
                min_dif = dif
                min_salesman = j
        
        best_routes[min_salesman] = copy.deepcopy(better_routes[min_salesman])


    index = pos1 = pos2 = 0
    two_opted_length = min_two_opted_length = 0
    reversed_cities = []
    better_route = []
    two_opted_route = [0] * SALESMAN_NUMBER


    for i in range(0, len(best_routes)):
        min_two_opted_length = 100000
        better_route = copy.deepcopy(best_routes[i])
        for j in range(1, len(best_routes[i])-2):
            two_opted_route = copy.deepcopy(best_routes[i])
            for l in range(j, len(best_routes[i])-1):
                for o in range(j, l+1):
                    reversed_cities.append(best_routes[i][o])
                reversed_cities.reverse()
                index = 0
                for o in range(j, l+1):
                    two_opted_route[o] = reversed_cities[index]
                    index = index + 1
                two_opted_length = 0
                for o in range(1, len(two_opted_route)):
                    two_opted_length += W[two_opted_route[o-1]][two_opted_route[o]]
                if two_opted_length < min_two_opted_length:
                    min_two_opted_length = two_opted_length
                    better_route = copy.deepcopy(two_opted_route)
        best_routes[i] = copy.deepcopy(better_route)
    return best_routes

def evaluation():
    # APIキーを設定
    API_KEY = 'AIzaSyC_B5d5cMEfsU1AfJuRrd3NgS4tBwGfP08'
    gc = googlemaps.Client(key=API_KEY)
    # 出発地と目的地を設定
    origins = ["埼玉県秩父市宮側町1-8", "埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]
    # origins = ["埼玉県秩父市宮側町1-8"]
    destinations = ["埼玉県秩父市宮側町1-8", "埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]

    # Distance Matrix API を呼び出す
    # result = googlemaps.distance_matrix.distance_matrix(client=gc, origins=origins, destinations=destinations, mode="driving")

    # mtrx = [[0]*len(destinations) for i in range(len(destinations))]

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
    #                 print(f"  → 目的地: {destinations[j]}, ルートが見つかりません。")
    # else:
    #     print("APIレスポンスに問題があります。")

    # W = mtrx
    W = [
        [0.0, 0.4, 1.1, 6.5], 
        [0.5, 0.0, 1.0, 5.8], 
        [1.1, 1.4, 0.0, 5.7], 
        [6.5, 6.7, 5.8, 0.0]
    ]

    CITY_NUMBER = len(W)
    
    initial_solution = greedy_initialization()

    print(initial_solution)

    initial_solution_lengths = [0.0] * SALESMAN_NUMBER
    for i in range(len(initial_solution)):
        for j in range(1, len(initial_solution[i])):
            initial_solution_lengths[i] += W[initial_solution[i][j-1]][initial_solution[i][j]]

    initial_value = sum(initial_solution_lengths)
    print(initial_value)

    optimal_solution = [[] for i in range(SALESMAN_NUMBER)]
    optimal_solution = initial_solution
    min_value = initial_value

    cnt = 0
    all_cnt = 0
    while cnt < 10000:
        shaked_solution = shaking(initial_solution, 1)
        better_solution = local_search(shaked_solution)

        solution_lengths = [0.0] * SALESMAN_NUMBER
        for i in range(len(better_solution)):
            for j in range(1, len(better_solution[i])):
                solution_lengths[i] += W[better_solution[i][j-1]][better_solution[i][j]]
        
        value = sum(solution_lengths)

        if value < min_value:
            min_value = value
            optimal_solution = better_solution
            cnt = 0
            print(min_value)
        
        cnt = cnt + 1
        all_cnt = all_cnt + 1
    
    print("optimal value is "+str(min_value))
    print("optimal solution is ")
    print(optimal_solution)
    for route in optimal_solution:
        for city in route:
              print(destinations[city], end=', ')
        print()
    print("all_cnt is "+str(all_cnt))



evaluation()


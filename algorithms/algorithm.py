import copy
import random
import googlemaps

class VNS():
    city_number: int
    salesman_number: int
    depot_number = 0 # can be changed?
    distance_matrix: list[list]
    exclusive_cities: list[list]
    shared_cities: list
    max_solution_number = 10

    def __init__(self, salesman_number, distance_matrix):
        self.city_number = len(distance_matrix) - 1
        self.salesman_number = salesman_number
        self.distance_matrix = distance_matrix
    
    def set_cities(self, exclusive_cities, shared_cities):
        self.exclusive_cities = exclusive_cities
        self.shared_cities = shared_cities

    def greedy_initialization(self):
        k = 0
        v = 0
        tk = []
        R = [[] for i in range(self.salesman_number)] 
        while k < self.salesman_number:
            tk = self.exclusive_cities[k]
            rk = []
            v = self.depot_number
            rk.append(self.depot_number)
            for i in range(len(self.exclusive_cities[k])):
                closest_length = 10000000
                closest_city = self.depot_number
                for j in range(len(tk)):
                    pos1 = v
                    pos2 = tk[j]
                    tkj_length = self.distance_matrix[pos1][pos2]
                    if tkj_length < closest_length:
                        closest_length = tkj_length
                        closest_city = pos2
                    
                rk.append(closest_city)
                v = closest_city
                tk.remove(closest_city)
            rk.append(self.depot_number)
            R[k] = rk
            k = k + 1
        
        ex_route = []
        new_route = []
        better_routes = [[] for i in range(self.salesman_number)]
        ex_route_lengths = [0] * self.salesman_number
        new_route_lengths = [0] * self.salesman_number
        min_route_lengths = [100000] * self.salesman_number
        for i in range(len(self.shared_cities)):
            ex_route = []
            new_route = []
            better_routes = [[] for i in range(self.salesman_number)]
            ex_route_lengths = [0] * self.salesman_number
            new_route_lengths = [0] * self.salesman_number
            min_route_lengths = [100000] * self.salesman_number
            k = 0
            while k < self.salesman_number:
                ex_route = R[k]
                for j in range(1, len(ex_route)):
                    ex_route_lengths[k] += self.distance_matrix[ex_route[j-1]][ex_route[j]]
                for j in range(1, len(ex_route)):
                    new_route = copy.deepcopy(R[k]) #参照渡しになってる！
                    new_route_lengths[k] = 0
                    a = self.shared_cities[i]
                    new_route.insert(j, a)
                    for l in range(1, len(new_route)):
                        new_route_lengths[k] += self.distance_matrix[new_route[l-1]][new_route[l]]
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
    
    def shaking(self, x:list[list]):
        N = [[[]]]
        new_x = [[] for i in range(self.salesman_number)]
        cities_numbers = []
        for route in x:
            cities_numbers.append(len(route))

        minimum_cities_number = min(cities_numbers)
        minimum_cities_index = cities_numbers.index(min(cities_numbers))
        maximum_cities_index = cities_numbers.index(max(cities_numbers))

        s = k = pos1 = pos2 = relocated_city_number = r = 0

        while s < self.max_solution_number:
            new_x = copy.deepcopy(x)
            r = random.random()
            k = random.randint(0, self.salesman_number-1)
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
        fitnesses = [0] * self.max_solution_number
        route_lengths = [0] * self.max_solution_number

        del N[0]
        for i in range(len(N)):
            for j in range(len(N[i])):
                for l in range(1, len(N[i][j])):
                    route_lengths[i] += self.distance_matrix[N[i][j][l]][N[i][j][l-1]]

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

    def local_search(self, x:list[list]):
        exclusive_S = [[] for i in range(self.salesman_number)]
        shared_S = []
        rest_x = [[] for i in range(self.salesman_number)]
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
                    if removed_city in self.shared_cities:
                        shared_S.append(removed_city)
                    else:
                        exclusive_S[i].append(removed_city)

        k = a = 0
        new_route = []
        exclusive_better_routes = [[] for i in range(self.salesman_number)]

        exclusive_better_routes = rest_x

        for i in range(len(exclusive_S)):
            for j in range(len(exclusive_S[i])):
                min_length = [100000] * self.salesman_number
                for l in range(1, len(rest_x[i])):
                    ex_length = [0] * self.salesman_number
                    new_route = copy.deepcopy(rest_x[i])
                    a = exclusive_S[i][j]
                    new_route.insert(l, a)
                    for o in range(1, len(new_route)):
                        ex_length[i] += self.distance_matrix[new_route[o-1]][new_route[o]]
                    if ex_length[i] < min_length[i]:
                        min_length[i] = ex_length[i]
                        exclusive_better_routes[i] = copy.deepcopy(new_route)
                rest_x = copy.deepcopy(exclusive_better_routes)
        
        better_routes = [[] for i in range(self.salesman_number)]
        best_routes = [[] for i in range(self.salesman_number)]
        new_length = [0] * self.salesman_number

        best_routes = copy.deepcopy(rest_x)
        for i in range(len(shared_S)):
            ex_length = [0] * self.salesman_number
            new_length = [0] * self.salesman_number
            min_length = [100000] * self.salesman_number
            k = 0
            while k < self.salesman_number:
                better_routes[k] = copy.deepcopy(best_routes[k])
                for j in range(1, len(better_routes)):
                    new_route = copy.deepcopy(best_routes[k])
                    new_length[k] = 0
                    a = shared_S[i]
                    new_route.insert(j, a)

                    for l in range(1, len(new_route)):
                        new_length[k] += self.distance_matrix[new_route[l-1]][new_route[l]]
                    
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
        two_opted_route = [0] * self.salesman_number


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
                        two_opted_length += self.distance_matrix[two_opted_route[o-1]][two_opted_route[o]]
                    if two_opted_length < min_two_opted_length:
                        min_two_opted_length = two_opted_length
                        better_route = copy.deepcopy(two_opted_route)
            best_routes[i] = copy.deepcopy(better_route)
        return best_routes
    
    def evaluation(self):
        initial_solution = self.greedy_initialization()

        # print(initial_solution)

        initial_solution_lengths = [0.0] * self.salesman_number
        for i in range(len(initial_solution)):
            for j in range(1, len(initial_solution[i])):
                initial_solution_lengths[i] += self.distance_matrix[initial_solution[i][j-1]][initial_solution[i][j]]

        initial_value = sum(initial_solution_lengths)
        # print(initial_value)

        optimal_solution = [[] for i in range(self.salesman_number)]
        optimal_solution = initial_solution
        min_value = initial_value


        cnt = 0
        all_cnt = 0
        while cnt < 10:
            shaked_solution = self.shaking(initial_solution)
            better_solution = self.local_search(shaked_solution)

            solution_lengths = [0.0] * self.salesman_number
            for i in range(len(better_solution)):
                for j in range(1, len(better_solution[i])):
                    solution_lengths[i] += self.distance_matrix[better_solution[i][j-1]][better_solution[i][j]]
            
            value = sum(solution_lengths)

            if value < min_value:
                min_value = value
                optimal_solution = better_solution
                cnt = 0
                # print(min_value)
            
            cnt = cnt + 1
            all_cnt = all_cnt + 1
        
            # print("optimal value is "+str(min_value))
            # print("optimal solution is ")
            # print(optimal_solution)
            # for route in optimal_solution:
            #     for city in route:
            #         print(city, end=', ')
            #     print()
            # print("all_cnt is "+str(all_cnt))

        return optimal_solution
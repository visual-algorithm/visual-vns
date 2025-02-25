origin = "埼玉県秩父市宮側町1-8"
waypoints = [origin, "埼玉県秩父市番場町1-1","埼玉県秩父市熊木熊木町8-15","埼玉県秩父郡小鹿野町長留2518"]

optimal = [
    [0,1,0],
    [0,2,3,0]
]

optimal_address = [[]]
for route in optimal:
    optimal_address.append([""] * (len(route)))

del optimal_address[0]


for i in range(len(optimal)):
    for j in range(len(optimal[i])):
        optimal_address[i][j] = waypoints[optimal[i][j]]

print(optimal_address)
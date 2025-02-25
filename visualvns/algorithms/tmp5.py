origin = "埼玉県秩父市宮側町1-8"

address = [
    ['埼玉県秩父市番場町1-1'],
    ['埼玉県秩父市熊木熊木町8-15', '埼玉県秩父郡小鹿野町長留2518']
]

routes = []
for i in range(len(address)):
    d = {"start": origin, "waypoints": address[i], "end": origin}
    routes.append(d)

print(routes)
optimal_address = [
    ['埼玉県秩父市宮側町1-8', '埼玉県秩父市番場町1-1', '埼玉県秩父市宮側町1-8'],
    ['埼玉県秩父市宮側町1-8', '埼玉県秩父市熊木熊木町8-15', '埼玉県秩父郡小鹿野町長留2518', '埼玉県秩父市宮側町1-8']
]

for route in optimal_address:
    del(route[0])
    del(route[len(route)-1])

print(optimal_address)
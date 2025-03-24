depot_address = "新横浜駅"
city_addresses = ["東京駅", "大阪駅", "名古屋駅", "京都駅", "新横浜駅", "川崎駅", "仙台駅", "博多駅", "金沢駅", "日光駅"]
city_addresses.remove(depot_address)
city_addresses.insert(0, depot_address)
print(city_addresses)
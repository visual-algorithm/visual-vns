import pandas as pd

df = pd.DataFrame([[0, 10, 20], [30, 40, 50]])
print(df)
#     0   1   2
# 0   0  10  20
# 1  30  40  50

print(df.values.tolist())
# [[0, 10, 20], [30, 40, 50]]
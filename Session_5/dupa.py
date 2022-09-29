import numpy as np
row = [[1,2,3], [2,3,4]]
row = np.insert(row, 0, row[0])

row = np.insert(row, -1, row[-1])
print(row)


depth = [1,2,3,4,5]
print(depth[1:-1])

# matrix = [[1,2,3], [1,2,3], [1,2,3]]
# sum = np.sum(matrix)
# print(sum)

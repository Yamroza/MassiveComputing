import numpy as np

print(sum([1,2,3]))



a = [1,2,3,4,5,6]
b = [1,2,3,4,5,6]

a = np.array_split(a, 2)
b = np.array_split(b, 2)
data_tuple = list(zip(a,b))
print(data_tuple)


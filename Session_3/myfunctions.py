# My Functions Library

# Author of addictional functions: Aleksandra Jamróz
# Functions needed for FirstParallel notebook

import time
import numpy as np


def f(x):
    return x * x


def square_vector(idx):
    start_time = time.time()
    result = []
    NUM_ELEMENTS = 156250       # DO NOT FORGET TO CHANGE THIS VALUE WHEN CHANGING THE NUMBER OF PARALLEL PROCESES
    data = np.random.rand(NUM_ELEMENTS)
    for d in data:
        result.append(f(d))
    total_time = time.time()-start_time
    print("Hi, i am the task index {0}, time {1}".format(idx,total_time))
    return total_time


# first dot product function
def dot_product_1(vector1, vector2):
    return sum([vector1[i] * vector2[i] for i in range(len(vector1))])


# second dot product function
def dot_product(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]
    return sum


def dot(a, b):
    r = a * b
    return r


# Functions needed for Benchmark notebook

def work(task):
    """
    This function, which just executes several times a mathematical operation, 
    to consume CPU time, will be used in the benchmark notebook to measure the
    speedup when launch tasks in paralallel
    Some amount of work that will take time
    Parameters:
    task : tuple, contains number, loop, and number processors
    """
    number, loop = task
    b = 2. * number - 1.
    for i in range(loop):
        a, b = b * i, number * i + b
    return a, b


if __name__ == "__main__":
    print("This is not an executable library")


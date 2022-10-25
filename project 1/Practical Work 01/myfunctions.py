# My Functions Library

# Authors of functions:
# Aleksandra Jamróz
# Mireia Alba Kesti Izquierdo


import numpy as np
import multiprocessing as mp
import myfunctions2 as my2


def tonumpyarray(mp_arr):
    """
    Creates a numpy array structure of type unsigned int8, 
    with the memory used by our global r/w shared memory
    mp_array - shared memory array with lock
    """
    return np.frombuffer(mp_arr.get_obj(),dtype=np.uint8)


def image_filter(image: np.array, 
                 filter_mask: np.array,
                 numprocesses: int,
                 filtered_image: mp.Array):
    """
    Executing filtering on image and saving it in shared memory space
    Parameters:
    image - original image
    filter_mask - filter
    numprocesses - number of processes in which the filter must be parallelized
    filtered_image - shared memory variable
    """
    rows = range(image.shape[0])
    with mp.Pool(processes = numprocesses,
                 initializer = my2.pool_init,
                 initargs = [filtered_image, image, filter_mask]) as p:
        p.map(my2.filtering, rows)


# This cell should be the last one to avoid the execution of 
# this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


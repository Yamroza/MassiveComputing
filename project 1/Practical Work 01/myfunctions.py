# My Functions Library

import numpy as np
import multiprocessing as mp
from my_functions2 import filtering

# Authors of functions:
# Aleksandra Jamróz
# Mireia Alba Kesti Izquierdo


def tonumpyarray(mp_arr):
    """
    Creates a numpy array structure of type unsigned int8, 
    with the memory used by our global r/w shared memory
    mp_array - shared memory array with lock
    """
    return np.frombuffer(mp_arr.get_obj(),dtype=np.uint8)


def pool_init(shared_array_, srcimg, filter_mask):
    """
    Initializing the global shared memory data
    shared_array_ - shared read/write data, with lock. It is a vector 
    (because the shared memory should be allocated as a vector)
    srcimg - the original image
    filtermask - filter which will be applied to the image 
    Results will be stored in the shared memory array
    """
    
    global shared_space         # define the local process memory reference for shared memory space
    global shared_matrix        # define the numpy matrix handler
    global image                # define the readonly memory data as global (the scope of this global variables is the local module)
    global my_filter
    
    # initializing the global read only memory data
    image = srcimg
    my_filter = filter_mask
    size = image.shape
    shared_space = shared_array_    # assigning the shared memory to the local reference
    shared_matrix = tonumpyarray(shared_space).reshape(size)    # define the numpy matrix reference to handle data, which will use the shared memory buffer
    
    return 


# FIRST OBLIGATORY FUNCTION FROM INSTRUCTION
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
                 initializer = pool_init,
                 initargs = [filtered_image, image, filter_mask]) as p:
        p.map(filtering, rows)
    return 


# This cell should be the last one to avoid the execution of 
# this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


# My Functions Library

import numpy as np
from multiprocessing.sharedctypes import Value, Array, RawArray
from multiprocessing import Process, Lock
import ctypes


def tonumpyarray(mp_arr):
    """
    Creates a numpy array structure of type unsigned int8, 
    with the memory used by our global r/w shared memory
    mp_array - shared memory array with lock
    """
    return np.frombuffer(mp_arr.get_obj(),dtype=np.uint8)


def dot_init(g_A):
    """
    Creates the instance of Value data type and initialize it to 0
    """
    global A 
    A = g_A # We create a variable of type "double"           
    
    
def shared_dot_1(V):
    # This code is wrong!!!
    # Nothing is locked
    for f in V:
        A.value += f[0]*f[1]
    

def shared_dot_2(V):
    # This code is wrong!!!
    # It returns correct value, but lasts a long time
    with A.get_lock():
        for f in V:
            A.value += f[0]*f[1]


def shared_dot_3(V):
    # It is OKEY!
    # We lock the value just for one unit of time
    a = 0
    for f in V:
        a += f[0]*f[1]
    with A.get_lock():
        A.value += a
    

def pool_init(shared_array_, srcimg, imgfilter):
    """
    Initializing the global shared memory data
    shared_array_ - shared read/write data, with lock. It is a vector 
    (because the shared memory should be allocated as a vector)
    srcimg - the original image
    imgfilter - filter which will be applied to the image 
    Results will be stored in the shared memory array
    """
    
    global shared_space         # define the local process memory reference for shared memory space
    global shared_matrix        # define the numpy matrix handler
    global image                # define the readonly memory data as global (the scope of this global variables is the local module)
    global my_filter
    
    # initializing the global read only memory data
    image = srcimg
    my_filter = imgfilter
    size = image.shape
    
    shared_space = shared_array_    # assigning the shared memory to the local reference
    shared_matrix = tonumpyarray(shared_space).reshape(size)    # define the numpy matrix reference to handle data, which will use the shared memory buffer


def parallel_shared_imagecopy(row):
    """
    Copies the original image to the global r/w shared  memory 
    """
    global image
    global my_filter
    global shared_space    
    # with this instruction we lock the shared memory space, avoiding other parallel processes trying to write on it
    with shared_space.get_lock():
        # while we are in this code block no one, except this execution thread, can write in the shared memory
        shared_matrix[row,:,:] = image[row,:,:]
    return


def edge_filter(row):
    global image
    global my_filter
    global shared_space

    with shared_space.get_lock():
        (rows,cols,depth) = image.shape

        #fetch the r row from the original image
        srow = image[row,:,:]

        if (row > 0):
            prow = image[row-1,:,:]
        else:
            prow = image[row,:,:]
    
        if (row == (rows-1)):
            nrow = image[row,:,:]
        else:
            nrow = image[row+1,:,:]

        # copy first and last element of each row to create borders
        prow = np.ndarray.tolist(prow)
        prow.insert(0, prow[0])
        prow.append(prow[-1])
        prow = np.array(prow)

        srow = np.ndarray.tolist(srow)
        srow.insert(0, srow[0])
        srow.append(srow[-1])
        srow = np.array(srow)

        nrow = np.ndarray.tolist(nrow)
        nrow.insert(0, nrow[0])
        nrow.append(nrow[-1])
        nrow = np.array(nrow)
    
        #defines the result vector, and set the initial value to 0
        frow = np.zeros((cols,depth))
        frow = srow

        # calculation of filtered pixel's value
        for i in range(1, len(srow)-1):         # iterating through pixels in the row
            for j in range(depth):              # iterating on r, g, b color components
                filtered_mat = [[prow[i-1][j] * my_filter[0][0], prow[i][j] * my_filter[0][1], prow[i+1][j] * my_filter[0][2]], 
                                [srow[i-1][j] * my_filter[1][0], srow[i][j] * my_filter[1][1], srow[i+1][j] * my_filter[1][2]],
                                [nrow[i-1][j] * my_filter[2][0], nrow[i][j] * my_filter[2][1], nrow[i+1][j] * my_filter[2][2]]]
                frow[i][j] = np.sum(filtered_mat)

        #while we are in this code block no ones, except this execution thread, can write in the shared memory
        shared_matrix[row,:,:] = frow[1:-1]
    return    


#This cell should be the last one
#this avoid the execution of this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


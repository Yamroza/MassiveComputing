# My Functions Library

import numpy as np
import multiprocessing as mp


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


# function copy-pasted from previous session 6
# we have 2 images so we can't actually write both to the same global variables
# idk, 2 functions? or some if statement in "initializer = ..." parameter?
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
# We have 2 pictures and 2 filters, so we can't make them both global using <<pool_init>>
# because it would overwrite them in the same memory place later, so using this one will be wrong
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


# SECOND OBLIGATORY FUNCTION FROM INSTRUCTION
def filters_execution(image: np.array,  
                      filter_mask1: np.array, 
                      filter_mask2: np.array,  
                      numprocessors: int,
                      filtered_image1: mp.Array,
                      filtered_image2: mp.Array ):
    """
    Function invoking 2 different parallel processes, each executing a filter
    on the same image and saving the result to independent memory spaces. Uses
    previous function for filtering.
    """

    # creating two processes
    p1 = mp.Process(target = image_filter, args = (image, filter_mask1, numprocessors, filtered_image1))
    p2 = mp.Process(target = image_filter, args = (image, filter_mask2, numprocessors, filtered_image2))
    
    # starting processes 
    p1.start() 
    p2.start() 
  
    # wait until processes are finished 
    p1.join() 
    p2.join()

    return


def filtering(r):
    
    global image
    global my_filter

    (rows, cols, depth) = image.shape
    (filter_rows, filter_cols) = my_filter.shape

    # fetch the row from the original image
    srow = image[r,:,:]

    # defines the result vector, and set the initial value to 0
    frow = np.zeros((cols,depth))
    frow = srow

    # calculating how many rows & cols we have to take
    additional_rows_number = int((filter_rows - 1) / 2)
    additional_cols_number = int((filter_cols - 1) / 2)    
    
    # creating matrix of needed rows
    rows_mat = []

    for row_number in range(-additional_rows_number, additional_rows_number + 1):
        index = r + row_number
        if index < 0:
            index = 0
        if index > len(image)-1:
            index = len(image)-1
        rows_mat.append(image[index,:,:])

    # filling output row
    for i in range(len(srow)):      # iterating on pixels in row
        for j in range(depth):      # iterating on color components (1 for grayscale, 3 for color)
            sum = 0                 # final pixel value
            for row in range(filter_rows):
                for col in range(filter_cols):
                    col_position = i + col - additional_cols_number
                    if col_position < 0:
                        sum += my_filter[row][col] * rows_mat[row][0][j]
                    elif col_position > len(srow) - 1:
                        sum += my_filter[row][col] * rows_mat[row][-1][j]
                    else:
                        sum += my_filter[row][col] * rows_mat[row][col_position][j]

            frow[i][j] = int(sum)

    with shared_space.get_lock():
        shared_matrix[r,:,:] = frow

    return    


# This cell should be the last one to avoid the execution of 
# this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


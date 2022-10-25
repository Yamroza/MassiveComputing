import numpy as np


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
    global image                # define the read-only memory data as global (the scope of this global variables is the local module)
    global my_filter            # define the filter mask
    global shared_matrix        # define the numpy matrix handler
    
    # initializing the global read only memory data
    image = srcimg
    my_filter = filter_mask
    size = image.shape

    shared_space = shared_array_    # assigning the shared memory to the local reference
    shared_matrix = tonumpyarray(shared_space).reshape(size)    # define the numpy matrix reference to handle data, which will use the shared memory buffer


def filtering(r):
    """
    Filtering function. Uses global variables in order to filter specific row of the image.
    Overwrites shared matrix containing the results of calculae. Uses lock to avoid races.
    r - row number

    """
    
    global image
    global my_filter
    global shared_space
    global shared_matrix

    (rows, cols, depth) = image.shape
    (filter_rows, filter_cols) = my_filter.shape

    # fetch the row from the original image
    srow = image[r,:,:]

    # defines the result vector, and set the initial value to 0
    frow = np.zeros((cols,depth))

    # calculating how many rows & cols we have to take
    additional_rows_number = int((filter_rows - 1) / 2)
    additional_cols_number = int((filter_cols - 1) / 2)    
    
    for i in range(len(srow)):      # iterating on pixels in row
        for j in range(depth):      # iterating on color components (1 for grayscale, 3 for color)
            sum = 0                 # final pixel value
            for row in range(filter_rows):
                for col in range(filter_cols):

                    row_position = r + row - additional_rows_number
                    if row_position < 0:
                        row_position = 0
                    if row_position > len(image)-1:
                        row_position = len(image)-1

                    col_position = i + col - additional_cols_number
                    if col_position < 0:
                        sum += my_filter[row][col] * image[row_position,:,:][0][j]
                    elif col_position > len(srow) - 1:
                        sum += my_filter[row][col] * image[row_position,:,:][-1][j]
                    else:
                        sum += my_filter[row][col] * image[row_position,:,:][col_position][j]

            frow[i][j] = sum

    with shared_space.get_lock():
        shared_matrix[r,:,:] = frow

    return


# This cell should be the last one to avoid the execution of 
# this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


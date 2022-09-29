# My Functions Library

import numpy as np


def init_second(my_matrix2):
    global matrix_2
    matrix_2 = my_matrix2
    print(matrix_2.shape)


def init_globalimage(img, filt):
    global image
    global my_filter
    image = img
    my_filter = filt


def parallel_matmul(v):
    """
    v: input row
    matrix_2: second matrix, shared by memory
    """

    # here we calculate the shape of the second matrix, to generate the resultant row
    matrix_2 # we will use the global matrix
    
    (rows,columns) = matrix_2.shape
    
    # we allocate the final vector of size the number of columns of matrix_2
    d = np.zeros(columns)
    
    # we calculate the dot product between vector v and each column of matrix_2
    for i in range(columns):
        d[i] = np.dot(v, matrix_2[:,i])
    
    return d


def parallel_filtering_image(r):
    """"
    r: row number to filter
    image: global memory array
    my_filter: filter shape to apply to the image
    """
    
    global image
    global my_filter
    
    # from the global variable, gets the image shape
    (rows, cols, depth) = image.shape

    # fetch the row from the original image
    srow = image[r,:,:]
    if (r > 0):
        prow = image[r-1,:,:]
    else:
        prow = image[r,:,:]
    
    if (r == (rows-1)):
        nrow = image[r,:,:]
    else:
        nrow = image[r+1,:,:]

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

    # defines the result vector, and set the initial value to 0
    frow = np.zeros((cols,depth))
    frow = srow

    # calculation of filtered pixel's value
    for i in range(1, len(srow)-1):         # iterating through pixels in the row
        for j in range(depth):              # iterating on r, g, b color components
            frow[i][j] = np.sum([[prow[i-1][j] * my_filter[0][0], prow[i][j] * my_filter[0][1], prow[i+1][j] * my_filter[0][2]], 
                                 [srow[i-1][j] * my_filter[1][0], srow[i][j] * my_filter[1][1], srow[i+1][j] * my_filter[1][2]],
                                 [nrow[i-1][j] * my_filter[2][0], nrow[i][j] * my_filter[2][1], nrow[i+1][j] * my_filter[2][2]]])
    
    return frow[1:-1]                   # returns row without additional unnecessary borders




def second_parallel_filtering_image(r):
    """"
    r: row number to filter
    image: global memory array
    my_filter: filter shape to apply to the image
    """
    
    global image
    global my_filter
    
    # from the global variable, gets the image shape
    (rows, cols, depth) = image.shape

    # fetch the row from the original image
    srow = image[r,:,:]
    if (r > 0):
        prow = image[r-1,:,:]
    else:
        prow = image[r,:,:]
    
    if (r == (rows-1)):
        nrow = image[r,:,:]
    else:
        nrow = image[r+1,:,:]

    # defines the result vector, and set the initial value to 0
    frow = np.zeros((cols,depth))
    frow = srow

    for i in range(len(srow)):
        for j in range(depth):
            x = i - 1
            y = i + 1
            if x < 0:
                x += 1
            if y > len(srow)-1:
                y -= 1

            frow[i][j] = np.sum([[prow[x][j] * my_filter[0][0], prow[i][j] * my_filter[0][1], prow[y][j] * my_filter[0][2]], 
                                 [srow[x][j] * my_filter[1][0], srow[i][j] * my_filter[1][1], srow[y][j] * my_filter[1][2]],
                                 [nrow[x][j] * my_filter[2][0], nrow[i][j] * my_filter[2][1], nrow[y][j] * my_filter[2][2]]])

    return frow                 # returns row without additional unnecessary borders

    
#This cell should be the last one
#this avoid the execution of this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


# My Functions Library

import numpy as np

# Authors of homework:
# Aleksandra Jamróz
# Mireia Alba Kesti Izquierdo

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

    # defines the result vector, and set the initial value to 0
    frow = np.zeros((cols,depth))
    frow = srow

    for i in range(len(srow)):      # iterating on pixels in the row
        for j in range(depth):      # iterating on color components (1 for grayscale images, 3 for rgb)
 
            x = i - 1               # x - previous column value
            y = i + 1               # y - next column value
            if x < 0:
                x += 1              # x value incremented if it exceeds the border of image
            if y > len(srow)-1:
                y -= 1              # y value decremented if it exceeds the border of image

            frow[i][j] = (prow[x][j] * my_filter[0][0] + prow[i][j] * my_filter[0][1] + prow[y][j] * my_filter[0][2] +
                          srow[x][j] * my_filter[1][0] + srow[i][j] * my_filter[1][1] + srow[y][j] * my_filter[1][2] +
                          nrow[x][j] * my_filter[2][0] + nrow[i][j] * my_filter[2][1] + nrow[y][j] * my_filter[2][2])

    return frow


#This cell should be the last one
#this avoid the execution of this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


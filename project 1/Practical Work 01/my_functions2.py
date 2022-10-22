import numpy as np


def filtering(r):
    
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
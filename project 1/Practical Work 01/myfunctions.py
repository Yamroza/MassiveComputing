# My Functions Library

import numpy as np
import multiprocessing as mp

# Authors of functions:
# Aleksandra Jamróz
# Mireia Alba Kesti Izquierdo


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
    return 


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
    return



# This cell should be the last one to avoid the execution of 
# this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


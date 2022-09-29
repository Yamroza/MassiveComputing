#!/usr/bin/env python
# coding: utf-8

# # MyFunctions2 module

# In[ ]:


import multiprocessing as mp
import numpy as np
from multiprocessing import Semaphore, Lock, Process, Pool
import ctypes


# In[ ]:


def withdraw(balance):     
    for _ in range(10000): 
        balance.value = balance.value - 1
  


# In[ ]:


def deposit(balance):     
    for _ in range(10000): 
        balance.value = balance.value + 1


# In[ ]:


def withdraw2(balance, lock):     
    for _ in range(10000): 
        lock.acquire() 
        balance.value = balance.value - 1
        lock.release() 


# In[ ]:


def deposit2(balance, lock):     
    for _ in range(10000): 
        lock.acquire() 
        balance.value = balance.value + 1
        lock.release() 


# In[ ]:


#This cell should be the last one
#this avoid the execution of this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")


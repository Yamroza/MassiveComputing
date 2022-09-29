# Freerunning module

import multiprocessing as mp
import numpy as np
from multiprocessing import Semaphore, Lock, Process, Pool
import ctypes


def withdraw(balance):
    for _ in range(10000):
        balance.value = balance.value - 1


def deposit(balance):
    for _ in range(10000):
        balance.value = balance.value + 1


def withdraw2(balance, lock):
    for _ in range(10000):
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()


def deposit2(balance, lock):
    for _ in range(10000):
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()


#This cell should be the last one
#this avoid the execution of this script when is invoked directly.
if __name__ == "__main__":
    print("This is not an executable library")
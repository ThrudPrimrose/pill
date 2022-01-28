import numpy as np


def first_n_0(arr):
    a = 0
    for i in arr:
        if i == 0:
            a += 1
        else:
            return a

    return a


def cull_zeros(arr, x):
    n = first_n_0(arr)
    l = arr[n:]
    xs = x[n:]
    npl = np.array(l)
    npxs = np.array(xs)
    return (npl, npxs)

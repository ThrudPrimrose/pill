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


def arr_to_string(arr):
    s = str()
    # s += "["
    if len(arr) > 1:
        for i in range(len(arr)-1):
            s += arr[i]
            s += "; "
        s += arr[len(arr)-1]
        # s += "]"
    elif len(arr) == 1:
        s += arr[0]
        # s += "]"
    # else:
        # s += "[]"
    return s


def string_to_arr(str):
    # "[ ..., a..., "
    # read until first ,
    # skip one offeset, repeat
    if not ";" in str:
        print(str)
    else:
        x = str.split("; ")
        print(x)

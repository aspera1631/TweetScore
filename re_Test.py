__author__ = 'bdeutsch'

import numpy as np
import pandas as pd

def cartesian(arrays, out=None):
    """
    From pv on stackoverflow
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    cartesian(([1, 2, 3], [4, 5], [6, 7])) ->
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

emo_vals = range(0,7)
ht_vals = range(0,7)
media_vals = range(0,3)
txt_bas_vals = range(0,29)
url_vals = range(0,3)
user_vals = range(0,7)

test = cartesian((emo_vals, ht_vals, media_vals, txt_bas_vals, url_vals, user_vals))

tweetspace = pd.DataFrame(test, columns=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"])

print tweetspace
import pandas as pd


tweets = pd.read_pickle('goodness_ind_3')

print tweets["goodness"].idxmax(axis=1)



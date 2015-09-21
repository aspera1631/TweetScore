

import pandas as pd



ts = pd.read_pickle('goodness_ind_4')


ideal = ts["goodness"].idxmax(axis=1)
rts = ts["goodness"].max()
print ideal, rts

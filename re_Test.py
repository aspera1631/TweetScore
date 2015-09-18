__author__ = 'bdeutsch'

import numpy as np
import pandas as pd



ts = pd.read_pickle('recommendations')

print ts.tail(10)
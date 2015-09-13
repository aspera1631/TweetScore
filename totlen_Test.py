__author__ = 'bdeutsch'

import numpy as np
import pandas as pd


def get_ent_len(entities):
    totlen = 0
    if len(entities) > 0:
        for item in entities:
            indices = item.get("indices", [0,0])
            len1 = indices[1] - indices[0]
            totlen = totlen + len1
    return totlen


def replace_amper(text):
    newtext = text.replace('&amp;','&')
    return newtext

#test = [{}, {"text":"bar","indices":[53,63]}]
#test = "Muslims must protect religious minorities in Syria &amp; Iraq; shame on us if we don't, we wouldn't be true to the teachings of our Prophet PBUH"
#print replace_amper(test)

#test = "I'm ready for\n\ud83c\udf41\ud83c\udf41\ud83c\udf41   \ud83c\udfc8     \ud83c\udf83          \ud83d\udc7b\n\ud83c\udf41          \ud83c\udfc8\ud83c\udfc8   \ud83c\udf83         \ud83d\udc7b\n\ud83c\udf41\ud83c\udf41    \ud83c\udfc8  \ud83c\udfc8   \ud83c\udf83         \ud83d\udc7b\n\ud83c\udf41       \ud83c\udfc8\ud83c\udfc8\ud83c\udfc8  \ud83c\udf83         \ud83d\udc7b\n\ud83c\udf41      \ud83c\udfc8       \ud83c\udfc8 \ud83c\udf83\ud83c\udf83\ud83c\udf83\ud83d\udc7b\ud83d\udc7b\ud83d\udc7b"

print test.decode("utf-8", "strict")
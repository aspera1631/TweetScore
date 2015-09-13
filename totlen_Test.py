__author__ = 'bdeutsch'


def get_ent_len(entities):
    totlen = 0
    if len(entities) > 0:
        for item in entities:
            indices = item.get("indices", [0,0])
            len1 = indices[1] - indices[0]
            totlen = totlen + len1
    return totlen


#test = [{}, {"text":"bar","indices":[53,63]}]
test = {}
print get_ent_len(test)
__author__ = 'bdeutsch'

import numpy as np
import pandas as pd
import MySQLdb

## Given the gradient, output a file with the top n recommendations

# Import gradient, replace NaN with a very negative gradient (will always avoid those transitions)
gradient = pd.read_pickle('gradient_prob').fillna(-100000000)

# Create a new dataframe with same indices as gradient, but 3 columns corresponding to each index
recommendations = pd.DataFrame(columns=["msg1", "msg2", "msg3"], index=gradient.index)

# Create a new dataframe that has the gradient cols as indices. One column corresponds to the text message.
indices = ["emo+", "ht+", "med+", "txt+", "url+", "usr+", "emo-", "ht-", "med-", "txt-", "url-", "usr-"]
msg_tbl = pd.DataFrame(columns=["messages"], index=indices)
msg_tbl["messages"] = ["Add an emoji", "Add a hashtag", "Add an image", "Add a bit more text", "Add a link", "Add a user mention", "Remove an emoji", "Remove a hashtag", "Remove an image", "Remove a bit of text", "Remove a link", "Remove a user mention"]



# Sort each row of the gradient by column (axis 1). Return the first n column names that are not nan.

# Generate list of indices
ind1 = gradient.index.values
# For each index
for i in ind1:
    # reorder columns in this row
    new_columns = gradient.columns[gradient.ix[i].argsort()]
    # ordered row. If we have NaN here it messes up the ordering.
    ord_row = gradient.loc[i][reversed(new_columns)]

    # Filter for only positive recommendations. Kills old NaN values
    pos_steps = ord_row[ord_row.values > 0]

    # Build a message list
    msg_list = []
    # For each message
    for j in [0,1,2]:
        # Try to find the message corresponding to the first three values.
        try:
            msg_ind = pos_steps.index.values[j]
            msg = msg_tbl.loc[msg_ind].values[0]
        except:
            # if there aren't three positive values, report empty strings.
            msg = ''
        msg_list.append(msg)
    # Build the recommendation dataframe.
    recommendations.loc[i][["msg1", "msg2", "msg3"]] = msg_list

# Write to pickle file
recommendations.to_pickle("recommendations_prob")

# Write to SQL
con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect
tableName = 'recommendations_prob'
recommendations.to_sql(con=con, name=tableName, if_exists="replace", flavor='mysql')




'''
rownum = 900
new_columns = gradient.columns[gradient.ix[ind1[rownum]].argsort()]
#new_columns = gradient.columns[gradient.ix[ind1[1]]]
#print gradient.loc[ind1[rownum]]
#print gradient.loc[ind1[rownum]][reversed(new_columns)]
#print new_columns


ord_row = gradient.loc[ind1[rownum]][reversed(new_columns)]

# take only the suggestions that lead to an improvement
pos_steps = ord_row[ord_row.values > 0]
# Build the rec. dataframe


#print msg_tbl

msg_list = []
for i in [0,1,2]:
    try:
        msg_ind = pos_steps.index.values[i]
        msg = msg_tbl.loc[msg_ind].values[0]
    except:
        msg = ''
    msg_list.append(msg)


recommendations.loc[ind1[rownum]][["msg1", "msg2", "msg3"]] = msg_list

print recommendations.loc[ind1[rownum]]

'''
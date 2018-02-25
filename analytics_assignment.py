
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

def return_similar_row_nums(array, index_list):
    '''
    Input: Each group(first name, last name) formed by a unique dob, gender combination as key.
    Output: A list of lists where  each inner list contains indices of rows of similar names.
    '''
    sim_index_list = []
    visited = [0]*len(array)
    for i in range(len(array)):
        temp = []
        flag = False
        x = array[i]
        if(visited[i]==0):
            flag = True
            visited[i] = 1
            first_name_x = x[0].split(' ')
            last_name_x = x[1].split(' ')
            temp.append(index_list[i])
            for j in range(len(array)):
                y = array[j]
                if(visited[j] == 0):
                    first_name_y = y[0].split(' ')
                    last_name_y = y[1].split(' ')
                    if(fuzz.ratio(first_name_x[0],first_name_y[0])>70 and (fuzz.ratio(last_name_x[0],last_name_y[0])>70) and (fuzz.ratio(x[0]+' '+x[1], y[0]+' '+y[1])>80)):
                        temp.append(index_list[j])
                        visited[j] = 1
        if(flag):
            sim_index_list.append(temp)
    return sim_index_list

df = pd.read_csv('Deduplication Problem - Sample Dataset.csv')
df1 = df.groupby(['dob', 'gn'])
'''
Grouping by Date of birth and Gender column, because even if two persons have 
same name but have different dob or have different gender must be classified 
as two different persons.
'''
dic = df1.groups
'''
'dic' contains all possible unique keys (dob, gender) with values having row indices
of the actual dataframe.

Eg:-
{('01/03/68', 'F'): Int64Index([0, 1, 2, 3, 4], dtype='int64'),
 ('01/05/51', 'M'): Int64Index([27], dtype='int64'),
 ......}
'''
sim = {}
for k in dic.keys():
    ind = return_similar_row_nums(list(df.loc[dic[k]][['ln', 'fn']].values), list(dic[k]))
    sim[k] = ind
    
'''
Printing similar set of names of same person followed by a newline
'''
for key in sim:
    for i in sim[key]:
        print (df.loc[i])
        print ('\n')


# In[ ]:




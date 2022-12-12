#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd
import os, glob
from tqdm import tqdm
import warnings


# In[61]:


warnings.filterwarnings("ignore")

all_files = glob.glob("*.txt")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)


# In[23]:


outputFileName= input(' * Enter your output file name ( file type is csv) : ')


def timeframe(item):
    if item == 1:
        return '1Min'
    elif item == 2:
        return '5Min'
    elif item == 3:
        return '15Min'
    elif item == 4:
        return '30Min'
    elif item == 5:
        return '1H'
    elif item == 6:
        return '4H'
    elif item == 7:
        return '1D'
    else:
        return 'The time frame in not valid !'
    
timeFrameInput = int(input(""" * Enter your time frame :

    1 : M1
    2 : M5
    3 : M15
    4 : M30
    5 : H1
    6 : H4
    7 : D1   
    
    """))

timeFrame = timeframe(timeFrameInput)


# In[20]:


arr=[]

for i in tqdm(range(0,len(frame)),total=len(frame),desc=' * Splitting data '):
    arr.append(frame.iloc[i][0].split())


# In[57]:


table  = pd.DataFrame(arr)
table = table .rename({0: 'date', 1: 'time', 2: 'bid', 3:'ask'}, axis=1)


# In[62]:


table["DateTime"] = table["date"].astype(str) +" "+ table["time"]
data = table[['DateTime','bid']]
data['DateTime'] = pd.to_datetime(data['DateTime'])
data = data.set_index(['DateTime'])


# In[63]:


data["bid"] = pd.to_numeric(data["bid"], downcast="float")
#data["ask"] = pd.to_numeric(data["ask"], downcast="float")


# In[64]:


data_ohlc = data['bid'].resample(timeFrame).ohlc()


# In[65]:


data_ohlc['dateTime']=data_ohlc.index
splitedTime=[]


# In[66]:


data_ohlc['date'] = pd.to_datetime(data_ohlc['dateTime']).dt.date
data_ohlc['time'] = pd.to_datetime(data_ohlc['dateTime']).dt.time


# In[67]:


output = data_ohlc.reset_index()
output = output[['date','time','open','high','low','close']]
output=output[output['open'].notna()]


# In[49]:


output.to_csv(outputFileName+'.csv',index=False)


# In[50]:


print('Finished ... !')


# In[ ]:





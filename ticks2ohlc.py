import pandas as pd


fileName= input(' * Enter your input file name ( file type is txt) : ')
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
    
timeFrameInput = int(input(""" * Select the time frame :

    1 : M1
    2 : M5
    3 : M15
    4 : M30
    5 : H1
    6 : H4
    7 : D1         

    """))

timeFrame = timeframe(timeFrameInput)


df = pd.read_fwf(fileName+'.txt')
df = df.rename({'RateDateTime\tRateBid\tRateAsk': 'A', 'Unnamed: 1': 'B'}, axis=1) 
arr= []
bid= []




for i in range(len(df)):
    arr.append((df['A'][i].replace('\t', ' ').split(' ')))
    
for i in range(len(df)):
    bid.append(df['B'][i]) 
    

table = pd.DataFrame(arr)
table['bid']=bid

table = table.rename({0: 'date', 1: 'time', 2: 'bid'}, axis=1)

table["DateTime"] = table['date'].astype(str) +" "+ table["time"]
data = table[['DateTime','bid']]

data['DateTime'] = pd.to_datetime(data['DateTime'])

data = data.set_index(['DateTime'])


data["bid"] = pd.to_numeric(data["bid"], downcast="float")
#data["ask"] = pd.to_numeric(data["ask"], downcast="float")

data_ohlc = data['bid'].resample(timeFrame).ohlc()


data_ohlc['dateTime']=data_ohlc.index
splitedTime=[]


data_ohlc['date'] = pd.to_datetime(data_ohlc['dateTime']).dt.date
data_ohlc['time'] = pd.to_datetime(data_ohlc['dateTime']).dt.time

output = data_ohlc.reset_index()
output = output[['date','time','open','high','low','close']]

output.to_csv(outputFileName+'.csv')


print('Finished ... !')
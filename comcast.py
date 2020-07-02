import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
com = pd.read_csv("Comcast_telecom_complaints_data.csv")
com['DT'] = com['Date'] + " " + com['Time']

com.isnull().sum()

#Trend Chart Monthly and Daily
com.dtypes

time = com.loc[:,'Time']
# Function to convert the date format 
def convert24(str1): 
    if(len(str1.split(":")[0])==1 ): str1 = "0"+str1 
# is AM and first two elements are 12  
    if str1[-2:] == "AM" and str1[:2] == "12": 
     return "00" + str1[2:-2] 
# remove the AM elif str1[-2:] == "AM": 
     return str1[:-2]
# Checking if last two elements of time 
# is PM and first two elements are 12 
    elif str1[-2:] == "PM" and str1[:2] == "12": 
     return str1[:-2] 
    else: 
# add 12 to hours and remove PM 

     return str(int(str1[:2]) + 12) + str1[2:8] 

for label, row in com.iterrows(): 

 com.loc[label,'Time'] = convert24(row['Time']) 

dt = com["Date"] + " " + com['Time']

 # Daily plot
td1 = com['Date'].value_counts()
td1.plot(grid=True)  

#Monthly Plot
com['Month'] = com['Date_month_year'].str[3:6]
mon = com['Month'].value_counts()
mon.plot(grid=True)

#Categorising Type of Problems   
cat = com.loc[:,('Customer Complaint','Status')]
def findcat(int):
    if 'internet' in int.casefold() and "data" not in int.casefold():
        return 'Internet'
    if 'bill' in int.casefold() or 'fee' in int.casefold() or 'charg' in int.casefold() or 'pric' in int.casefold() or 'pay' in int.casefold() or 'rate' in int.casefold():
        return 'Money'
    if int=='comcast':
        return 'No Description'
    if 'speed' in int.casefold() or 'slow' in int.casefold():
        return 'Speed'
    if 'service' in int.casefold() or 'fraud' in int.casefold():
        return 'service'
    if 'data' in int.casefold() or 'network' in int.casefold() or 'outage' in int.casefold() or 'switch' in int.casefold():
        return 'Network'
    elif 'comcast' in int.casefold():
        return 'Company'
    else:
        return 'Misc'
      
for i, j in cat.iterrows():
    cat.loc[i,'Customer Complaint'] = findcat(j['Customer Complaint'])
        
category = cat['Customer Complaint'].value_counts()
category.plot(grid=True)

#categorical variable with value as Open and Closed.
def newcat(int1):
    if int1=='Closed' or int1=='Solved':
        return 'Close'
    else:
        return 'Open'
    
for a, b in cat.iterrows():
    cat.loc[a,'Status'] = newcat(b['Status'])
    
cat['State'] = com.loc[:,'State']

#state has the maximum complaints
maxcomp = cat['State'].value_counts()

#Complaints resolved and unresolved State-wise
def stat(int2):
    if 'Open' in int2:
        return 1
    else:
        return 0
    
for a, b in cat.iterrows():
    cat.loc[a,'Status'] = stat(b['Status'])

cat.query('Status==1')['State']
maxunres = cat.query('Status==1')['State'].value_counts()
maxres = cat.query('Status==0')['State'].value_counts()

#stacked bar chart
from matplotlib import rc
bar1 = maxunres.to_frame()
bar1 = bar1.reset_index()
bar1['Open'] = bar1['State']
bar1['State'] = bar1['index']
bar1 = bar1.drop(['index'], axis = 1)


bar2 = maxres.to_frame()
bar2 = bar2.reset_index()
bar2['Close'] = bar2['State']
bar2['State'] = bar2['index']
bar2 = bar2.drop(['index'], axis = 1)


bar = pd.merge(bar2, bar1, on="State", how = 'left')
bar = bar.replace(np.NAN, 0, inplace=False)
bar1plt = bar.iloc[:,1].values
bar2plt = bar.iloc[:,2].values
states = cat['State'].value_counts()
states = states.reset_index()
states['State'] = states['index']
states = states.drop(['index'], axis = 1)
states = states.iloc[:,0].values

bars = np.add(bar1plt, bar2plt).tolist()
r = list(range(43))
p1open = plt.bar(r,bar1plt,width=.8)
p1close = plt.bar(r, bar2plt, bottom=bar1plt,  color='#2d7f5e', edgecolor='white', width=.8)
            
plt.xticks(r, states, rotation=45, fontsize=5)
plt.xlabel("States")
plt.ylabel('Scores')
plt.title('Open and Close Complaints State-Wise')
plt.legend((p1open[0], p1close[0]), ('Open', 'Close'))

#percentage of complaints resolved till date, 
#which were received through the Internet and customer care calls.

cat['Received Via'] = com.loc[:,'Received Via']
rec0 = cat.query('Status==0')['Received Via'].value_counts()
rec0['Total'] = rec0.sum()
rec1 = cat.query('Status==1')['Received Via'].value_counts()
rec1['Total'] = rec1.sum()

percentage = rec0['Total']/(rec0['Total'] + rec1['Total'])*100
print(percentage)




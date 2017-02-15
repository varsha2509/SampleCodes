# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:14:33 2017

@author: varshagopalakrishnan
"""

### Sample Code in Python for Data Cleaning and Analysis.
###### The following codes are snippets from class problems and from research work

import pandas as pd
import re
import numpy as nppd.set_option('display.max_rows', 530)


os.chdir("/home/varshagopalakrishnan/Documents/Python/Data science in Python")





## The following code is used to clean a text file to remove characters after ','

df_list = []
with open("university_towns.txt") as f:
    for line in f:
        # remove whitespace at the start and the newline at the end
        line = line.strip()
        # split each column on whitespace
        columns = re.split('\n', line)
        df_list.append(columns)
df = pd.DataFrame(df_list)
#df = pd.to_csv(files,sep="\n",header=None)
df.columns=['Region name']
sep='('
for index,item in enumerate(df['Region name']):
    df['Region name'][index]=item.split(sep)[0]
df['Region name'] = df['Region name'].str.replace(r"[\(\[].*?[\)\]]","")
columns = ['State','RegionName']
df2 = pd.DataFrame(data=np.empty((len(df),2)),columns=columns,dtype=str)
x=['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii',
    'Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
    'Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York',
    'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee',
    'Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']


for index, item in enumerate(df['Region name']):
    if (item in x):
        df2.iloc[index]['State'] = item
        df2.iloc[index]['RegionName'] = item
    else:
        df2.iloc[index]['RegionName']= item
        df2.iloc[index]['State'] = df2.iloc[index-1]['State']
df2 = df2[df2['RegionName'] != df2['State']]
df2['RegionName'] = df2['RegionName'].str.rstrip()
df2['RegionName'] = df2['RegionName'].str.rstrip('  ,')
df2['RegionName'] = df2['RegionName'].str.rstrip(' . ')
df2['RegionName'] = df2['RegionName'].str.rstrip(' \)')
df2 = df2[df2['RegionName']!= '']
df2.reset_index(inplace=True)
del df2['index']
print df2


## Following function calculates a recession start data based on GDP in year 2009
def get_recession_start():
    gdp = pd.read_excel('gdplev.xls', sheetname=0, header=6, skiprows=213, parse_cols='E:G',names = ['Year', 'GDP in billion', 'GDP in 2009 billion'])        
    gdp.reset_index()
    #gdp.set_index('Year',inplace=True)
    index = 0
    gdp['diff'] = gdp['GDP in 2009 billion'].diff()
    gdp_b = []
    for index,item in enumerate(gdp['diff']):
        if (item > 0):
            gdp_b.append('1')
        if (item < 0):
            gdp_b.append('0')


    new_index=0
    for index,item in enumerate(gdp_b):
        if (gdp_b[index] is '0' and gdp_b[index+1] is '0'):
            if(gdp_b[index+2] is '1' and gdp_b[index+3] is '1'):
                new_index = index;
            if(gdp_b[index+2] is '0' and gdp_b[index+3] is '1'):   
                continue
    gdp.reset_index()
    return(str(gdp.iloc[new_index-1]['Year']))
    
get_recession_start()


## Following function calculates the quarter of recession bottom based on GDP data for year 2009
def get_recession_bottom():
    gdp = pd.read_excel('gdplev.xls', sheetname=0, header=6, skiprows=213, parse_cols='E:G',names = ['Year', 'GDP in billion', 'GDP in 2009 billion'])        
    gdp.reset_index()
    #gdp.set_index('Year',inplace=True)
    index = 0
    gdp['diff'] = gdp['GDP in 2009 billion'].diff()
    gdp_b = []
    for index,item in enumerate(gdp['diff']):
        if (item > 0):
            gdp_b.append('1')
        if (item < 0):
            gdp_b.append('0')


    new_index=0
    for index,item in enumerate(gdp_b):
        if (gdp_b[index] is '0' and gdp_b[index+1] is '0'):
            if(gdp_b[index+2] is '1' and gdp_b[index+3] is '1'):
                new_index = index;
            if(gdp_b[index+2] is '0' and gdp_b[index+3] is '1'):   
                continue
    gdp.reset_index()
    
    return(str(gdp.iloc[new_index+2]['Year']))

get_recession_bottom()




### Following code snippet performs a hypothesis test on housing prices in university towns and non-university
#towns during recession. The hypothesis tests whether decline in prices is higher in university towns or non-university towns
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
housing = pd.read_csv('City_Zhvi_AllHomes.csv', header  =0,index_col=[1,2],na_values=np.nan)
housing = housing.iloc[0:len(housing),49:254]
new_dataframe = pd.DataFrame(data=np.zeros((len(housing),6)),columns=(['RegionName','State','2008q3','2008q4','2009q1','2009q2']))
housing.reset_index(inplace=True)
new_dataframe['State'] = housing['State']
new_dataframe['RegionName'] = housing['RegionName']
new_dataframe['State'] = new_dataframe['State'].replace(states)  
new_dataframe['2008q3'] = (housing['2008-07'] + housing['2008-08'] + housing['2008-09'])/3
new_dataframe['2008q4'] = (housing['2008-10'] + housing['2008-11'] + housing['2008-12'])/3
new_dataframe['2009q1'] = (housing['2009-01'] + housing['2009-02'] + housing['2009-03'])/3
new_dataframe['2009q2'] = (housing['2009-04'] + housing['2009-05'] + housing['2009-06'])/3
new_dataframe.set_index(['State','RegionName'], inplace=True)

new_dataframe['PriceRatio'] = new_dataframe['2008q3'].div(new_dataframe['2009q2'])
new_dataframe = new_dataframe.reset_index()
univ_town = new_dataframe[new_dataframe['RegionName'].isin(df2['RegionName'])]
non_univ_town = new_dataframe[~new_dataframe['RegionName'].isin(df2['RegionName'])]

from scipy import stats

[p,statistic] = stats.ttest_ind(univ_town['PriceRatio'].dropna(), non_univ_town['PriceRatio'].dropna())
 

univ_town_mean = univ_town['PriceRatio'].mean()
non_univ_town_mean = non_univ_town['PriceRatio'].mean()

different = []

if (p<0.01):
    different= True
else:
    different= False

better = []
if (univ_town_mean < non_univ_town_mean):
    better = 'university town'
else:
    better = 'non-university town'
   
### Print a tuple that displays whether hypothesis is true or false, p value and category with lower mean
print((different),(p),(better))    
    

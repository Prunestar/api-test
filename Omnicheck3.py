#This is the termhist self check file that checks the values in termhist add up with that of itself


import requests
import numpy as np
import scipy as sp
import seaborn as sns
import pandas as pd
from collections import defaultdict
#import dateparser
from datetime import timedelta, date
import time
import itertools
from datetime import timedelta, date
import os
from Strategytest import q_filter 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print('termhist-self')
#creating dates to use for checking


current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Check '+q_filter)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
final_directoryterm=os.path.join(final_directory,r'Termhist-self')
if not os.path.exists(final_directoryterm):
   os.makedirs(final_directoryterm)
    
    
    

def check(a,b,c):
	checker2=[]
	checker=[]
	#defines blank lists to house data extracted from dicts
	tmp = defaultdict(list)    
	tmp2= defaultdict(list)
	tmp3= defaultdict(list)
	tmp4= defaultdict(list)
	tmp5= defaultdict(list)
	tmp6= defaultdict(list)

	#extracts data from the first loop
	for ii,j in enumerate(a):
		#print(j)
		#print(j)

		# loop over the return dict

		for iii,k  in enumerate(a[j]):#



			tmp2[j.encode('utf-8')].append(k)

			#print(iii,k)

			if ii==2:

				for iiii,l in enumerate(a[j][k]):
					#print(k,l)
					tmp[k.encode('utf-8')].append(l)

	#extracts data from the second dict
	for ii,j in enumerate(b):
		#print(j)

		# loop over the return dict

		for iii,k  in enumerate(b[j]):#


			tmp4[j.encode('utf-8')].append(k)
			#print(iii,k)

			if ii==2:

				for iiii,l in enumerate(b[j][k]):
					#print(k,l)
					tmp3[k.encode('utf-8')].append(l)

	#extracts data from the third dict
	for ii,j in enumerate(c):
		#print(j)

		# loop over the return dict

		for iii,k  in enumerate(c[j]):



			tmp6[j.encode('utf-8')].append(k)
		   # print(iii,k)

			if ii==2:

				for iiii,l in enumerate(c[j][k]):
					#print(k,l)
					tmp5[k.encode('utf-8')].append(l)

	#creates three dataframes that can be compared
	nofilter=pd.DataFrame(tmp,index=tmp2['x-axis'])
	#print(nofilter)
	#print(len(tmp4['x-axis']))
	truefilter=pd.DataFrame(tmp3,index=tmp4['x-axis'])
	#print(truefilter)
	falsefilter=pd.DataFrame(tmp5,index=tmp6['x-axis']) 
	#print(falsefilter)


	#subtracts the dataframes from one another to check if there is any indiscrepency
	#once found its location is assigned to x and y
	checker=truefilter.add(falsefilter,fill_value=0)
	checker2=nofilter.add(-checker,fill_value=0)
	#print(checker2)
	x,y= sp.sparse.coo_matrix(checker2!=0).nonzero()

	#this prints out the location of a misscount if one is found
	if len(x)==0:
		print('no issues found')
	else:
		checker2[checker2!=0].to_csv(os.path.join(final_directoryterm,filename))

def stylepercategorycheck(a,b,c):
    checker2=[]
    checker=[]
    #defines blank lists to house data extracted from dicts
    tmp = defaultdict(list)    
    tmp2= defaultdict(list)
    tmp3= defaultdict(list)
    tmp4= defaultdict(list)
    tmp5= defaultdict(list)
    tmp6= defaultdict(list)

    #loops over the first dict
    for ii,j in enumerate(a):
        

        # loop over the return dict

        for iii,k  in enumerate(a[j]):#

            if ii!=0:
				
				tmp2[j].append(k)

            #print(iii,k)

            if ii==0:

                for iiii,l in enumerate(a[j][k]):
                    #print(k,l)
                    tmp[k].append(l)

    #loops over the second dict
    for ii,j in enumerate(b):
        #print(j)

        # loop over the return dict

        for iii,k  in enumerate(b[j]):#

            if ii!=0:
                tmp4[j].append(k)
            #print(iii,k)

            if ii==0:

                for iiii,l in enumerate(b[j][k]):
                    #print(k,l)
                    tmp3[k].append(l)

    #loops over the third
    for ii,j in enumerate(c):
        #print(ii)

        # loop over the return dict

        for iii,k  in enumerate(c[j]):#

            if ii!=0:

                tmp6[j].append(k)
            #print(iii,k)

            if ii==0:

                for iiii,l in enumerate(c[j][k]):
                    #print(k,l)
                    tmp5[k].append(l)


    spcdf=pd.DataFrame(tmp,index=tmp2['x-axis']) #creates style per category pandas dataframe 
    oosspcdf=pd.DataFrame(tmp3,index=tmp4['x-axis'])
    ispcdf=pd.DataFrame(tmp5,index=tmp6['x-axis'])    
    checker=oosspcdf.add(ispcdf,fill_value=0)
	
    checker2=spcdf.add(-checker,fill_value=0)

    x,y= sp.sparse.coo_matrix(checker2!=0).nonzero()
    
    if len(x)!=0:
        checker2[checker2!=0].to_csv(os.path.join(final_directoryterm,filename))
    else:
		print('no issues found')
        



# should be env variables ....
un =  "hwGaKxk2Xv"
pw = "xayoA6yGXX4yHTaym5zz"
#un = "Zcoz4UKUAy"
#pw = "pWkeXqiON8ryZxTrEwwg"
data_base_url = "data.staging.omnilytics.co"
#data_base_url = "data.omnilytics.co"





#defining variables to be put into a string list
R=str('Retailer')
S=str('Style')
C=str('Category')
B=str('Brand')
D01=str('"Discount":{"from":0,"to":1}')
DT=str('"Discount":{"from":0,"to":100}')
D100=str('"Discount":{"from":1,"to":100}')
D=str('Discount')

RP=str('Replenished')
SZ=str("Size")
STK=str('Stock')
#creating lists to cycle through
Variable_list_term=[R,C,B,SZ]
Filter_list_term=[STK,RP]
#Discount_list=[DT,D010]


for a,b in itertools.permutations(Variable_list_term,2):
    if a!=b:
        if a==R:
            continue

        #defines three blank arrays to house the data for comparison
    
        for c in Filter_list_term:
			first=[]
			second=[]
			third=[]
			
			print(a+b+c)

			q = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '}}&groupby={"'+b+'":[]}'
			#print(q)
			data_url = "https://{}:{}@{}/".format(un,pw,data_base_url)+q
			r = requests.get(data_url)
			first.append(r.json())

			q2 = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '},"'+c+'":[true]}&groupby={"'+b+'":[]}'
			data_url2 = "https://{}:{}@{}/".format(un,pw,data_base_url)+q2
			r2 = requests.get(data_url2)
			second.append(r2.json())

			q3 = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '},"'+c+'":[false]}&groupby={"'+b+'":[]}'
			data_url3 = "https://{}:{}@{}/".format(un,pw,data_base_url)+q3
			r3 = requests.get(data_url3)
			third.append(r3.json())
			#print(third[0])
			#print(second[0]['x-axis'])
			#print(third[0])
			#print(first[0])
			filename='{}-{}-{}.csv'.format(a,b,c)



			if b==C:


				stylepercategorycheck(first[0],second[0],third[0])

			else:
				#print(first[0])
				check(first[0],second[0],third[0])
	first=[]
	second=[]
	third=[]
	print(a+b+'Discount')
	q = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '},'+DT+'}&groupby={"'+b+'":[]}'
	data_url = "https://{}:{}@{}/".format(un,pw,data_base_url)+q
	r = requests.get(data_url)
	first.append(r.json())



	q2 = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '},'+D01+'}&groupby={"'+b+'":[]}'
	data_url2 = "https://{}:{}@{}/".format(un,pw,data_base_url)+q2
	r2 = requests.get(data_url2)
	second.append(r2.json())



	q3 = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+ '},'+D100+'}&groupby={"'+b+'":[]}'
	data_url3 = "https://{}:{}@{}/".format(un,pw,data_base_url)+q3
	r3 = requests.get(data_url3)
	third.append(r3.json())

	filename='{}-{}-Discount.csv'.format(a,b)

	if b==C:
		stylepercategorycheck(first[0],second[0],third[0])

	else:

		check(first[0],second[0],third[0])

















import requests
import numpy as np
import scipy as sp
import seaborn as sns
import pandas as pd
from collections import defaultdict
import urllib
from datetime import timedelta, date
from Strategytest import q_filter 
import time
import itertools
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os

print('termhist-numberhist')
#creating dates to use for checking
#q_filter='"to":"2017-11-07","from":"2017-10-31"'

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Check '+q_filter)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
final_directorynum=os.path.join(final_directory,r'Termhist-Numberhist')
if not os.path.exists(final_directorynum):
   os.makedirs(final_directorynum)

# should be env variables ....
un =  "hwGaKxk2Xv"
pw = "xayoA6yGXX4yHTaym5zz"
#un = "Zcoz4UKUAy"
#pw = "pWkeXqiON8ryZxTrEwwg"
data_base_url = "data.staging.omnilytics.co"

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

def dataframe(item,b):
	
	tmp = defaultdict(list)    
	tmp2= defaultdict(list)


    #loops over the first dict
	for ii,j in enumerate(item):
		
        
		for iii,k  in enumerate(item[j]):
			if j=='x-axis':
				tmp2[j].append(k)
			if j=='Count':
				tmp[j].append(k)
		

				
	df=pd.DataFrame(tmp,index=tmp2['x-axis'])
	rsultlist=[df.sum()[0]-b,df.sum()[0]]
	return rsultlist
	
def check(a,two):
    #defines blank lists to house data extracted from dicts
    tmp = defaultdict(list)    
    tmp2= defaultdict(list)


    #extracts data from the first loop
    for ii,j in enumerate(a):
        #print(j)
        #print(j)

        # loop over the return dict

        for iii,k  in enumerate(a[j]):#



            tmp2[j].append(k)

            #print(k)

            if ii==2:
				
                for iiii,l in enumerate(a[j][k]):
					tmp[k].append(l)



	nofilter=pd.DataFrame(tmp,index=tmp2['x-axis'])
	#print(nofilter)
	soom= nofilter.sum(axis=0)
	#print(soom.index.values)
    indexlist=[]
    countlist=defaultdict(list)
    for i in range(0,len(soom.values)):

		#print(soom.index.values[i])
		compare=[]
		q = 'numberhist?interval=50&dimension=Price&currency=USD&filter={"'+two+'":["'+urllib.quote_plus((soom.index.values[i]).encode('utf-8'))+'"],"Available":{'+q_filter+'}}'
		data_url = "https://{}:{}@{}/".format(un,pw,data_base_url)+q
		#print(data_url)


		r = requests.get(data_url)

		compare.append(r.json())
		#print(compare)
		if (dataframe(compare[0],soom.values[i]))[0]!=0:
			indexlist.append(soom.index.values[i].encode('utf-8'))
			countlist['termhist'].append(soom.values[i])
			countlist['numbhist'].append(dataframe(compare[0],soom.values[i])[1])

    findf=pd.DataFrame(countlist,index=indexlist)
    findf.to_csv(os.path.join(final_directorynum,filename))
		
def categorybnumhist(a,two):
    #defines blank lists to house data extracted from dicts
    tmp = defaultdict(list)    
    tmp2= defaultdict(list)


    #extracts data from the first loop
    for ii,j in enumerate(a):
		#print(ii)
        #print(j)
		#print(j)

		# loop over the return dict

		for iii,k  in enumerate(a[j]):#


			if ii!=0:
				tmp2[j.encode('utf-8')].append(k)

				#print(k)

			if ii==0:

				for iiii,l in enumerate(a[j][k]):
					tmp[k].append(l)
	#print(tmp)
    #print(len(tmp2['x-axis']))

    nofilter=pd.DataFrame(tmp,index=tmp2['x-axis'])
    #print(nofilter)

    soom= nofilter.sum(axis=0)
	#print(soom.values)
    indexlist=[]
    countlist=defaultdict(list)
    for i in range(0,len(soom.values)):

	    #print(soom.index.values[i])
	    compare=[]
	    q = 'numberhist?interval=50&dimension=Price&currency=USD&filter={"'+two+'":["'+urllib.quote_plus((soom.index.values[i]).encode('utf-8'))+'"],"Available":{"to":"2017-11-07","from":"2017-10-31"}}'
	    data_url = "https://{}:{}@{}/".format(un,pw,data_base_url)+q

	    r = requests.get(data_url)

	    compare.append(r.json())
	    #print(compare)
	    if (dataframe(compare[0],soom.values[i]))[0]!=0:
			indexlist.append(soom.index.values[i])
			countlist['termhist'].append(soom.values[i])
			countlist['numbhist'].append(dataframe(compare[0],soom.values[i])[1])
			
    findf=pd.DataFrame(countlist,index=indexlist)
    findf.to_csv(os.path.join(final_directorynum,filename))
		
	

def checksz(a,two):
    #defines blank lists to house data extracted from dicts
    tmp = defaultdict(list)    
    tmp2= defaultdict(list)


    #extracts data from the first loop
    for ii,j in enumerate(a):
        #print(j)
        #print(j)

        # loop over the return dict

        for iii,k  in enumerate(a[j]):#



            tmp2[j].append(k)

            #print(k)

            if ii==2:
				
                for iiii,l in enumerate(a[j][k]):
					tmp[k].append(l)



	nofilter=pd.DataFrame(tmp,index=tmp2['x-axis'])
	#print(nofilter)
	soom= nofilter.sum(axis=0)
	#print(soom.index.values)
    indexlist=[]
    countlist=defaultdict(list)
    for i in range(87,98):

		print(soom.index.values[i])
		compare=[]
		q = 'numberhist?interval=50&dimension=Price&currency=USD&filter={"'+two+'":["'+urllib.quote_plus((soom.index.values[i]).encode('utf-8'))+'"],"Available":{'+q_filter+'}}'
		data_url = "https://{}:{}@{}/".format(un,pw,data_base_url)+q
		#print(data_url)


		r = requests.get(data_url)

		compare.append(r.json())
		#print(compare)
		if (dataframe(compare[0],soom.values[i]))[0]!=0:
			indexlist.append(soom.index.values[i])
			countlist['termhist'].append(soom.values[i])
			countlist['numbhist'].append(dataframe(compare[0],soom.values[i])[1])
			#print(countlist)

    findf=pd.DataFrame(countlist,index=indexlist)
    findf.to_csv(os.path.join(final_directorynum,filename))











#creating lists to cycle through
#Variable_list_num=[R,B]
Variable_list_num=[R,SZ,C,B]


for a,b in itertools.permutations(Variable_list_num,2):
	
	if a==R:
		continue
	if b==SZ:
		continue
		'''
		first=[]
		second=[]
		third=[]

		print(a+' '+b)


		qt = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+'}}&groupby={"'+b+'":[]}'
		data_urlt = "https://{}:{}@{}/".format(un,pw,data_base_url)+qt
		rt = requests.get(data_urlt)
		first.append(rt.json())
		print(data_urlt)
		filename='{}-{}.csv'.format(a,b)
		
		checksz(first[0],b)
		'''
	
	else:
		#defines three blank arrays to house the data for comparison
		first=[]
		second=[]
		third=[]

		print(a+' '+b)


		qt = 'termhist?dimension='+a+'&filter={"Available":{'+q_filter+'}}&groupby={"'+b+'":[]}'
		data_urlt = "https://{}:{}@{}/".format(un,pw,data_base_url)+qt
		print(data_urlt)
		rt = requests.get(data_urlt)
		first.append(rt.json())
		#print(data_urlt)
		filename='{}-{}.csv'.format(a,b)

		if b==C:
			categorybnumhist(first[0],b)
		
		else:

			check(first[0],b)
				
				

	
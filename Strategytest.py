#This is the strategy termhist file that checks that the numbers in strategy and termhist add up

import requests
import numpy as np
import scipy as sp
import seaborn as sns
import pandas as pd
from collections import defaultdict
import urllib
from datetime import timedelta, date
import time
import itertools
import math
import os
print('stratgey-termhist')
y1, m1, d1 = input("Enter the start year, month and day. e.g. 2012, 12, 25 : ")
y2, m2, d2 = input("Enter end date in same format : ")

Dates=[]
start_date = date(y1, m1, d1)
end_date = date(y2, m2, d2)
q_filter=('"from":"{}","to":"{}"'.format(start_date,end_date))

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Check '+q_filter)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
final_directorystrat=os.path.join(final_directory,r'Strategy-Termhist')
if not os.path.exists(final_directorystrat):
   os.makedirs(final_directorystrat)


# should be env variables ....
un =  "hwGaKxk2Xv"
pw = "xayoA6yGXX4yHTaym5zz"
#un = "Zcoz4UKUAy"
#pw = "pWkeXqiON8ryZxTrEwwg"
data_base_url = "data.staging.omnilytics.co"


#print(df)



R=str('Retailer')
S=str('Style')
C=str('Category')
B=str('Brand')
D01=str('"Discount":{"from":0,"to":1}')

D100=str('"Discount":{"from":1,"to":100}')
D=str('Discount')

RP=str('Replenished')
SZ=str("Size")
STK=str('Stock')

Var_list_strat=[R,B,S,C]
filter_list_strat=[RP,STK,D01,D100]
tf=['true','false']
second_strat=[0]

for Cat in Var_list_strat:
	#defines three blank arrays to house the data for comparison
	first=[]



	qt = 'strategy?filter={"Available":{'+q_filter+'}}&groupby={"'+Cat+'":[]}&size=10000000'
	#strategy does not require a dimension
	data_urlt = "https://{}:{}@{}/".format(un,pw,data_base_url)+qt
	rt = requests.get(data_urlt)
	first.append(rt.json())
	#print(data_urlt)
	#print(r.text)
	#first.append(r.json())

	tmp = defaultdict(list)    
	tmp2= defaultdict(list)
	hope=[]
	#print(len(first[0]['Retailer']))

	#creates dataframe from strategy url
	for iv,m in enumerate(first[0]):
		
		for ii,k in enumerate(first[0][m]):
			tmp=defaultdict(list)
			test=first[0][m][ii]

			for i,j in enumerate(test):
				if i==4 or i==6:	
					for ii,k in enumerate(test[j]):
						for iii,l in enumerate(k):
							hope.append(k[l])
						for iv in range(0,len(hope)):
							if type(hope[iv])==int:
								tmp[hope[iv+1].encode('utf-8')]=hope[iv]

				if i==1:
					tmp2[test[j].encode('utf-8')]=tmp
				if i==0 or i==3:
					tmp[j.encode('utf-8')]=test[j]


	df=pd.DataFrame(tmp2).transpose()
	#now creates the same dataframe but from the termhist api
	for b in filter_list_strat:
		print (b)
		#below produces the dataframe for discounts
		if b==D01 or b==D100:
			if b==D01:
				Index='Full Price'
			if b==D100:
				Index='Discount'
			qt = 'termhist?dimension='+Cat+'&Size=10000000000000&filter={"Available":{'+q_filter+'},'+b+'}'
			#strategy does not require a dimension
			data_urlt = "https://{}:{}@{}/".format(un,pw,data_base_url)+qt
			#print(data_urlt)
			rt = requests.get(data_urlt)
			second_strat[0]=(rt.json())
			
			tmp = defaultdict(list)    
			tmp2= []
			
			for ii,j in enumerate(second_strat[0]):


				for iii,k  in enumerate(second_strat[0][j]):
					if j=='x-axis':
						#print(			type)(k.encode('utf-8'))
						tmp2.append(k.encode('utf-8').replace('(','').replace(')','').replace(',',''))
					if j=='Count':
						tmp[Index].append(k)
			#print(tmp2)
			#print(tmp)
						
						
			df1=pd.DataFrame(tmp,index=tmp2)
			df2=pd.DataFrame(df1[Index] -df[Index])
			filename='{}-{}-{}.csv'.format(Cat,b,Index)
			df3=df2[df2[Index].notnull()]
			df3[df3[Index]!=0].to_csv(os.path.join(final_directorystrat,filename))
		else:
			#the next part does the same thing but for the other variables
			for troo in tf:

				qt = 'termhist?dimension='+Cat+'&Size=10000000000000&filter={"Available":{'+q_filter+'},"'+b+'":['+troo+']}'
				#strategy does not require a dimension
				data_urlt = "https://{}:{}@{}/".format(un,pw,data_base_url)+qt
				#print(data_urlt)
				rt = requests.get(data_urlt)
				second_strat[0]=(rt.json())


				tmp = defaultdict(list)    
				tmp2= []



				if b==RP:
					if troo=='true':
						Index='Replenishment'
					if troo=='false':
						continue
				if b==STK:
					if troo=='true':
						Index='In Stock'
					if troo=='false':
						Index='Out of Stock'
				#loops over the first dict
				for ii,j in enumerate(second_strat[0]):


					for iii,k  in enumerate(second_strat[0][j]):
						if j=='x-axis':
							#print(			type)(k.encode('utf-8'))
							tmp2.append(k.encode('utf-8').replace('(','').replace(')','').replace(',',''))
						if j=='Count':
							tmp[Index].append(k)


				df1=pd.DataFrame(tmp,index=tmp2)
				#once both dataframes are made the difference is taken
				df2=pd.DataFrame(df1[Index] -df[Index])
				filename='{}-{}-{}.csv'.format(Cat,b,Index)
				#where the difference is not zero a csv is saved 
				df3=df2[df2[Index].notnull()]
				df3[df3[Index]!=0].to_csv(os.path.join(final_directorystrat,filename))





				
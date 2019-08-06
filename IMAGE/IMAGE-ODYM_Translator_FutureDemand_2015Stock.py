# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:10:36 2019

@author: sklose
"""

# -*- coding: utf-8 -*-
"""
File CDLINKS_MESSAGEix-ODYM_Translator

Parse, evaluate, and export IAM scenario results for Electricity generation technologies

"""
# Import required libraries:
import os
import sys
import logging as log
import xlrd, xlwt
import numpy as np
import time
import datetime
import scipy.io
import scipy
import pandas as pd
import shutil   
import uuid
import matplotlib.pyplot as plt   
import importlib
import getpass
from copy import deepcopy
from tqdm import tqdm
from scipy.interpolate import interp1d
import pylab
import seaborn as sns

import xlsxwriter
import openpyxl
from dynamic_stock_model import DynamicStockModel

#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

import imp
import sys
sys.path.append("C:/Users/sklose/Documents/ODYM-RECC-Repos/RECC-Cu-Repo/ODYM-RECC Cu/")

import RECC_Paths # Import path file

#imp.load_source(RECC_Paths , 'C:/Users/sklose/Documents/ODYM-RECC-Repos/RECC-Cu-Repo/ODYM-RECC Cu/RECC_Paths.py') 

DFilePathIMAGE = RECC_Paths.rawdata_pathIMAGE
ResultsPath= os.path.join(RECC_Paths.data_path_raw)
## Define indices for MESSAGE data
#Regions_M  = ['AFR','CPA','EEU','FSU','LAC','MEA','NAM','PAO','PAS','SAS','WEU','World']
#Model_M    = ['CD_Links_SSP1_v2','CD_Links_SSP2_v2','CD_Links_SSP3_v2']
#Scenario_M = ['NPi','NPi2020_1000'] # for BAU/no policy scenario after 2030 and 2dC scenario
#Years_M    = [1990,1995,2000,2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100,2110]
## For meaning of scenarios, cf. https://db1.ene.iiasa.ac.at/CDLINKSDB/dsd?Action=htmlpage&page=10
#
## Define indices for ODYM-RECC data
#Scenario_R = ['SSP1','SSP2','SSP3']
#RCPScen_R  = ['Baseline(unmitigated)','RCP2.6']
#Regions_R  = ['R32CAN','R32CHN','R32EU12-M','R32IND','R32JPN','R32USA','France','Germany','Italy','Poland','Spain','UK','Oth_R32EU15','Oth_R32EU12-H','World']
#Time_R     = np.arange(2000,2101,1)
#TimeL_R    = [i for i in Time_R] 
## Read data into pandas dataframe:
DF_Inflow = pd.read_excel(os.path.join(DFilePathIMAGE,'1_F_MetalDemand_appliances_DEETMAN_2018.xlsx'), sep = ',', encoding = 'unicode_escape', sheet_name='Data')



DF_Lifetime = pd.read_excel(os.path.join(DFilePathIMAGE,'DEETMAN_3_LT_RECC_ProductLifetime_appliances_V1.0.xlsx'), sep = ',', encoding = 'unicode_escape', sheet_name='Data')



Par_Sigma = (DF_Lifetime['stats_array_4']).values
Par_Lifetime = (DF_Lifetime['value']).values
DF_Inflow_s = DF_Inflow[['aspect 6 : commodity','aspect 5 : time','aspect 4 : scenario','value']]

Scenarios = ['SSP1', 'SSP2', 'SSP2_450ppm', 'SSP3']

Products = ['Fan', 'Air-cooler' ,'Air-conditioning', 'Refridgerator','Microwave', 'Washing Machine', 'Tumble dryer','Dish washer',
            'Television','VCR/DVD player','PC & Laptop computers','Other small appliances']


time_total = np.arange(1971,2051)
time_Historic= np.arange(1971,2016)

time_Future= np.arange(2016,2051)


Par_inflow_hist = np.zeros((len(Scenarios),len(time_Historic),len(Products)))

for s in range (0, len(Scenarios)):
    for p in range (0, len(Products)):
        for t in range (0, len(time_Historic)):
            Par_inflow_hist[s,t,p] = DF_Inflow_s['value'].loc[(DF_Inflow_s['aspect 6 : commodity']==Products[p]) & (DF_Inflow_s['aspect 5 : time']==time_Historic[t]) & (DF_Inflow_s['aspect 4 : scenario']==Scenarios[s])]

#
#Lifetime = np.zeros((len(time_Historic),len(Products)))
#
#for t in range (0, len(time_Historic)):
#    Lifetime[t,:] = Par_Lifetime[:]
#    
#Sigma = np.zeros((len(time_Historic),len(Products)))
#
#for t in range (0, len(time_Historic)):
#    Sigma[t,:] = Par_Sigma[:]
#    
#timeDSM = time_Historic
#
#LifetimeDSM = Lifetime[:,:]
#StdDevDSM = Sigma[:,:]
#
#Stock_by_cohort = np.zeros((len(Scenarios),len(Products),len(time_Historic),len(time_Historic)))
#
#appended_S_C_2015 = []
#
#for p in range (0,len(Products)):
#    for s in range (0, len(Scenarios)):
#        DSM= DynamicStockModel(t = timeDSM-1971, i = Par_inflow_hist[s,:,p], lt = {'Type': 'Normal', 'Mean': Lifetime[:,p], 'StdDev': Sigma[:,p] })
#
#        Stock_by_cohort[s,p,:,:] = DSM.compute_s_c_inflow_driven()
#
#        S_C_2015 = pd.DataFrame({'Stock in Year':'2015','Year':time_Historic,'Scenario':Scenarios[s],'RCP_Scen':'Baseline(unmitigated)','Product':Products[p],'Value':Stock_by_cohort[s,p,44,:]}) #Value: Stock in 2015
#
#        S_C_2015 = S_C_2015[['Stock in Year','Year','Scenario','RCP_Scen','Product','Value']]
#        
#        appended_S_C_2015.append(S_C_2015)
#    
#appened_S_C_2015 = pd.concat(appended_S_C_2015)
#
#
##Replace IMAGE Scenario names with ODYM Scenario names
#Scenario_ODYM = ['SSP1','SSP2','SSP3']
#RCPScen_ODYM  = ['Baseline(unmitigated)','RCP2.6']
#
#appened_S_C_2015.loc[appened_S_C_2015.Scenario == 'SSP2_450ppm', 'RCP_Scen'] = 'RCP2.6'
#appened_S_C_2015['Scenario'].replace(   to_replace='SSP2_450ppm',value='SSP2',   inplace=True)    
#
##appened_S_C_2015.loc[appened_S_C_2015.Scenario.isin('SSP1','SSP2'), 'RCP_Scen'] = 
#
#        
#book=openpyxl.load_workbook(ResultsPath+'\\2_S_RECC_FinalProducts_2015_appliances_V1.0_raw.xlsx' )
##        
#writer=pd.ExcelWriter(ResultsPath+'\\2_S_RECC_FinalProducts_2015_appliances_V1.0_raw.xlsx', engine='openpyxl')
##
#writer.book=book
##
#writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
##
#appened_S_C_2015.to_excel(writer, sheet_name='values',startcol=0,startrow=0,index=False,header=True)
#            
##
#writer.save()


###### Create RECC 1_F_RECC_FinalProducts_Future_appliances

Par_demand_future = DF_Inflow_s.loc[DF_Inflow_s['aspect 5 : time'].isin(time_total)]
Par_demand_future = Par_demand_future.loc[Par_demand_future['aspect 6 : commodity'].isin(Products)]
Par_demand_future = Par_demand_future.loc[Par_demand_future['aspect 4 : scenario'].isin(Scenarios)]


Par_demand_future = Par_demand_future.rename({'aspect 6 : commodity': 'Product', 
                                              'aspect 5 : time': 'Year', 
                                              'aspect 4 : scenario': 'Scenario',
                                              'value':'Value'}, axis='columns')

Par_demand_future['RCP_Scen']='Baseline(unmitigated)'

Par_demand_future.loc[Par_demand_future.Scenario == 'SSP2_450ppm', 'RCP_Scen'] = 'RCP2.6'
Par_demand_future['Scenario'].replace(   to_replace='SSP2_450ppm',value='SSP2',   inplace=True)  

Par_demand_future = Par_demand_future[['Year','Scenario','RCP_Scen','Product','Value']]



book=openpyxl.load_workbook(ResultsPath+'\\1_F_RECC_FinalProducts_Future_appliances_V1.0_raw.xlsx' )
#        
writer=pd.ExcelWriter(ResultsPath+'\\1_F_RECC_FinalProducts_Future_appliances_V1.0_raw.xlsx', engine='openpyxl')
#
writer.book=book
#
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#
Par_demand_future.to_excel(writer, sheet_name='values',startcol=0,startrow=0,index=False,header=True)
            
#
writer.save()

## The end.


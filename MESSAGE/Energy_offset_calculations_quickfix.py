# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:34:42 2019

@author: sklose
"""

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

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import imp



#imp.reload( RECC_Paths )
import RECC_Paths # Import path file



DFilePathMESSAGE = RECC_Paths.rawdata_pathMESSAGE
ResultsPath= os.path.join(RECC_Paths.rawdata_path,'Data','Raw')
# Define indices for MESSAGE data
Regions_M  = ['AFR','CPA','EEU','FSU','LAC','MEA','NAM','PAO','PAS','SAS','WEU','World']
Model_M    = ['CD_Links_SSP1_v2_release_1.2_emiupd','CD_Links_SSP2_v2','CD_Links_SSP3_v2','CD_Links_SSP2_v2_release_1.2_emiupd']
Scenario_M = ['NPi','NPi2020_1000','LED_v0.3'] # for BAU/no policy scenario after 2030 and 2dC scenario
Years_M    = [1990,1995,2000,2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100,2110]
# For meaning of scenarios, cf. https://db1.ene.iiasa.ac.at/CDLINKSDB/dsd?Action=htmlpage&page=10

# Define indices for ODYM-RECC data
Scenario_R = ['SSP1','SSP2','SSP3','LED']
RCPScen_R  = ['Baseline(unmitigated)','RCP2.6','RCP2.6']
Regions_R  = ['R32CAN','R32CHN','R32EU12-M','R32IND','R32JPN','R32USA','France','Germany','Italy','Poland','Spain','UK','Oth_R32EU15','Oth_R32EU12-H','World']
Time_R     = np.arange(2000,2101,1)
TimeL_R    = [i for i in Time_R] 
# Read data into pandas dataframe:
DF = pd.read_csv(os.path.join(DFilePathMESSAGE,'CD_Links_SSP1-3.csv'), sep = ',', encoding = 'unicode_escape')

DF_LEDadded = pd.read_csv(os.path.join(DFilePathMESSAGE,'messageix_native_20190808-134140.csv'), sep = ',', encoding = 'unicode_escape')

DF_LEDadded.head(5)

Path_Copper_GW = os.path.join(DFilePathMESSAGE) + '\\Copper_MI.xlsx'   ##Import Data on Material Intensity of kommer [kt/GW]
CopperGW_WB_df = pd.read_excel(Path_Copper_GW)

CopperGW_WB_df.set_index(CopperGW_WB_df['VARIABLE'])



print(DF_LEDadded.shape)
print(len(DF_LEDadded.index))
list(DF_LEDadded.columns.values) # all columns used


       
    
####
# Translate Capacity additions into RECC model dataformat
###





Useful_Energy_MSG = ['Useful Energy|Input|Industrial Specific']


Emissions_MSG = ['Emissions|CO2']



#### Convert MESSAGE Cappacity Addition data in ODYM format

DF_UE_MSG= DF.loc[DF['VARIABLE'].isin(Useful_Energy_MSG) & DF['SCENARIO'].isin(Scenario_M) & DF['MODEL'].isin(Model_M)] # extract emissions from energy supply, in Mt CO2/yr
        
[DF_UE_MSG['MODEL'].replace(   to_replace=[Model_M[i]],value=Scenario_R[i],   inplace=True) for i in range(0,3)]
[DF_UE_MSG['SCENARIO'].replace(to_replace=[Scenario_M[i]],value=RCPScen_R[i], inplace=True) for i in range(0,2)]


DF_EM_MSG = DF.loc[DF['VARIABLE'].isin(Emissions_MSG) & DF['SCENARIO'].isin(Scenario_M) & DF['MODEL'].isin(Model_M)]
[DF_EM_MSG['MODEL'].replace(   to_replace=[Model_M[i]],value=Scenario_R[i],   inplace=True) for i in range(0,3)]
[DF_EM_MSG['SCENARIO'].replace(to_replace=[Scenario_M[i]],value=RCPScen_R[i], inplace=True) for i in range(0,2)]

Emissions_SSP2_Baseline=DF_UE_MSG[(DF_UE_MSG.MODEL == 'SSP2') & (DF_UE_MSG.SCENARIO  == 'Baseline(unmitigated)') & (DF_UE_MSG.REGION  == 'World')]
Emissions_SSP2_Mitigated=DF_UE_MSG[(DF_UE_MSG.MODEL == 'SSP2') & (DF_UE_MSG.SCENARIO  == 'RCP2.6') & (DF_UE_MSG.REGION  == 'World')]

dEmissions_SSP2_Baseline = Emissions_SSP2_Baseline.loc[:, (Emissions_SSP2_Baseline != 0).any(axis=0)] ##delete columns that are zero
dEmissions_SSP2_Mitigated = Emissions_SSP2_Mitigated.loc[:, (Emissions_SSP2_Mitigated != 0).any(axis=0)] ##delete columns that are zero




#####Create stepfunction and expand input file to every year input
col_1990 = np.arange(1986,1990)
col_1990j = " ".join(str(x) for x in col_1990)
col_1990s = col_1990j.split()

col_1995 = np.arange(1991,1995)
col_1995j = " ".join(str(x) for x in col_1995)
col_1995s = col_1995j.split()

col_2000 = np.arange(1996,2000)
col_2000j = " ".join(str(x) for x in col_2000)
col_2000s = col_2000j.split()  

col_2005 = np.arange(2001,2005)
col_2005j = " ".join(str(x) for x in col_2005)
col_2005s = col_2005j.split()  

col_2010 = np.arange(2006,2010)
col_2010j = " ".join(str(x) for x in col_2010)
col_2010s = col_2010j.split()  

col_2020 = np.arange(2011,2020)
col_2020j = " ".join(str(x) for x in col_2020)
col_2020s = col_2020j.split()  

col_2030 = np.arange(2021,2030)
col_2030j = " ".join(str(x) for x in col_2030)
col_2030s = col_2030j.split()  

col_2040 = np.arange(2031,2040)
col_2040j = " ".join(str(x) for x in col_2040)
col_2040s = col_2040j.split()  

col_2050 = np.arange(2041,2050)
col_2050j = " ".join(str(x) for x in col_2050)
col_2050s = col_2050j.split()  

col_2060 = np.arange(2051,2060)
col_2060j = " ".join(str(x) for x in col_2060)
col_2060s = col_2060j.split()  

col_2070 = np.arange(2061,2070)
col_2070j = " ".join(str(x) for x in col_2070)
col_2070s = col_2070j.split()  

col_2080 = np.arange(2071,2080)
col_2080j = " ".join(str(x) for x in col_2080)
col_2080s = col_2080j.split()  

col_2090 = np.arange(2081,2090)
col_2090j = " ".join(str(x) for x in col_2090)
col_2090s = col_2090j.split()  

col_2100 = np.arange(2091,2100)
col_2100j = " ".join(str(x) for x in col_2100)
col_2100s = col_2100j.split()  

col_2110 = np.arange(2101,2110)
col_2110j = " ".join(str(x) for x in col_2110)
col_2110s = col_2110j.split()  

ddCAexp0 = pd.concat([Emissions_SSP2_Baseline, pd.DataFrame(columns = col_1990s )],sort=True)
ddCAexp1 = pd.concat([ddCAexp0, pd.DataFrame(columns = col_1995s )],sort=True)
ddCAexp2 = pd.concat([ddCAexp1, pd.DataFrame(columns = col_2000s )],sort=True)
ddCAexp3 = pd.concat([ddCAexp2, pd.DataFrame(columns = col_2005s )],sort=True)
ddCAexp4 = pd.concat([ddCAexp3, pd.DataFrame(columns = col_2010s )],sort=True)
ddCAexp5 = pd.concat([ddCAexp4, pd.DataFrame(columns = col_2020s )],sort=True)
ddCAexp6 = pd.concat([ddCAexp5, pd.DataFrame(columns = col_2030s )],sort=True)
ddCAexp7 = pd.concat([ddCAexp6, pd.DataFrame(columns = col_2040s )],sort=True)
ddCAexp8 = pd.concat([ddCAexp7, pd.DataFrame(columns = col_2050s )],sort=True)
ddCAexp9 = pd.concat([ddCAexp8, pd.DataFrame(columns = col_2060s )],sort=True)
ddCAexp10 = pd.concat([ddCAexp9, pd.DataFrame(columns = col_2070s )],sort=True)
ddCAexp11 = pd.concat([ddCAexp10, pd.DataFrame(columns = col_2080s )],sort=True)
ddCAexp12 = pd.concat([ddCAexp11, pd.DataFrame(columns = col_2090s )],sort=True)
ddCAexp13 = pd.concat([ddCAexp12, pd.DataFrame(columns = col_2100s )],sort=True)
ddCAexp14 = pd.concat([ddCAexp13, pd.DataFrame(columns = col_2100s )],sort=True)
ddCAexp15 = pd.concat([ddCAexp14, pd.DataFrame(columns = col_2110s )],sort=True)

for c in col_1990s:
    ddCAexp15[c] = ddCAexp15['1990']
for c in col_1995s:
    ddCAexp15[c] = ddCAexp15['1995']
for c in col_2000s:
    ddCAexp15[c] = ddCAexp15['2000']
for c in col_2005s:
    ddCAexp15[c] = ddCAexp15['2005']
for c in col_2010s:
    ddCAexp15[c] = ddCAexp15['2010']
for c in col_2020s:
    ddCAexp15[c] = ddCAexp15['2020']
for c in col_2030s:
    ddCAexp15[c] = ddCAexp15['2030']
for c in col_2040s:
    ddCAexp15[c] = ddCAexp15['2040']
for c in col_2050s:
    ddCAexp15[c] = ddCAexp15['2050']
for c in col_2060s:
    ddCAexp15[c] = ddCAexp15['2060']
for c in col_2070s:
    ddCAexp15[c] = ddCAexp15['2070']
for c in col_2080s:
    ddCAexp15[c] = ddCAexp15['2080']
for c in col_2090s:
    ddCAexp15[c] = ddCAexp15['2090']
for c in col_2100s:
    ddCAexp15[c] = ddCAexp15['2100']
for c in col_2110s:
    ddCAexp15[c] = ddCAexp15['2110']


dEmissions_SSP2_Baseline = ddCAexp15

dEmissions_SSP2_Baseline.drop('MODEL', axis=1, inplace=True)
dEmissions_SSP2_Baseline.drop('REGION', axis=1, inplace=True)
dEmissions_SSP2_Baseline.drop('SCENARIO', axis=1, inplace=True)
dEmissions_SSP2_Baseline.drop('UNIT', axis=1, inplace=True)
dEmissions_SSP2_Baseline.drop('VARIABLE', axis=1, inplace=True)


#########


ddCAexp0 = pd.concat([Emissions_SSP2_Mitigated, pd.DataFrame(columns = col_1990s )],sort=True)
ddCAexp1 = pd.concat([ddCAexp0, pd.DataFrame(columns = col_1995s )],sort=True)
ddCAexp2 = pd.concat([ddCAexp1, pd.DataFrame(columns = col_2000s )],sort=True)
ddCAexp3 = pd.concat([ddCAexp2, pd.DataFrame(columns = col_2005s )],sort=True)
ddCAexp4 = pd.concat([ddCAexp3, pd.DataFrame(columns = col_2010s )],sort=True)
ddCAexp5 = pd.concat([ddCAexp4, pd.DataFrame(columns = col_2020s )],sort=True)
ddCAexp6 = pd.concat([ddCAexp5, pd.DataFrame(columns = col_2030s )],sort=True)
ddCAexp7 = pd.concat([ddCAexp6, pd.DataFrame(columns = col_2040s )],sort=True)
ddCAexp8 = pd.concat([ddCAexp7, pd.DataFrame(columns = col_2050s )],sort=True)
ddCAexp9 = pd.concat([ddCAexp8, pd.DataFrame(columns = col_2060s )],sort=True)
ddCAexp10 = pd.concat([ddCAexp9, pd.DataFrame(columns = col_2070s )],sort=True)
ddCAexp11 = pd.concat([ddCAexp10, pd.DataFrame(columns = col_2080s )],sort=True)
ddCAexp12 = pd.concat([ddCAexp11, pd.DataFrame(columns = col_2090s )],sort=True)
ddCAexp13 = pd.concat([ddCAexp12, pd.DataFrame(columns = col_2100s )],sort=True)
ddCAexp14 = pd.concat([ddCAexp13, pd.DataFrame(columns = col_2100s )],sort=True)
ddCAexp15 = pd.concat([ddCAexp14, pd.DataFrame(columns = col_2110s )],sort=True)

for c in col_1990s:
    ddCAexp15[c] = ddCAexp15['1990']
for c in col_1995s:
    ddCAexp15[c] = ddCAexp15['1995']
for c in col_2000s:
    ddCAexp15[c] = ddCAexp15['2000']
for c in col_2005s:
    ddCAexp15[c] = ddCAexp15['2005']
for c in col_2010s:
    ddCAexp15[c] = ddCAexp15['2010']
for c in col_2020s:
    ddCAexp15[c] = ddCAexp15['2020']
for c in col_2030s:
    ddCAexp15[c] = ddCAexp15['2030']
for c in col_2040s:
    ddCAexp15[c] = ddCAexp15['2040']
for c in col_2050s:
    ddCAexp15[c] = ddCAexp15['2050']
for c in col_2060s:
    ddCAexp15[c] = ddCAexp15['2060']
for c in col_2070s:
    ddCAexp15[c] = ddCAexp15['2070']
for c in col_2080s:
    ddCAexp15[c] = ddCAexp15['2080']
for c in col_2090s:
    ddCAexp15[c] = ddCAexp15['2090']
for c in col_2100s:
    ddCAexp15[c] = ddCAexp15['2100']
for c in col_2110s:
    ddCAexp15[c] = ddCAexp15['2110']


dEmissions_SSP2_Mitigated = ddCAexp15

dEmissions_SSP2_Mitigated.drop('MODEL', axis=1, inplace=True)
dEmissions_SSP2_Mitigated.drop('REGION', axis=1, inplace=True)
dEmissions_SSP2_Mitigated.drop('SCENARIO', axis=1, inplace=True)
dEmissions_SSP2_Mitigated.drop('UNIT', axis=1, inplace=True)
dEmissions_SSP2_Mitigated.drop('VARIABLE', axis=1, inplace=True)



book=openpyxl.load_workbook(ResultsPath+'\\Energy_offset_calculations.xlsx' )
        
writer=pd.ExcelWriter(ResultsPath+'\\Energy_offset_calculations.xlsx', engine='openpyxl')

writer.book=book

writer.sheets = dict((ws.title, ws) for ws in book.worksheets)


DF_UE_MSG.to_excel(writer, sheet_name='UE',startcol=0,startrow=0,index=False,header=True)

DF_EM_MSG.to_excel(writer, sheet_name='EM',startcol=0,startrow=0,index=False,header=True)

writer.save()
# The end.
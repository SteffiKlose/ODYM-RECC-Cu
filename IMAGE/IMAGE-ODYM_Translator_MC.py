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

## Read data into pandas dataframe:
DF_MC = pd.read_excel(os.path.join(DFilePathIMAGE,'3_MC_RECC_appliances_DEETMAN_2018.xlsx'), sep = ',', encoding = 'unicode_escape', sheet_name='Data')


DF_MC_s = DF_MC[['aspect 1 : commodity', 'aspect 2 : element', 'aspect 3 : scenario', 'value']]

Scenarios = ['SSP1', 'SSP2', 'SSP2_450ppm', 'SSP3']

Products = ['Fan', 'Air-cooler' ,'Air-conditioning', 'Refridgerator','Microwave', 'Washing Machine', 'Tumble dryer','Dish washer',
            'Television','VCR/DVD player','PC & Laptop computers','Other small appliances']

Element = ['copper']

DF_MC_s = DF_MC_s.loc[DF_MC_s['aspect 1 : commodity'].isin(Products)]
DF_MC_s = DF_MC_s.loc[DF_MC_s['aspect 2 : element'].isin(Element)]


DF_MC_s = DF_MC_s.rename({'aspect 1 : commodity': 'Product', 
                          'aspect 2 : element': 'Commodity', 
                          'aspect 3 : scenario': 'Scenario',
                          'value':'Value'}, axis='columns')

DF_MC_s_mean = []
DF_MC_s_mean = DF_MC_s.groupby(['Product']).mean()

DF_MC_s_diff = []
DF_MC_s['Diff'] = DF_MC_s.groupby('Product')['Value'].diff()

DF_MC_s_diff = DF_MC_s[['Product','Commodity','Diff']]

DF_MC_s_diff = DF_MC_s_diff.dropna()

DF_MC_mean_diff = DF_MC_s_mean.merge(DF_MC_s_diff, on = ['Product'])

DF_MC_mean_diff = DF_MC_mean_diff[['Product','Commodity','Value', 'Diff']]

        
book=openpyxl.load_workbook(ResultsPath+'\\3_MC_RECC_appliances_V1.0.xlsx' )
#        
writer=pd.ExcelWriter(ResultsPath+'\\3_MC_RECC_appliances_V1.0.xlsx', engine='openpyxl')
#
writer.book=book
#
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#
DF_MC_mean_diff.to_excel(writer, sheet_name='values',startcol=0,startrow=0,index=False,header=True)
            
#
writer.save()



## The end.


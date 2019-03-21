
# coding: utf-8

# load packages
import pandas as pd
import glob, os

# select directory
path = r'/data/private/wemc/100WS/100WS_nc/nuts0/'

# create list of available years
years = ['S1979','S1980','S1981','S1982','S1983','S1984',
         'S1985','S1986','S1987','S1988','S1989','S1990',
         'S1991','S1992','S1993','S1994','S1995','S1996',
         'S1997','S1998','S1999','S2000','S2001','S2002',
         'S2003','S2004','S2005','S2006','S2007','S2008',
         'S2009','S2010','S2011','S2012','S2013','S2014',
         'S2015','S2016','S2017','S2018']

# set first year in list
year = years[0]

# specify nuts level for filenaming purposes
nuts = 'nut0'

# check for previous merged file and delete if present
for filename in glob.glob(path + "/H_*"):
    os.remove(filename) 
    
# find all .csv files and add to list    
allFiles = [os.path.basename(x) for x in glob.glob(path + r"/*.csv")]

for year in years:
    # empty list for populating with csv data
    list_ = []
    # empty list for filenaming purposes
    namelong = []
    for file_ in allFiles:
        name = os.path.splitext(file_)[0]
        if year in name:
            namelong.append(name)
            name = name[:2]
            df = pd.read_csv(file_, index_col=0, header=None, low_memory=False)
            df.rename(columns={1: name}, inplace=True)
            list_.append(df)
            frame = pd.concat(list_, axis = 1, sort=True)
            frame = frame.groupby(axis=1, level=0).first()
            # create filename from input file
            filename1 = namelong[0]
            filename2 = namelong[-1]
            # append nuts level to filename, remove country abbreviation and add csv extension
            csvname = filename1[3:36] + nuts + filename1[40:55] + filename2[55:] + '.csv'
            frame.to_csv(csvname)

print("completed merge")

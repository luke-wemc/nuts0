
# coding: utf-8

# load packages
import pandas as pd
import glob, os

# select directory
path = r'/data/private/wemc/100WS/100WS_nc/nuts0/'

# select directory for outputted appended file
outpath = '/data/private/wemc/nuts0_averages/'

# specify nuts level for filenaming purposes
nuts = 'nut0'

# empty list for populating with csv data
list_ = []

# empty list for filenaming purposes
namelong = []
    
# find all .csv files in directory and add to list    
allFiles = [os.path.basename(x) for x in glob.glob("H_*")]

# sort files, will sort via date (if files are correctly named as per DMP)
allFiles.sort()

# add nuts2 filenames to namelong list for output filenaming purposes   
for file in allFiles:
    name = os.path.splitext(file)[0]
    if  nuts in name:
        namelong.append(name)      

# create filename from input file
filename1 = namelong[0]
filename2 = namelong[-1]

# append nuts level to filename, remove country abbreviation and add csv extension
csvname = filename1[0:42] + filename2[42:] + '.csv'

# check for previous merged file and delete if present
# broken needs fixing before using
for filename in glob.glob(outpath + '/' + csvname):
    os.remove(filename) 
    print("checking for previous merged file and deleting if present...")

# find all .csv files in directory and add to list    
allFiles = [os.path.basename(x) for x in glob.glob("H_*")]
allFiles.sort()

# combine csv files if nuts id in filename
combined_csv = pd.concat([pd.read_csv(file) for file in allFiles if nuts in name], axis=0, ignore_index=True, sort=True)
print("combining merged nuts files...")

# add metadata - check this information is correct before running

metadata = ["""
## General
### Title
10 metre wind speed
### Abstract 
ERA5 reanalysis data 
### Date
2019-02-01
### Date type
Publication: Date identifies when the data was issued
### Unit
m s-1
### URL
NA
### Data format
CSV (according to Request for Comments [RFC] 4180, see: https://tools.ietf.org/html/rfc4180)
### Keywords
10 metre, wind, reanalysis
### Point of contact
#### Individual name
Luke Sanger
####Electronic mail address
luke.sanger@wemcouncil.org
#### Organisation name
World Energy & Meteorology Council
#### Role
Owner: Party that owns the resource
##Usage
### Access constraints
Intellectual property rights: The IP of these data belongs to the EU Copernicus programme 
### Use constraints
[this is an example, you may use the Creative commons licence] Copyright: Exclusive right to the publication, production, or sale of the rights to a literary, dramatic, musical, or artistic work, or to the use of a commercial print or label, granted by law for a specified period of time to an author, composer, artist, distributor
### Citation(s)
NA
## Temporal extent
### Begin date
1979-01-01
### End date
2017-12-31
### Temporal resolution
Hourly
### Geographic bounding box
westBoundLongitude -22.00
eastBoundLongitude 45.00
southBoundLatitude 27.00
northBoundLatitude 72.00
### Spatial resolution 
Country scale
## Lineage Statement
### Original Data Source
### Statement
The original data sources are ECMWF ERA5 Reanalysis (available at: https://cds.climate.copernicus.eu) 
_
"""]

# shift dataframe down one row
cv = combined_csv.shift(periods=1, freq=None, axis=0)

# insert metadata in first row
cv.iloc[0,0] = metadata

# remove numbered index
cv.set_index('0', inplace=True)

# rename time index for convenience
cv.index.names = ['Time']

# save to csv, in nuts output directory (defined at beginning of script)

cv.to_csv(outpath + csvname)

print("completed csv append and saved to " + nuts + " directory in /data/private/resources")


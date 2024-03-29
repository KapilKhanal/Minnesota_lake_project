import numpy as np
import pandas as pd
from dfply import *
from toolz import first
from functools import reduce
import os 

CHUNK_SIZE  = 500
files = os.listdir("./Data/MinneMUDAC/")
filePaths = ['./Data/MinneMUDAC/'+ file for file in files if not file=="references"]
filePaths.remove("./Data/MinneMUDAC/.ipynb_checkpoints")
filePaths.remove('./Data/MinneMUDAC/.DS_Store')
filePaths.remove('./Data/MinneMUDAC/mces_lakes_1999_2014.txt')

def read_chunk(file,size):
    chunk = pd.read_csv(file,chunksize=size,sep = "|")
    return chunk

df_iterators = [read_chunk(filePath,CHUNK_SIZE) for filePath in filePaths[1:]]
first_chunks = [first(df) for df in df_iterators]
cols_set = [set(df.columns) for df in first_chunks]


def get_common(list_set):
     return set(reduce(lambda s1,s2:s1.intersection(s2),list_set))

common_columns = get_common(cols_set)

common_columns_df  = pd.DataFrame.from_records(list(common_columns))
common_columns_df.to_csv("Data/parcel_common_columns_2004_2014.csv")

lake = pd.read_csv('./data/MinneMUDAC/mces_lakes_1999_2014.txt', sep = '\t', dtype= {'longitude': 'str', 'latitude': 'str'})

monitor = pd.read_csv('./Data/MinneMUDAC/references/Parcel_Lake_Monitoring_Site_Xref.txt', sep= "\t", dtype = {'centroid_long': 'str', 'centroid_lat': 'str' })

lake_set = set(lake.DNR_ID_Site_Number)
monitor_set = set(monitor.Monit_MAP_CODE1)
common_id = lake_set.intersection(monitor_set)

diff_codes_lake_monitor_set = lake_set.difference(monitor_set)


lake_code_table = (lake
                   >>select(X.DNR_ID_Site_Number,X.LAKE_NAME)
                     >>group_by(X.DNR_ID_Site_Number,X.LAKE_NAME)
                         >>summarise(Count = n(X.DNR_ID_Site_Number))
                            >>drop(X.Count)
                         )
lake_code_dict =  dict(zip(lake_code_table['DNR_ID_Site_Number'],lake_code_table["LAKE_NAME"]))

lat_long_distance_ID_dict = {(str(round(float(latitude),5)),str(round(float(longitude),5))):(distance,id_site) 
                     for latitude,longitude,distance,id_site in
                              zip(monitor.centroid_lat,monitor.centroid_long,monitor.Distance_Parcel_Lake_meters,monitor.Monit_MAP_CODE1)}
lat_long_tuple = set(lat_long_tuple for lat_long_tuple in lat_long_distance_ID_dict.keys())


def read_chunk(file,size):
    chunk_iter = pd.read_csv(file,chunksize=size,sep = "|",usecols =['centroid_lat','centroid_long'],dtype = {'centroid_lat':str,'centroid_long':str})
    return chunk_iter
filepaths = [
 './Data/MinneMUDAC/2015_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2009_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2007_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2011_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2005_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2013_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2014_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2008_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2010_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2006_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2012_metro_tax_parcels.txt',
 './Data/MinneMUDAC/2004_metro_tax_parcels.txt']
list_of_chunk_iter = [read_chunk(file,500) for file in filepaths]
list_of_chunk = []
for iterables in list_of_chunk_iter:
    for chunk in iterables:
        list_of_chunk.append(chunk)
parcel_lat_long_listofSet = [set(zip(X.centroid_lat,X.centroid_long)) for X in list_of_chunk]
parcel_lat_long_Set = set(lat_long for lat_long_set in parcel_lat_long_listofSet for lat_long in lat_long_set)

common_lat_long = lat_long_tuple.intersection(parcel_lat_long_Set)
lake_lat_long = (lake
             >> select(X.DNR_ID_Site_Number, X.latitude, X.longitude) \
             >> group_by(X.DNR_ID_Site_Number,X.latitude, X.longitude) \
             >> summarise(counts = n(X.DNR_ID_Site_Number)) \
             >> drop(X.counts))
lat_long_ID_tuple = {(str(round(float(latitude),5)),str(round(float(longitude),5)),id_site,distance )
                     for (latitude,longitude),(distance,id_site) in
                              lat_long_distance_ID_dict.items() if (latitude,longitude) in common_lat_long and id_site in common_id }

lat_long_id__lake_dict = {(lat,long):(id_site,lake_code_dict[id_site],distance) 
                    for lat,long,id_site,distance in lat_long_ID_tuple if (lat,long) in common_lat_long and id_site in common_id }

import os
import glob
import psycopg2
import pandas as pd
from queries import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
spark = SparkSession \
     .builder \
     .appName("Lake Dataset Project") \
     .config("spark.some.config.option", "some-value") \
     .getOrCreate()    
sc = spark.sparkContext


def process_lake_data(cur, filepath):
    """Read a lake file and
    insert data to lake table in database
    Args:
        cur (psycopg2.cursor): The psycopg2 cursor
        filepath (str): The location of the lake file
    """
    # open lake file
    lake_df = sc.textFile(filepath)
    header = lake_df.first()
    log_rows = lake_df.filter(lambda line: line != header)
    temp_var = log_rows.map(lambda k: k.split("\t"))
    df      =  temp_var.toDF(header.split("\t"))
    
    cur.execute(drop_lakes_table)
    cur.execute(create_lakes_table)
    for row in df.collect():
        record_to_insert = tuple(row.asDict().values())
        cur.execute(lake_insert_query, record_to_insert)
     
     



def process_data(cur, conn, filepath, func):
    """Read all files from the given location and
    execute the specified function
    Args:
        cur (psycopg2.cursor): The psycopg2 cursor
        conn (psycopg2.connection): The database connection
        filepath (str): The location of files to be processed
        func (function): The function to execute
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.txt'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
    print("inserted")




def main():
    
    conn = psycopg2.connect("dbname=mn_lakes user=kapil")
    cur = conn.cursor()
    process_data(cur, conn, filepath='Data/Lake data', func=process_lake_data)
    #process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()




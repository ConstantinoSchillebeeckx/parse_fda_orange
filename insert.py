#!/usr/bin/env python3

import pandas as pd
import os, re, sys
from sqlalchemy import create_engine

'''
Script will load all of the Drugs@FDA data into a postgres database of
the name defined by the first sys.argv:
python insert.py table_name

Assumes that data was downloaded and extracted into the directory `raw/` 
and that a postgres server is running on local host with write privileges 
for user running this script.
'''



def camel_case_to_underscore_lower(name):
    """
    Convert a camel-case name, e.g. someCamelCase into an underscore
    delimited, lower-case version, e.g. some_camel_case. Any all
    caps name, e.g. TE, will simply be lower-cased, e.g. te

    https://stackoverflow.com/a/7322356/1153897
    """

    if name.isupper():
        return name.lower()
    else:
        name = name.replace('ID','Id').replace('_','')
        return re.sub( '(?<!^)(?=[A-Z])', '_', name ).lower()


assert len(sys.argv) == 2, "You must provide a database table name"


# connect to DB
# assumes current user has read/write access
conn = create_engine('postgresql://localhost/' + sys.argv[1])


for file in os.listdir('raw'):
    
    # filename without extension
    name = camel_case_to_underscore_lower(os.path.splitext(file)[0])
    
    # read data
    df = pd.read_csv('raw/'+file, sep='~', encoding = "ISO-8859-1")

    # convert column names
    df.columns = [camel_case_to_underscore_lower(l) for l in df.columns]

    # manualy change 'Approved Prior to Jan 1, 1982' to 'Jan 1, 1900'
    if name == 'products':
        df.approval_date = df.approval_date.replace('Approved Prior to Jan 1, 1982','Jan 1, 1900')

    # convert to datetime
    for l in df.columns:
        if 'date' in l:
            df[l] = pd.to_datetime(df[l], infer_datetime_format=True)
    
    # insert data
    print("Loading data for %s" %name)
    df.to_sql(name, con=conn, if_exists='replace', index=False)


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import mysql.connector
import sys
from pathlib import Path
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()
config.read('db.ini')

db = {}
db['user'] = config['db']['user']
db['pw'] = config['db']['pw']
db['host'] = config['db']['host']
db['database'] = config['db']['database']

out_folder = Path('out')

def connect_sql_server(serverDict):
  return mysql.connector.connect(user=serverDict['user'], 
          password=serverDict['pw'],
          host=serverDict['host'],
          database=serverDict['database']
          )
  
# Select what database to use
local_db = connect_sql_server( db )
local_cursor = local_db.cursor()

pe = pd.read_sql_query("select *, weekofyear(SampleTime) as wnum from pulpeye where SampleTime > '2020-11-21 00:00:00' ", local_db)

# read data from excel sheet
dff = pd.read_excel('data.xlsx', sheet_name='FAR-csf')

# Get current time and arguments
now = datetime.now()
last_sample_time = pe.SampleTime.max()
now = last_sample_time

current_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Current Time =", current_time)
print ('Number of arguments: {} arguments'.format(len(sys.argv)))
print('Last sample {}'.format(pe.SampleTime.max()))

hours_back = 24   # default period to look back
duration = hours_back

if len(sys.argv) > 1:
  if sys.argv[1] == 'w':
    sys.argv[1] = 168
  if sys.argv[1] == 'm':
    sys.argv[1] = 672
  if sys.argv[1] == '2d':
    sys.argv[1] = 48    
  if sys.argv[1] == 'q':
    sys.argv[1] = 2016  
  hours_back = int(sys.argv[1])
  duration = hours_back
  
  # one letter code options

# Determine start and end times for data
start_time_dt = now - timedelta(hours = hours_back)
start_time = start_time_dt.strftime("%Y-%m-%d %H:%M:%S")
end_time = current_time

if len(sys.argv) > 2:
  hours_back = int(sys.argv[1])
  end_hours_back = hours_back - int(sys.argv[2])
  end_time_dt = now - timedelta(hours = end_hours_back)
  end_time = end_time_dt.strftime("%Y-%m-%d %H:%M:%S")
  duration = int(sys.argv[2])

# Filter data to period   hours back to start...  hours back to end
pe = pe[pe.SampleTime > start_time]
pe = pe[pe.SampleTime < end_time]

# data separated by sample point
pe_mc6 = pe[pe.PulpName == 'MC6']
pe_mc1 = pe[pe.PulpName == 'MC1']
pe_rej = pe[pe.PulpName == 'Ref_Rejects']
pe_l1 = pe[pe.PulpName == 'L1_Lat_Transfer']
pe_l3 = pe[pe.PulpName == 'L3_Lat_Transfer']
pe_l2 = pe[pe.PulpName == 'L2_Lat_Transfer']

sns.boxplot(x='Screen', y='feed', data=dff)

#pe_rej.to_csv('rej.csv')  
# plt.boxplot(df)
plt.show()

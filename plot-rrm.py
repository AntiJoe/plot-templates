import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from datetime import datetime, timedelta
import seaborn as sns
from scipy import stats

dff = pd.read_excel('data.xlsx', sheet_name='FAR-con')
print(dff) # print out datafile

dff = dff[dff.Trial != 'SD']

# Create plot figure and axis
fig = plt.figure('Screen Audit Feb 3')
ax = fig.add_subplot(1,1,1)
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
font['size'] = 12
barWidth = 0.15
fig.suptitle('Reject Rates by Mass vs Feed Consistency\nIndividual Screens and Combined Screenroom', fontdict=font)
c = ['blue', 'green', 'red', 'black'] # color for each line and scatter
m = ['o', '^', 'v', 'D']        # markers for each scatter set
w = [2,2,2,2]                   # weight for each line
ls = ['--', '--', '--', '-']    # line styles for each line
offset = [-barWidth, 0, barWidth]
trial= [3,3]
trialLegend = ['Trial 1 - 1.3%', 'Trial 2 - 1.55%', 'Trial 3 - 1.0%']
idx = 0
# create scatter for each Tag
for screenTag in ['FS', 'P', 'S', 'Combined']:
    df = dff[dff.Screen == screenTag]
    
    ax = sns.regplot(x=df.feed, y=df.RRm, ci=None, label=screenTag, color=c[idx], 
    marker=m[idx], line_kws={"lw":w[idx], "ls": ls[idx]})
    idx = idx + 1   # increment index used in marker, line style and width arrays

# get and print line parameters...  used manually in remote
slope, intercept, r_value, p_value, std_err = stats.linregress(df.feed, df.RRm) 
print('slope: {}, intercept: {}, r_squ: {}, p_value: {}, std_err: {}'.format(slope, intercept, r_value**2, p_value, std_err))

plt.legend()
plt.grid(True, ls=':')

plt.xlabel('Feed Consistency (%)', fontdict=font)
plt.ylabel('Reject Rate by Mass', fontdict=font)
xpad = 0.1
ypad = 5
plt.xlim(min(dff.feed) - xpad, max(dff.feed) + xpad)
plt.ylim(min(dff.RRm) - ypad, max(dff.RRm) + ypad)

outfile = 'FPS-rrm.png'
plt.savefig(outfile, dpi=600)   # save chart to file
plt.show()
plt.close()

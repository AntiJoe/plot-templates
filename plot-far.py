import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from datetime import datetime, timedelta
import seaborn as sns

# read data from excel sheet
dff = pd.read_excel('data.xlsx', sheet_name='FAR-csf')
print(dff)

# set default parameters for plots 
fig = plt.figure('Screen Audit Feb 3')
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
            }
font['size'] = 12

barWidth = 0.15                     # set bar width  0.15 = 15% of bar zone
offset = [0, barWidth, -barWidth]   # set offset for each Trial round
c = ['b', 'g', 'r']                 # bar colors for each Trial round
baralpha = 0.8

# loop through Tags in data...  generate one plot per Tag
for screenTag in ['FS', 'P', 'S', 'Combined']:
    df = dff[dff.Screen == screenTag]
    print(df)
    print(df.describe())

    fig.suptitle('{} Screen \nFreeness Streams vs Feed Consistency'.format(screenTag), fontdict=font)
    trial= [3,3]
    trialLegend = ['Trial 1 - 1.3%', 'Trial 2 - 1.55%', 'Trial 3 - 1.0%']

# iterate through each Trial to plot Trial data bars
    for i in [1,2,3]:
        trial = df[df.Trial == i]
        plt.bar(1 + offset[i -1], trial.feed, width=barWidth, bottom=0, alpha=baralpha, color=c[i-1], label=trialLegend[i-1])
        plt.bar(2 + offset[i -1], trial.accepts, width=barWidth, bottom=0, alpha=baralpha, color=c[i-1])
        plt.bar(3 + offset[i -1], trial.rejects, width=barWidth, bottom=0, alpha=baralpha, color=c[i-1])

    plt.legend()
    plt.grid(True, ls=':')
    plt.xticks([1,2,3], labels=['Feed', 'Accepts', 'Rejects'])
    plt.ylabel('Freeness (ml)', fontdict=font)
    outfile = '{}-csf-far.png'.format(screenTag) # save chart to file using Tag in file name
    plt.savefig(outfile, dpi=600)
    plt.show()
    plt.close()

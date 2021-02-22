import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import mysql.connector
import sys
from pathlib import Path
from datetime import datetime, timedelta

out_folder = Path('out')

# read data from excel sheet
dff = pd.read_excel('data.xlsx', sheet_name='FAR-csf')

sns.boxplot(x='Screen', y='feed', data=dff)

plt.show()

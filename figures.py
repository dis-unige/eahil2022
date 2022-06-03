# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:08:15 2022

@author: ciercor
"""
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

IARC_color = "#1E7FB8" #[(30, 127, 184)]
UNIGE_color = "#CF0063" #[(207, 00, 99)] 

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

#### 13

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "df_filtered.csv"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
def read_big_csv(file):
    df_chuncks = pd.read_csv(file, chunksize=10000, sep=",")  # the number of rows per chunk
    df_chunk_list = []
    for sub_df in df_chuncks:
        df_chunk_list.append(sub_df)
    del(file); del(sub_df); del(df_chuncks)
    # merge them together
    df_original = pd.concat(df_chunk_list,sort=False)
    del(df_chunk_list)
    return(df_original)

df1 = read_big_csv(file_IARC)
df2 = read_big_csv(file_UNIGE)

# filter remove noise
df1_filter = df1[df1["Years_difference"] <= 50]
df2_filter = df2[df2["Years_difference"] <= 50]

#boxplot
data = {'IARC': df1_filter["Years_difference"], 'UNIGE': df2_filter["Years_difference"]}

fig, ax = plt.subplots()
# Remove top and right border
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
# Remove y-axis tick marks

# Set the colors for each distribution
colors = [IARC_color, UNIGE_color]
colors_IARC = dict(color=colors[0])
colors_UNIGE = dict(color=colors[1])

# Set plot title
ax.set_title('Citations age distribution during the last 50 years')
ax.boxplot(data["IARC"], positions=[1], labels = [list(data.keys())[0]],
           boxprops=colors_IARC, 
           medianprops=colors_IARC, 
           whiskerprops=colors_IARC, 
           capprops=colors_IARC, 
           flierprops=dict(markeredgecolor=colors[0]))
           
ax.boxplot(data["UNIGE"], positions=[2], labels = [list(data.keys())[1]],
           boxprops=colors_UNIGE, 
           medianprops=colors_UNIGE, 
           whiskerprops=colors_UNIGE, 
           capprops=colors_UNIGE, 
           flierprops=dict(markeredgecolor=colors[1]))
plt.ylabel("Age")
plt.savefig(folder_IARC + '13 - Citations age distribution during the last 50 years.png', dpi = 150)
plt.show()
plt.close('all')

######################################################################################################
######################################################################################################

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "df_filtered.csv"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
def read_big_csv(file):
    df_chuncks = pd.read_csv(file, chunksize=10000, sep=",")  # the number of rows per chunk
    df_chunk_list = []
    for sub_df in df_chuncks:
        df_chunk_list.append(sub_df)
    del(file); del(sub_df); del(df_chuncks)
    # merge them together
    df_original = pd.concat(df_chunk_list,sort=False)
    del(df_chunk_list)
    return(df_original)

df1 = read_big_csv(file_IARC)
df2 = read_big_csv(file_UNIGE)

# filter remove noise
df1_filter = df1[df1["Years_difference"] <= 50]
df2_filter = df2[df2["Years_difference"] <= 50]

sns.set(style="white")
fig = sns.kdeplot(df1_filter['Years_difference'], shade=False, color=IARC_color)
fig = sns.kdeplot(df2_filter['Years_difference'], shade=False, color=UNIGE_color)
fig.legend(labels=['IARC','UNIGE'])
fig.set_title("Citatons age during the last 50 years")
fig.vlines(x=[15], ymin=0, ymax=0.105, color='red')

plt.xlabel("Age")
plt.savefig(folder_IARC + '13 - Citatons age during the last 50 years.png', dpi = 150)
plt.show()
plt.close("all")

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

#### 14_15

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "14_15.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1 = df1[df1["YD_mean"] <= 50]
df2 = df2[df2["YD_mean"] <= 50]

# change column names 
df1.columns = df1.columns.str.replace(' ','_')
df2.columns = df2.columns.str.replace(' ','_')

#boxplot
data = {'IARC': df1["YD_mean"], 'UNIGE': df2["YD_mean"]}

fig, ax = plt.subplots()
# Remove top and right border
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
# Remove y-axis tick marks

# Set the colors for each distribution
colors = [IARC_color, UNIGE_color]
colors_IARC = dict(color=colors[0])
colors_UNIGE = dict(color=colors[1])

# Set plot title
ax.set_title('Citations age distribution by publication during the last 50 years')
ax.boxplot(data["IARC"], positions=[1], labels = [list(data.keys())[0]],
           boxprops=colors_IARC, 
           medianprops=colors_IARC, 
           whiskerprops=colors_IARC, 
           capprops=colors_IARC, 
           flierprops=dict(markeredgecolor=colors[0]))
           
ax.boxplot(data["UNIGE"], positions=[2], labels = [list(data.keys())[1]],
           boxprops=colors_UNIGE, 
           medianprops=colors_UNIGE, 
           whiskerprops=colors_UNIGE, 
           capprops=colors_UNIGE, 
           flierprops=dict(markeredgecolor=colors[1]))
plt.xlabel("Age")
plt.savefig(folder_IARC + '14_15 - Citations age distribution by publication during the last 50 years.png', dpi = 150)
plt.show()
plt.close('all')

######################################################################################################
######################################################################################################

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "14_15.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1_filter = df1[df1["YD_mean"] <= 50]
df2_filter = df2[df2["YD_mean"] <= 50]

sns.set(style="white")
fig = sns.kdeplot(df1_filter['YD_mean'], shade=False, color=IARC_color)
fig = sns.kdeplot(df2_filter['YD_mean'], shade=False, color=UNIGE_color)
fig.legend(labels=['IARC','UNIGE'])
fig.set_title("Citations age by publication during the last 50 years")
fig.vlines(x=[15], ymin=0, ymax=0.14, color='red')

plt.xlabel("Age")
plt.savefig(folder_IARC + '14_15 - Citations age by publication during the last 50 years.png', dpi = 150)
plt.show()
plt.close("all")

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

#### 16

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "16.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC)
df2 = pd.read_excel(file_UNIGE)

labels = list(df1["Year_Published"])
IARC_means = list(df1["YD_mean"].round(1))
UNIGE_means = list(df2["YD_mean"].round(1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IARC_means, width, label='IARC', color=IARC_color)
rects2 = ax.bar(x + width/2, UNIGE_means, width, label='UNIGE', color=UNIGE_color)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Age')
ax.set_title('Citation average age during the las 20 years')
ax.set_xticks(x, labels, rotation=70)
ax.legend(fontsize = 7)

ax.bar_label(rects1, padding=1, fontsize = 4)
ax.bar_label(rects2, padding=1, fontsize = 4)

fig.tight_layout()
plt.savefig(folder_IARC + '16 - Citation average age during the las 20 years.png', dpi = 150)
plt.show()
plt.close("all")

#####

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "16.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC)
df2 = pd.read_excel(file_UNIGE)

labels = list(df1["Year_Published"])
IARC_means = list(df1["Ratio C/P"].round(1))
UNIGE_means = list(df2["Ratio C/P"].round(1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IARC_means, width, label='IARC', color=IARC_color)
rects2 = ax.bar(x + width/2, UNIGE_means, width, label='UNIGE', color=UNIGE_color)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Ratio C/P')
ax.set_title('Ratio of citation by publication during the las 20 years')
ax.set_xticks(x, labels, rotation=70)
ax.legend(fontsize = 6)

ax.bar_label(rects1, padding=1, fontsize = 4)
ax.bar_label(rects2, padding=1, fontsize = 4)

fig.tight_layout()
plt.savefig(folder_IARC + '16 - Ratio citation publication during the las 20 years.png', dpi = 150)
plt.show()
plt.close("all")

####

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "16.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC)
df2 = pd.read_excel(file_UNIGE)

labels = list(df1["Year_Published"])
IARC_means = list(df1["Publications"].round(1))
UNIGE_means = list(df2["Publications"].round(1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IARC_means, width, label='IARC', color=IARC_color)
rects2 = ax.bar(x + width/2, UNIGE_means, width, label='UNIGE', color=UNIGE_color)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Publications')
ax.set_title('Publications during the las 20 years')
ax.set_xticks(x, labels, rotation=70)
ax.legend(fontsize = 6)

ax.bar_label(rects1, padding=1, fontsize = 4)
ax.bar_label(rects2, padding=1, fontsize = 4)

fig.tight_layout()
plt.savefig(folder_IARC + '16 - Publications during the las 20 years.png', dpi = 150)
plt.show()
plt.close("all")

####

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "16.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC)
df2 = pd.read_excel(file_UNIGE)

labels = list(df1["Year_Published"])
IARC_means = list(df1["Citations"].round(1))
UNIGE_means = list(df2["Citations"].round(1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IARC_means, width, label='IARC', color=IARC_color)
rects2 = ax.bar(x + width/2, UNIGE_means, width, label='UNIGE', color=UNIGE_color)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Citations')
ax.set_title('Citations during the las 20 years')
ax.set_xticks(x, labels, rotation=70)
ax.legend(fontsize = 6)

ax.bar_label(rects1, padding=1, fontsize = 4)
ax.bar_label(rects2, padding=1, fontsize = 4)

fig.tight_layout()
plt.savefig(folder_IARC + '16 - Citations during the las 20 years.png', dpi = 150)
plt.show()
plt.close("all")

####

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "16.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC)
df2 = pd.read_excel(file_UNIGE)

labels = list(df1["Year_Published"])
IARC_means = list(df1["Journals"].round(1))
UNIGE_means = list(df2["Journals"].round(1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IARC_means, width, label='IARC', color=IARC_color)
rects2 = ax.bar(x + width/2, UNIGE_means, width, label='UNIGE', color=UNIGE_color)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Journals')
ax.set_title('Journals during the las 20 years')
ax.set_xticks(x, labels, rotation=70)
ax.legend(fontsize = 6)

ax.bar_label(rects1, padding=1, fontsize = 4)
ax.bar_label(rects2, padding=1, fontsize = 4)

fig.tight_layout()
plt.savefig(folder_IARC + '16 - Journals during the las 20 years.png', dpi = 150)
plt.show()
plt.close("all")

######################################################################################################
######################################################################################################

### 18

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "18.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1 = df1[df1["YD_mean"] <= 50]
df2 = df2[df2["YD_mean"] <= 50]

# change column names 
df1.columns = df1.columns.str.replace(' ','_')
df2.columns = df2.columns.str.replace(' ','_')

#boxplot
data = {'IARC': df1["YD_mean"], 'UNIGE': df2["YD_mean"]}

fig, ax = plt.subplots()
# Remove top and right border
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
# Remove y-axis tick marks

# Set the colors for each distribution
colors = [IARC_color, UNIGE_color]
colors_IARC = dict(color=colors[0])
colors_UNIGE = dict(color=colors[1])

# Set plot title
ax.set_title('Journal publications average age distribution during the last 50 years')
ax.boxplot(data["IARC"], positions=[1], labels = [list(data.keys())[0]],
            boxprops=colors_IARC, 
            medianprops=colors_IARC, 
            whiskerprops=colors_IARC, 
            capprops=colors_IARC, 
            flierprops=dict(markeredgecolor=colors[0]))
           
ax.boxplot(data["UNIGE"], positions=[2], labels = [list(data.keys())[1]],
            boxprops=colors_UNIGE, 
            medianprops=colors_UNIGE, 
            whiskerprops=colors_UNIGE, 
            capprops=colors_UNIGE, 
            flierprops=dict(markeredgecolor=colors[1]))
plt.savefig(folder_IARC + '18 - Journal publications average age distribution during the last 20 years.png', dpi = 150)
plt.show()
plt.close('all')

####

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "18.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1_filter = df1[df1["YD_mean"] <= 50]
df2_filter = df2[df2["YD_mean"] <= 50]

sns.set(style="white")
fig = sns.kdeplot(df1_filter['YD_mean'], shade=False, color=IARC_color)
fig = sns.kdeplot(df2_filter['YD_mean'], shade=False, color=UNIGE_color)
fig.legend(labels=['IARC','UNIGE'])
fig.set_title("Journal publications average age by publication during the last 50 years")
fig.vlines(x=[15], ymin=0, ymax=0.14, color='red')

plt.xlabel("Age")
plt.savefig(folder_IARC + '18 - Journals publications average age during the last 50 years.png', dpi = 150)
plt.show()
plt.close("all")

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

### 20

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "20.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# change column names 
df1.columns = df1.columns.str.replace(' ','_')
df2.columns = df2.columns.str.replace(' ','_')

#boxplot
data = {'IARC': df1["Percent"], 'UNIGE': df2["Percent"]}

fig, ax = plt.subplots()
# Remove top and right border
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
# Remove y-axis tick marks

# Set the colors for each distribution
colors = [IARC_color, UNIGE_color]
colors_IARC = dict(color=colors[0])
colors_UNIGE = dict(color=colors[1])

# Set plot title
ax.set_title('Journals publication percentage distribution during the last 20 years')
ax.boxplot(data["IARC"], positions=[1], labels = [list(data.keys())[0]],
           boxprops=colors_IARC, 
           medianprops=colors_IARC, 
           whiskerprops=colors_IARC, 
           capprops=colors_IARC, 
           flierprops=dict(markeredgecolor=colors[0]))
           
ax.boxplot(data["UNIGE"], positions=[2], labels = [list(data.keys())[1]],
           boxprops=colors_UNIGE, 
           medianprops=colors_UNIGE, 
           whiskerprops=colors_UNIGE, 
           capprops=colors_UNIGE, 
           flierprops=dict(markeredgecolor=colors[1]))
plt.ylabel("Percent")
plt.savefig(folder_IARC + '20 - Journals publication percentage distribution during the last 20 years.png', dpi = 150)
plt.show()
plt.close('all')

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

#### 21

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "21.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1 = df1[df1["YD_mean"] <= 50]
df2 = df2[df2["YD_mean"] <= 50]

# change column names 
df1.columns = df1.columns.str.replace(' ','_')
df2.columns = df2.columns.str.replace(' ','_')

#boxplot
data = {'IARC': df1["YD_mean"], 'UNIGE': df2["YD_mean"]}

fig, ax = plt.subplots()
# Remove top and right border
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
# Remove y-axis tick marks

# Set the colors for each distribution
colors = [IARC_color, UNIGE_color]
colors_IARC = dict(color=colors[0])
colors_UNIGE = dict(color=colors[1])

# Set plot title
ax.set_title('Journal citations average age distribution during the last 50 years')
ax.boxplot(data["IARC"], positions=[1], labels = [list(data.keys())[0]],
            boxprops=colors_IARC, 
            medianprops=colors_IARC, 
            whiskerprops=colors_IARC, 
            capprops=colors_IARC, 
            flierprops=dict(markeredgecolor=colors[0]))
           
ax.boxplot(data["UNIGE"], positions=[2], labels = [list(data.keys())[1]],
            boxprops=colors_UNIGE, 
            medianprops=colors_UNIGE, 
            whiskerprops=colors_UNIGE, 
            capprops=colors_UNIGE, 
            flierprops=dict(markeredgecolor=colors[1]))
plt.savefig(folder_IARC + '21 - Journal citations average age distribution during the last 50 years.png', dpi = 150)
plt.show()
plt.close('all')

####

# file name + directory
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name = "21.xlsx"
file_IARC = folder_IARC + file_name
file_UNIGE = folder_UNIGE + file_name

# read csv file in chuncks, its more efficient
df1 = pd.read_excel(file_IARC, index_col=(0))
df2 = pd.read_excel(file_UNIGE, index_col=(0))

# filter remove noise
df1_filter = df1[df1["YD_mean"] <= 50]
df2_filter = df2[df2["YD_mean"] <= 50]

sns.set(style="white")
fig = sns.kdeplot(df1_filter['YD_mean'], shade=False, color=IARC_color)
fig = sns.kdeplot(df2_filter['YD_mean'], shade=False, color=UNIGE_color)
fig.legend(labels=['IARC','UNIGE'])
fig.set_title("Journal citations average age by publication during the last 50 years")
fig.vlines(x=[15], ymin=0, ymax=0.09, color='red')

plt.xlabel("Age")
plt.savefig(folder_IARC + '21 - Journals citations average age during the last 50 years.png', dpi = 150)
plt.show()
plt.close("all")
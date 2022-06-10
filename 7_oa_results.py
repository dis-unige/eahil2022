#!/usr/bin/env python
# coding: utf-8

# # Open Access status for WoS DOIs : Results
# 
# Notebook used for the study presented at the EAHIL 2022 conference
# 
# * Title: Computational assistance in the analysis of cited references in biomedical literature: a case study from two institutions.
# 
# * Authors:
#  * Teresa Lee, Knowledge Manager, International Agency for Research on Cancer (IARC/WHO) leet@iarc.fr  
#  * Pablo Iriarte, IT Coordinator, Library of the University of Geneva Pablo.Iriarte@unige.ch 
#  * Floriane Muller, Librarian (Medical Library), Library of the University of Geneva Floriane.Muller@unige.ch  
#  * Ramon Cierco Jimenez, Doctoral Student, International Agency for Research on Cancer (IARC/WHO) CiercoR@students.iarc.fr  
# 
# 
# ### Prerequisites
# * DOIs from publications and citations
# * unpaywall data downloaded using the notebook "doi_unpaywall.ipynb" or queries made directly on unpaywall website
# * merge of DOIs and unpaywall data using the notebook "oa_status_merge.ipynb" 
# 

# In[1]:


import re
import os
import pandas as pd
import time
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
from scipy import stats


# In[2]:


# open DOIs data
dois = pd.read_csv('export_dois_oa_status.tsv', sep='\t', encoding='utf-8', header=0)
dois


# In[3]:


# open UNIGE data
unige_all = pd.read_csv('unige_all_oa_status_citations.csv', encoding='utf-8', header=0, sep='\t')
unige_all


# In[4]:


# open IARC data
iarc_all = pd.read_csv('iarc_all_oa_status_citations.csv', encoding='utf-8', header=0, sep='\t')
iarc_all


# # Questions to tackle
# 
# ## 25. Within the cited articles, what proportion exist in digital form (or at least have a DOI). Does it evolve with time?

# In[5]:


# df for publications
unige_publications = unige_all.drop_duplicates(subset='publication_wos_id')
iarc_publications = iarc_all.drop_duplicates(subset='publication_wos_id')
# df with and without DOIs
unige_publications_with_dois = unige_all.loc[unige_all['publication_doi'].notna()].drop_duplicates(subset='publication_wos_id')
unige_citations_with_dois = unige_all.loc[unige_all['citation_doi'].notna()]
iarc_publications_with_dois = iarc_all.loc[iarc_all['publication_doi'].notna()].drop_duplicates(subset='publication_wos_id')
iarc_citations_with_dois = iarc_all.loc[iarc_all['citation_doi'].notna()]


# In[6]:


# % of UNIGE publications with DOIs
unige_publications_n = unige_publications.shape[0]
unige_publications_dois_n = unige_publications_with_dois.shape[0]
unige_publications_dois_p = unige_publications_dois_n / unige_publications_n
print ('UNIGE publications : ' + str(unige_publications_n))
print ('UNIGE publications with DOIs  : ' + str(unige_publications_dois_n))
print ('UNIGE publications with DOIs  % : ' + str(unige_publications_dois_p))


# In[7]:


# % of IARC publications with DOIs
iarc_publications_n = iarc_publications.shape[0]
iarc_publications_dois_n = iarc_publications_with_dois.shape[0]
iarc_publications_dois_p = iarc_publications_dois_n / iarc_publications_n
print ('IARC publications : ' + str(iarc_publications_n))
print ('IARC publications with DOIs  : ' + str(iarc_publications_dois_n))
print ('IARC publications with DOIs  % : ' + str(iarc_publications_dois_p))


# In[8]:


# % of UNIGE citations with DOIs
unige_citations_n = unige_all.shape[0]
unige_citations_dois_n = unige_citations_with_dois.shape[0]
unige_citations_dois_p = unige_citations_dois_n / unige_citations_n
print ('UNIGE citations : ' + str(unige_citations_n))
print ('UNIGE citations with DOIS : ' + str(unige_citations_dois_n))
print ('UNIGE citations with DOIS % : ' + str(unige_citations_dois_p))


# In[9]:


# % of IARC citations with DOIs
iarc_citations_n = iarc_all.shape[0]
iarc_citations_dois_n = iarc_citations_with_dois.shape[0]
iarc_citations_dois_p = iarc_citations_dois_n / iarc_citations_n
print ('IARC citations : ' + str(iarc_citations_n))
print ('IARC citations with DOIS : ' + str(iarc_citations_dois_n))
print ('IARC citations with DOIS % : ' + str(iarc_citations_dois_p))


# In[10]:


# write  results on file
with open('25.txt', 'a') as f:
    f.write('25. Within the cited articles, what proportion exist in digital form (or at least have a DOI)\n')
    f.write('----------------------------------------\n\n')
    f.write('PUBLICATIONS:\n\n')
    f.write('UNIGE publications : ' + str(unige_publications_n) + '\n')
    f.write('UNIGE publications with DOIs  : ' + str(unige_publications_dois_n) + '\n')
    f.write('UNIGE publications with DOIs  % : ' + str(unige_publications_dois_p) + '\n')
    f.write('  \n')
    f.write('IARC publications : ' + str(iarc_publications_n) + '\n')
    f.write('IARC publications with DOIs  : ' + str(iarc_publications_dois_n) + '\n')
    f.write('IARC publications with DOIs  % : ' + str(iarc_publications_dois_p) + '\n')
    f.write('  \n')
    f.write('CITATIONS:\n\n')
    f.write('UNIGE citations : ' + str(unige_citations_n) + '\n')
    f.write('UNIGE citations with DOIS : ' + str(unige_citations_dois_n) + '\n')
    f.write('UNIGE citations with DOIS % : ' + str(unige_citations_dois_p) + '\n')
    f.write('  \n')
    f.write('IARC citations : ' + str(iarc_citations_n) + '\n')
    f.write('IARC citations with DOIS : ' + str(iarc_citations_dois_n) + '\n')
    f.write('IARC citations with DOIS % : ' + str(iarc_citations_dois_p) + '\n')


# In[11]:


IARC_color = "#1E7FB8" #[(30, 127, 184)]
UNIGE_color = "#CF0063" #[(207, 00, 99)] 


# In[12]:


# UNIGE publications with DOI by year
 
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/25_unige_publications_pie_chart.png'
labels = 'UNIGE publications\nwith DOI on WoS', 'UNIGE publications\nwithout DOI on WoS'
sizes = [unige_publications_dois_n,
         unige_publications_n - unige_publications_dois_n ]
explode = (0.1, 0.1)
colors = [UNIGE_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, dpi=200)
plt.show()


# In[13]:


# IARC publications with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/25_iarc_publications_pie_chart.png'
labels = 'IARC publications\nwith DOI on WoS', 'IARC publications\nwithout DOI on WoS'
sizes = [iarc_publications_dois_n,
         iarc_publications_n - iarc_publications_dois_n ]
explode = (0.1, 0.1)
colors = [IARC_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, dpi=200)
plt.show()


# In[14]:


# UNIGE citations with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/25_unige_citations_pie_chart.png'
labels = 'UNIGE citations\nwith DOI on WoS', 'UNIGE citations\nwithout DOI on WoS'
sizes = [unige_citations_dois_n,
         unige_citations_n - unige_citations_dois_n ]
explode = (0.1, 0.1)
colors = [UNIGE_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, dpi=200)
plt.show()


# In[15]:


# IARC citations with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/25_iarc_citations_pie_chart.png'
labels = 'IARC citations\nwith DOI on WoS', 'IARC citations\nwithout DOI on WoS'
sizes = [iarc_citations_dois_n,
         iarc_citations_n - iarc_citations_dois_n ]
explode = (0.1, 0.1)
colors = [IARC_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, dpi=200)
plt.show()


# In[16]:


# UNIGE publications with DOI by year
unige_publications_with_dois_by_year = unige_publications_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_doi_count').sort_values(by='publication_year')
unige_publications_counts = unige_publications['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_count').sort_values(by='publication_year')
# merge
unige_publications_with_dois_by_year = pd.merge(unige_publications_with_dois_by_year, unige_publications_counts, on='publication_year')
# add %
unige_publications_with_dois_by_year['publication_doi_percent'] = unige_publications_with_dois_by_year['publication_doi_count'] / unige_publications_with_dois_by_year['publications_count']
# remove errors
unige_publications_with_dois_by_year = unige_publications_with_dois_by_year.loc[(unige_publications_with_dois_by_year['publication_year'] > 2000) & (unige_publications_with_dois_by_year['publication_year'] < 2021)]
unige_publications_with_dois_by_year


# In[17]:


# UNIGE publications export 25 csv and excel
unige_publications_with_dois_by_year.to_csv('results/25_unige_publications_with_doi_by_year.csv', index=False, sep='\t', encoding='utf-8')
unige_publications_with_dois_by_year.to_excel('results/25_unige_publications_with_doi_by_year.xlsx', index=False)


# In[18]:


# IARC publications with DOI by year
iarc_publications_with_dois_by_year = iarc_publications_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_doi_count').sort_values(by='publication_year')
iarc_publications_counts = iarc_publications['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_count').sort_values(by='publication_year')
# merge
iarc_publications_with_dois_by_year = pd.merge(iarc_publications_with_dois_by_year, iarc_publications_counts, on='publication_year')
# add %
iarc_publications_with_dois_by_year['publication_doi_percent'] = iarc_publications_with_dois_by_year['publication_doi_count'] / iarc_publications_with_dois_by_year['publications_count']
iarc_publications_with_dois_by_year


# In[19]:


# IARC publications export 25 csv and excel
iarc_publications_with_dois_by_year.to_csv('results/25_iarc_publications_with_doi_by_year.csv', index=False, sep='\t', encoding='utf-8')
iarc_publications_with_dois_by_year.to_excel('results/25_iarc_publications_with_doi_by_year.xlsx', index=False)


# In[20]:


# UNIGE citations with DOI by year
unige_citations_with_dois_by_year = unige_citations_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citation_doi_count').sort_values(by='publication_year')
unige_citations_counts = unige_all['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_count').sort_values(by='publication_year')
# merge
unige_citations_with_dois_by_year = pd.merge(unige_citations_with_dois_by_year, unige_citations_counts, on='publication_year')
# add %
unige_citations_with_dois_by_year['citation_doi_percent'] = unige_citations_with_dois_by_year['citation_doi_count'] / unige_citations_with_dois_by_year['citations_count']
# remove errors
unige_citations_with_dois_by_year = unige_citations_with_dois_by_year.loc[(unige_citations_with_dois_by_year['publication_year'] > 2000) & (unige_citations_with_dois_by_year['publication_year'] < 2021)]
unige_citations_with_dois_by_year


# In[21]:


# UNIGE citations export 25 csv and excel
unige_citations_with_dois_by_year.to_csv('results/25_unige_citations_with_doi_by_year.csv', index=False, sep='\t', encoding='utf-8')
unige_citations_with_dois_by_year.to_excel('results/25_unige_citations_with_doi_by_year.xlsx', index=False)


# In[22]:


# IARC citations with DOI by year
iarc_citations_with_dois_by_year = iarc_citations_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citation_doi_count').sort_values(by='publication_year')
iarc_citations_counts = iarc_all['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_count').sort_values(by='publication_year')
# merge
iarc_citations_with_dois_by_year = pd.merge(iarc_citations_with_dois_by_year, iarc_citations_counts, on='publication_year')
# add %
iarc_citations_with_dois_by_year['citation_doi_percent'] = iarc_citations_with_dois_by_year['citation_doi_count'] / iarc_citations_with_dois_by_year['citations_count']
iarc_citations_with_dois_by_year


# In[23]:


# IARC citations export 25 csv and excel
iarc_citations_with_dois_by_year.to_csv('results/25_iarc_citations_with_doi_by_year.csv', index=False, sep='\t', encoding='utf-8')
iarc_citations_with_dois_by_year.to_excel('results/25_iarc_citations_with_doi_by_year.xlsx', index=False)


# In[24]:


# merge both tables for publications
publications_with_dois_by_year = iarc_publications_with_dois_by_year[['publication_year', 'publication_doi_percent']]
publications_with_dois_by_year = publications_with_dois_by_year.rename(columns={'publication_doi_percent' : 'IARC'})
publications_with_dois_by_year = publications_with_dois_by_year.merge(unige_publications_with_dois_by_year[['publication_year', 'publication_doi_percent']], on='publication_year')
publications_with_dois_by_year = publications_with_dois_by_year.rename(columns={'publication_doi_percent' : 'UNIGE'})
publications_with_dois_by_year = publications_with_dois_by_year.set_index('publication_year')
publications_with_dois_by_year


# In[25]:


# merge both tables for citations
citations_with_dois_by_year = iarc_citations_with_dois_by_year[['publication_year', 'citation_doi_percent']]
citations_with_dois_by_year = citations_with_dois_by_year.rename(columns={'citation_doi_percent' : 'IARC'})
citations_with_dois_by_year = citations_with_dois_by_year.merge(unige_citations_with_dois_by_year[['publication_year', 'citation_doi_percent']], on='publication_year')
citations_with_dois_by_year = citations_with_dois_by_year.rename(columns={'citation_doi_percent' : 'UNIGE'})
citations_with_dois_by_year = citations_with_dois_by_year.set_index('publication_year')
citations_with_dois_by_year


# In[26]:


# export 25 csv and excel
# publications
publications_with_dois_by_year.to_csv('results/25_iarc_unige_publications_with_doi_by_year.csv', index=True, sep='\t', encoding='utf-8')
publications_with_dois_by_year.to_excel('results/25_iarc_unige_publications_with_doi_by_year.xlsx', index=True)
# citations
citations_with_dois_by_year.to_csv('results/25_iarc_unige_citations_with_doi_by_year.csv', index=True, sep='\t', encoding='utf-8')
citations_with_dois_by_year.to_excel('results/25_iarc_unige_citations_with_doi_by_year.xlsx', index=True)


# In[27]:


# year counts for publications
myfileoutfig = 'figures/25_iarc_unige_publications_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = publications_with_dois_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5,xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of publications with DOIs', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[28]:


# year counts for citations
myfileoutfig = 'figures/25_iarc_unige_citations_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = citations_with_dois_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5, xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of citations with DOIs', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[29]:


# UNIGE plot year counts for publications
unige_publications_with_dois_by_year_fig = unige_publications_with_dois_by_year[['publication_year', 'publication_doi_percent']]
unige_publications_with_dois_by_year_fig = unige_publications_with_dois_by_year_fig.set_index('publication_year')
myfileoutfig = 'figures/25_unige_publications_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = unige_publications_with_dois_by_year_fig.plot.area(legend=False, rot=70, color=[UNIGE_color], xlim=[2001,2020], ylim=[0,1])
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_title('UNIGE - Percent of publications with DOIs', fontsize=40)
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[30]:


# IARC plot year counts for publications
iarc_publications_with_dois_by_year_fig = iarc_publications_with_dois_by_year[['publication_year', 'publication_doi_percent']]
iarc_publications_with_dois_by_year_fig = iarc_publications_with_dois_by_year_fig.set_index('publication_year')
myfileoutfig = 'figures/25_iarc_publications_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = iarc_publications_with_dois_by_year_fig.plot.area(legend=False, rot=70, color=[IARC_color], xlim=[2001,2020], ylim=[0,1])
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_title('IARC - Percent of publications with DOIs', fontsize=40)
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[31]:


# UNIGE plot year counts for citations
unige_citations_with_dois_by_year_fig = unige_citations_with_dois_by_year[['publication_year', 'citation_doi_percent']]
unige_citations_with_dois_by_year_fig = unige_citations_with_dois_by_year_fig.set_index('publication_year')
myfileoutfig = 'figures/25_unige_citations_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = unige_citations_with_dois_by_year_fig.plot.area(legend=False, rot=70, color=[UNIGE_color], xlim=[2001,2020], ylim=[0,1])
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_title('UNIGE - Percent of citations with DOIs', fontsize=40)
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[32]:


# IARC plot year counts for citations
iarc_citations_with_dois_by_year_fig = iarc_citations_with_dois_by_year[['publication_year', 'citation_doi_percent']]
iarc_citations_with_dois_by_year_fig = iarc_citations_with_dois_by_year_fig.set_index('publication_year')
myfileoutfig = 'figures/25_iarc_citations_with_doi_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = iarc_citations_with_dois_by_year_fig.plot.area(legend=False, rot=70, color=[IARC_color], xlim=[2001,2020], ylim=[0,1])
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_title('IARC - Percent of citations with DOIs', fontsize=40)
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# ## 26. Self citation?

# In[33]:


unige_all.columns


# In[34]:


# df for selfcitations
unige_publications_unige_citations = unige_all.loc[unige_all['publication_doi_is_unige_citation'].notna()].drop_duplicates(subset='publication_wos_id')
unige_citations_after_2000 = unige_all.loc[(unige_all['citation_doi'].notna()) & (unige_all['citation_year'] > 2000)]
unige_citations_after_2000_unige_publications = unige_all.loc[(unige_all['citation_doi_is_unige_publication'].notna()) & (unige_all['citation_year'] > 2000)]
iarc_publications_iarc_citations = iarc_all.loc[iarc_all['publication_doi_is_iarc_citation'].notna()].drop_duplicates(subset='publication_wos_id')
iarc_citations_after_2000 = iarc_all.loc[(iarc_all['citation_doi'].notna()) & (iarc_all['citation_year'] > 2000)]
iarc_citations_after_2000_iarc_publications = iarc_all.loc[(iarc_all['citation_doi_is_iarc_publication'].notna()) & (unige_all['citation_year'] > 2000)]


# In[35]:


# UNIGE publication DOIs that are also UNIGE citation DOIs
unige_publications_unige_citations_n = unige_all.loc[unige_all['publication_doi_is_unige_citation'].notna()]['publication_wos_id'].nunique()
unige_publications_unige_citations_p = unige_publications_unige_citations_n / unige_publications_dois_n
print ('UNIGE publications : ' +  str(unige_publications_n))
print ('UNIGE publications with DOIs : ' +  str(unige_publications_dois_n))
print ('UNIGE publications with DOIs cited by UNIGE during the corpus years : ' + str(unige_publications_unige_citations_n))
print ('UNIGE publications with DOIs cited by UNIGE during the corpus years  % : ' + str(unige_publications_unige_citations_p))


# In[36]:


# IARC publication DOIs that are also IARC citation DOIs
iarc_publications_iarc_citations_n = iarc_all.loc[iarc_all['publication_doi_is_iarc_citation'].notna()]['publication_wos_id'].nunique()
iarc_publications_iarc_citations_p = iarc_publications_iarc_citations_n / iarc_publications_dois_n
print ('IARC publications : ' +  str(iarc_publications_n))
print ('IARC publications with DOIs : ' +  str(iarc_publications_dois_n))
print ('IARC publications with DOIs cited by IARC during the corpus years : ' + str(iarc_publications_iarc_citations_n))
print ('IARC publications with DOIs cited by IARC during the corpus years  % : ' + str(iarc_publications_iarc_citations_p))


# In[37]:


# UNIGE citations DOIs published after 2000 that are also UNIGE publication DOIs
unige_citations_after_2000_n = unige_all.loc[(unige_all['citation_doi'].notna()) & (unige_all['citation_year'] > 2000)].shape[0]
unige_citations_after_2000_unige_publications_n = unige_all.loc[(unige_all['citation_doi_is_unige_publication'].notna()) & (unige_all['citation_year'] > 2000)].shape[0]
unige_citations_after_2000_unige_publications_p = unige_citations_after_2000_unige_publications_n / unige_citations_after_2000_n
print ('UNIGE citations : ' +  str(unige_citations_n))
print ('UNIGE citations with DOIs : ' +  str(unige_citations_dois_n))
print ('UNIGE citations with DOIs published after 2000 : ' +  str(unige_citations_after_2000_n))
print ('UNIGE citations with DOIs published after 2000 that are also UNIGE publication : ' + str(unige_citations_after_2000_unige_publications_n))
print ('UNIGE citations with DOIs published after 2000 that are also UNIGE publication  % : ' + str(unige_citations_after_2000_unige_publications_p))


# In[38]:


# IARC citations DOIs published after 2000 that are also IARC publication DOIs
iarc_citations_after_2000_n = iarc_all.loc[(iarc_all['citation_doi'].notna()) & (iarc_all['citation_year'] > 2000)].shape[0]
iarc_citations_after_2000_iarc_publications_n = iarc_all.loc[(iarc_all['citation_doi_is_iarc_publication'].notna()) & (iarc_all['citation_year'] > 2000)].shape[0]
iarc_citations_after_2000_iarc_publications_p = iarc_citations_after_2000_iarc_publications_n / iarc_citations_after_2000_n
print ('IARC citations : ' +  str(iarc_citations_n))
print ('IARC citations with DOIs : ' +  str(iarc_citations_dois_n))
print ('IARC citations with DOIs published after 2000 : ' +  str(iarc_citations_after_2000_n))
print ('IARC citations with DOIs published after 2000 that are also IARC publication : ' + str(iarc_citations_after_2000_iarc_publications_n))
print ('IARC citations with DOIs published after 2000 that are also IARC publication  % : ' + str(iarc_citations_after_2000_iarc_publications_p))


# In[39]:


# write  results on file
with open('26.txt', 'a') as f:
    f.write('26. Self citation?\n')
    f.write('----------------------------------------\n\n')
    f.write('PUBLICATIONS:\n\n')
    f.write('UNIGE publications : ' + str(unige_publications_n) + '\n')
    f.write('UNIGE publications with DOIs : ' +  str(unige_publications_dois_n) + '\n')
    f.write('UNIGE publications with DOIs cited by UNIGE during the corpus years : ' + str(unige_publications_unige_citations_n) + '\n')
    f.write('UNIGE publications with DOIs cited by UNIGE during the corpus years  % : ' + str(unige_publications_unige_citations_p) + '\n')
    f.write('  \n')
    f.write('IARC publications : ' + str(iarc_publications_n) + '\n')
    f.write('IARC publications with DOIs : ' +  str(iarc_publications_dois_n) + '\n')
    f.write('IARC publications with DOIs cited by IARC during the corpus years : ' + str(iarc_publications_iarc_citations_n) + '\n')
    f.write('IARC publications with DOIs cited by IARC during the corpus years  % : ' + str(iarc_publications_iarc_citations_p) + '\n')
    f.write('  \n')
    f.write('CITATIONS:\n\n')
    f.write('UNIGE citations : ' + str(unige_citations_n) + '\n')
    f.write('UNIGE citations with DOIs : ' + str(unige_citations_dois_n) + '\n')
    f.write('UNIGE citations with DOIs published after 2000 : ' +  str(unige_citations_after_2000_n) + '\n')
    f.write('UNIGE citations with DOIs published after 2000 that are also UNIGE publication : ' + str(unige_citations_after_2000_unige_publications_n) + '\n')
    f.write('UNIGE citations with DOIs published after 2000 that are also UNIGE publication  % : ' + str(unige_citations_after_2000_unige_publications_p) + '\n')
    f.write('  \n')
    f.write('IARC citations : ' + str(iarc_citations_n) + '\n')
    f.write('IARC citations with DOIs : ' + str(iarc_citations_dois_n) + '\n')
    f.write('IARC citations with DOIs published after 2000 : ' +  str(iarc_citations_after_2000_n) + '\n')
    f.write('IARC citations with DOIs published after 2000 that are also IARC publication : ' + str(iarc_citations_after_2000_iarc_publications_n) + '\n')
    f.write('IARC citations with DOIs published after 2000 that are also IARC publication  % : ' + str(iarc_citations_after_2000_iarc_publications_p) + '\n')


# In[40]:


# UNIGE publications with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/26_unige_publications_pie_chart.png'
labels = 'UNIGE publications\nwith DOIs cited by UNIGE', 'UNIGE publications\nwith DOIs not cited by UNIGE'
sizes = [unige_publications_unige_citations_n,
         unige_publications_dois_n - unige_publications_unige_citations_n ]
explode = (0.1, 0.1)
colors = [UNIGE_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, dpi=200)
plt.show()


# In[41]:


# IARC publications with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/26_iarc_publications_pie_chart.png'
labels = 'IARC publications\nwith DOIs cited by IARC', 'IARC publications\nwith DOIs not cited by IARC'
sizes = [iarc_publications_iarc_citations_n,
         iarc_publications_dois_n - iarc_publications_iarc_citations_n ]
explode = (0.1, 0.1)
colors = [IARC_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[42]:


# UNIGE citations with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/26_unige_citations_pie_chart.png'
labels = 'UNIGE citations\nwith DOIs published after 2000\nthat are also UNIGE publications', 'UNIGE citations\nwith DOIs published after 2000\nthat aren\'t UNIGE publications'
sizes = [unige_citations_after_2000_unige_publications_n,
         unige_citations_after_2000_n - unige_citations_after_2000_unige_publications_n ]
explode = (0.1, 0.1)
colors = [UNIGE_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[43]:


# IARC citations with DOI by year
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/26_iarc_citations_pie_chart.png'
labels = 'IARC citations\nwith DOIs published after 2000\nthat are also IARC publications', 'IARC citations\nwith DOIs published after 2000\nthat aren\'t IARC publications :'
sizes = [iarc_citations_after_2000_iarc_publications_n,
         iarc_citations_after_2000_n - iarc_citations_after_2000_iarc_publications_n ]
explode = (0.1, 0.1)
colors = [IARC_color, 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(10, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# ## 26. Self citations evolve with time? 

# In[44]:


# UNIGE publications with DOI and cited by UNIGE by year
unige_publications_with_dois_cited_by_unige_by_year = unige_publications_unige_citations['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_self_cited_count').sort_values(by='publication_year')
unige_publications_with_dois_counts = unige_publications_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_with_doi_count').sort_values(by='publication_year')
# merge
unige_publications_with_dois_cited_by_unige_by_year = pd.merge(unige_publications_with_dois_cited_by_unige_by_year, unige_publications_with_dois_counts, on='publication_year')
# add %
unige_publications_with_dois_cited_by_unige_by_year['publication_self_cited_percent'] = unige_publications_with_dois_cited_by_unige_by_year['publication_self_cited_count'] / unige_publications_with_dois_cited_by_unige_by_year['publications_with_doi_count']
# remove errors
unige_publications_with_dois_cited_by_unige_by_year = unige_publications_with_dois_cited_by_unige_by_year.loc[(unige_publications_with_dois_cited_by_unige_by_year['publication_year'] > 2000) & (unige_publications_with_dois_cited_by_unige_by_year['publication_year'] < 2021)]
unige_publications_with_dois_cited_by_unige_by_year


# In[45]:


# UNIGE publications export 26 csv and excel
unige_publications_with_dois_cited_by_unige_by_year.to_csv('results/26_unige_publications_with_doi_self_cited_by_year.csv', index=False, sep='\t', encoding='utf-8')
unige_publications_with_dois_cited_by_unige_by_year.to_excel('results/26_unige_publications_with_doi_self_cited_by_year.xlsx', index=False)


# In[46]:


# IARC publications with DOI and cited by IARC by year
iarc_publications_with_dois_cited_by_iarc_by_year = iarc_publications_iarc_citations['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_self_cited_count').sort_values(by='publication_year')
iarc_publications_with_dois_counts = iarc_publications_with_dois['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_with_doi_count').sort_values(by='publication_year')
# merge
iarc_publications_with_dois_cited_by_iarc_by_year = pd.merge(iarc_publications_with_dois_cited_by_iarc_by_year, iarc_publications_with_dois_counts, on='publication_year')
# add %
iarc_publications_with_dois_cited_by_iarc_by_year['publication_self_cited_percent'] = iarc_publications_with_dois_cited_by_iarc_by_year['publication_self_cited_count'] / iarc_publications_with_dois_cited_by_iarc_by_year['publications_with_doi_count']
# remove errors
iarc_publications_with_dois_cited_by_iarc_by_year = iarc_publications_with_dois_cited_by_iarc_by_year.loc[(iarc_publications_with_dois_cited_by_iarc_by_year['publication_year'] > 2000) & (iarc_publications_with_dois_cited_by_iarc_by_year['publication_year'] < 2021)]
iarc_publications_with_dois_cited_by_iarc_by_year


# In[47]:


# IARC publications export 26 csv and excel
iarc_publications_with_dois_cited_by_iarc_by_year.to_csv('results/26_iarc_publications_with_doi_self_cited_by_year.csv', index=False, sep='\t', encoding='utf-8')
iarc_publications_with_dois_cited_by_iarc_by_year.to_excel('results/26_iarc_publications_with_doi_self_cited_by_year.xlsx', index=False)


# In[48]:


# UNIGE citations with DOI that are also UNIGE publication by year of primary publication
unige_citations_after_2000_unige_publications_by_year = unige_citations_after_2000_unige_publications['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='self_citation_doi_count').sort_values(by='publication_year')
unige_citations_after_2000_counts = unige_citations_after_2000['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_after_2000_count').sort_values(by='publication_year')
# merge
unige_citations_after_2000_unige_publications_by_year = pd.merge(unige_citations_after_2000_unige_publications_by_year, unige_citations_after_2000_counts, on='publication_year')
# add %
unige_citations_after_2000_unige_publications_by_year['self_citation_doi_percent'] = unige_citations_after_2000_unige_publications_by_year['self_citation_doi_count'] / unige_citations_after_2000_unige_publications_by_year['citations_after_2000_count']
# remove errors
unige_citations_after_2000_unige_publications_by_year = unige_citations_after_2000_unige_publications_by_year.loc[(unige_citations_after_2000_unige_publications_by_year['publication_year'] > 2000) & (unige_citations_after_2000_unige_publications_by_year['publication_year'] < 2021)]
unige_citations_after_2000_unige_publications_by_year


# In[49]:


# UNIGE self citations export 25 csv and excel
unige_citations_after_2000_unige_publications_by_year.to_csv('results/26_unige_citations_with_doi_and_unige_publication_by_year.csv', index=False, sep='\t', encoding='utf-8')
unige_citations_after_2000_unige_publications_by_year.to_excel('results/26_unige_citations_with_doi_and_unige_publication_by_year.xlsx', index=False)


# In[50]:


# IARC citations with DOI that are also IARC publication by year of primary publication
iarc_citations_after_2000_iarc_publications_by_year = iarc_citations_after_2000_iarc_publications['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='self_citation_doi_count').sort_values(by='publication_year')
iarc_citations_after_2000_counts = iarc_citations_after_2000['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_after_2000_count').sort_values(by='publication_year')
# merge
iarc_citations_after_2000_iarc_publications_by_year = pd.merge(iarc_citations_after_2000_iarc_publications_by_year, iarc_citations_after_2000_counts, on='publication_year')
# add %
iarc_citations_after_2000_iarc_publications_by_year['self_citation_doi_percent'] = iarc_citations_after_2000_iarc_publications_by_year['self_citation_doi_count'] / iarc_citations_after_2000_iarc_publications_by_year['citations_after_2000_count']
# remove errors
iarc_citations_after_2000_iarc_publications_by_year = iarc_citations_after_2000_iarc_publications_by_year.loc[(iarc_citations_after_2000_iarc_publications_by_year['publication_year'] > 2000) & (iarc_citations_after_2000_iarc_publications_by_year['publication_year'] < 2021)]
iarc_citations_after_2000_iarc_publications_by_year


# In[51]:


# IARC self citations export 26 csv and excel
iarc_citations_after_2000_iarc_publications_by_year.to_csv('results/26_iarc_citations_with_doi_and_unige_publication_by_year.csv', index=False, sep='\t', encoding='utf-8')
iarc_citations_after_2000_iarc_publications_by_year.to_excel('results/26_iarc_citations_with_doi_and_unige_publication_by_year.xlsx', index=False)


# In[52]:


# merge both tables for publications
publications_self_citations_with_dois_by_year = iarc_publications_with_dois_cited_by_iarc_by_year[['publication_year', 'publication_self_cited_percent']]
publications_self_citations_with_dois_by_year = publications_self_citations_with_dois_by_year.rename(columns={'publication_self_cited_percent' : 'IARC'})
publications_self_citations_with_dois_by_year = publications_self_citations_with_dois_by_year.merge(unige_publications_with_dois_cited_by_unige_by_year[['publication_year', 'publication_self_cited_percent']], on='publication_year')
publications_self_citations_with_dois_by_year = publications_self_citations_with_dois_by_year.rename(columns={'publication_self_cited_percent' : 'UNIGE'})
publications_self_citations_with_dois_by_year = publications_self_citations_with_dois_by_year.set_index('publication_year')
publications_self_citations_with_dois_by_year


# In[53]:


# merge both tables for citations
self_citations_with_dois_by_year = iarc_citations_after_2000_iarc_publications_by_year[['publication_year', 'self_citation_doi_percent']]
self_citations_with_dois_by_year = self_citations_with_dois_by_year.rename(columns={'self_citation_doi_percent' : 'IARC'})
self_citations_with_dois_by_year = self_citations_with_dois_by_year.merge(unige_citations_after_2000_unige_publications_by_year[['publication_year', 'self_citation_doi_percent']], on='publication_year')
self_citations_with_dois_by_year = self_citations_with_dois_by_year.rename(columns={'self_citation_doi_percent' : 'UNIGE'})
self_citations_with_dois_by_year = self_citations_with_dois_by_year.set_index('publication_year')
self_citations_with_dois_by_year


# In[54]:


# export 26 csv and excel
# publications
publications_self_citations_with_dois_by_year.to_csv('results/26_iarc_unige_publications_with_doi_self_cited_by_year.csv', index=True, sep='\t', encoding='utf-8')
publications_self_citations_with_dois_by_year.to_excel('results/26_iarc_unige_publications_with_doi_self_cited_by_year.xlsx', index=True)
# citations
self_citations_with_dois_by_year.to_csv('results/26_iarc_unige_citations_with_doi_and_unige_publication_by_year.csv', index=True, sep='\t', encoding='utf-8')
self_citations_with_dois_by_year.to_excel('results/26_iarc_unige_citations_with_doi_and_unige_publication_by_year.xlsx', index=True)


# In[55]:


# year counts for publications
myfileoutfig = 'figures/26_iarc_unige_publications_with_doi_self_cited_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = publications_self_citations_with_dois_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5,xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of publications with DOIs self cited', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[56]:


# year counts for citations
myfileoutfig = 'figures/26_iarc_unige_citations_with_doi_and_unige_publication_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = self_citations_with_dois_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5, xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of citations with DOIs published after 2000 that are also publications', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# ## 27. Within the cited articles, what proportion are OA?

# In[57]:


unige_all.columns


# In[58]:


# OA of publications
oas = ['gold', 'hybrid', 'bronze', 'green']
unige_publications_oa = unige_all.loc[unige_all['publication_doi_oa_status'].isin(oas)]
unige_publications_not_oa = unige_all.loc[unige_all['publication_doi_oa_status'] == 'closed']
unige_publications_oa_unknown = unige_all.loc[unige_all['publication_doi_oa_status'].isna() & unige_all['publication_doi'].notna()]
unige_publications_without_doi_and_citation_with_oa_status  = unige_all.loc[unige_all['publication_doi'].isna() & unige_all['citation_doi_oa_status'].notna()]
unige_publications_oa


# In[59]:


# OA of publications
oas = ['gold', 'hybrid', 'bronze', 'green']
iarc_publications_oa = iarc_all.loc[iarc_all['publication_doi_oa_status'].isin(oas)]
iarc_publications_not_oa = iarc_all.loc[iarc_all['publication_doi_oa_status'] == 'closed']
iarc_publications_oa_unknown = iarc_all.loc[iarc_all['publication_doi_oa_status'].isna() & iarc_all['publication_doi'].notna()]
iarc_publications_without_doi_and_citation_with_oa_status  = iarc_all.loc[iarc_all['publication_doi'].isna() & iarc_all['citation_doi_oa_status'].notna()]
iarc_publications_oa


# In[60]:


unige_publications_oa.drop_duplicates(subset='publication_wos_id').publication_doi_oa_status.value_counts()


# In[61]:


unige_publications_not_oa.drop_duplicates(subset='publication_wos_id').publication_doi_oa_status.value_counts()


# In[62]:


iarc_publications_oa.drop_duplicates(subset='publication_wos_id').publication_doi_oa_status.value_counts()


# In[63]:


iarc_publications_not_oa.drop_duplicates(subset='publication_wos_id').publication_doi_oa_status.value_counts()


# In[64]:


# UNIGE publications OA
unige_publications_oa_n = unige_publications_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_oa_p = unige_publications_oa_n / unige_publications_dois_n
print ('UNIGE publications with DOIs : ' + str(unige_publications_dois_n))
print ('UNIGE publications with DOIs that are OA : ' + str(unige_publications_oa_n))
print ('UNIGE publications with DOIs that are OA  % : ' + str(unige_publications_oa_p))
unige_publications_not_oa_n = unige_publications_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_not_oa_p = unige_publications_not_oa_n / unige_publications_dois_n
print ('UNIGE publications with DOIs that are not OA : ' + str(unige_publications_not_oa_n))
print ('UNIGE publications with DOIs that are not OA  % : ' + str(unige_publications_not_oa_p))
unige_publications_oa_unknown_n = unige_publications_oa_unknown.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_oa_unknown_p = unige_publications_oa_unknown_n / unige_publications_dois_n
print ('UNIGE publications with DOIs but OA unknown : ' + str(unige_publications_oa_unknown_n))
print ('UNIGE publications with DOIs but OA unknown % : ' + str(unige_publications_oa_unknown_p))


# In[65]:


unige_publications_oa_n + unige_publications_not_oa_n + unige_publications_oa_unknown_n


# In[66]:


# IARC publications OA
iarc_publications_oa_n = iarc_publications_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_oa_p = iarc_publications_oa_n / iarc_publications_dois_n
print ('IARC publications with DOIs : ' + str(iarc_publications_dois_n))
print ('IARC publications with DOIs that are OA : ' + str(iarc_publications_oa_n))
print ('IARC publications with DOIs that are OA  % : ' + str(iarc_publications_oa_p))
iarc_publications_not_oa_n = iarc_publications_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_not_oa_p = iarc_publications_not_oa_n / iarc_publications_dois_n
print ('IARC publications with DOIs that are not OA : ' + str(iarc_publications_not_oa_n))
print ('IARC publications with DOIs that are not OA  % : ' + str(iarc_publications_not_oa_p))
iarc_publications_oa_unknown_n = iarc_publications_oa_unknown.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_oa_unknown_p = iarc_publications_oa_unknown_n / iarc_publications_dois_n
print ('IARC publications with DOIs but OA unknown : ' + str(iarc_publications_oa_unknown_n))
print ('IARC publications with DOIs but OA unknown % : ' + str(iarc_publications_oa_unknown_p))


# In[67]:


iarc_publications_oa_n + iarc_publications_not_oa_n + iarc_publications_oa_unknown_n


# In[68]:


# write  results on file
with open('27_oa_publications.txt', 'a') as f:
    f.write('27. Within the publications, what proportion are OA?\n')
    f.write('----------------------------------------\n\n')
    f.write('  \n')
    f.write('UNIGE publications with DOIs : ' + str(unige_publications_dois_n) + '\n')
    f.write('UNIGE publications with DOIs that are OA : ' + str(unige_publications_oa_n) + '\n')
    f.write('UNIGE publications with DOIs that are OA  % : ' + str(unige_publications_oa_p) + '\n')
    f.write('UNIGE publications with DOIs that are not OA : ' + str(unige_publications_not_oa_n) + '\n')
    f.write('UNIGE publications with DOIs that are not OA  % : ' + str(unige_publications_not_oa_p) + '\n')
    f.write('UNIGE publications with DOIs but OA unknown : ' + str(unige_publications_oa_unknown_n) + '\n')
    f.write('UNIGE publications with DOIs but OA unknown % : ' + str(unige_publications_oa_unknown_p) + '\n')
    f.write('  \n')
    f.write('IARC publications with DOIs : ' + str(iarc_publications_dois_n) + '\n')
    f.write('IARC publications with DOIs that are OA : ' + str(iarc_publications_oa_n) + '\n')
    f.write('IARC publications with DOIs that are OA  % : ' + str(iarc_publications_oa_p) + '\n')
    f.write('IARC publications with DOIs that are not OA : ' + str(iarc_publications_not_oa_n) + '\n')
    f.write('IARC publications with DOIs that are not OA  % : ' + str(iarc_publications_not_oa_p) + '\n')
    f.write('IARC publications with DOIs but OA unknown : ' + str(iarc_publications_oa_unknown_n) + '\n')
    f.write('IARC publications with DOIs but OA unknown % : ' + str(iarc_publications_oa_unknown_p) + '\n')


# In[69]:


# UNIGE publications OA
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_unige_publications_oa_pie_chart.png'
labels = 'UNIGE publications\nwith DOIs and OA', 'UNIGE publications\nwith DOIs and not OA', 'UNIGE publications\nwith DOIs but OA unknown'
sizes = [unige_publications_oa_n,
         unige_publications_not_oa_n,
         unige_publications_oa_unknown_n]
explode = (0.1, 0.1, 0.1)
colors = [UNIGE_color, 'black', 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', pctdistance=1.2, labeldistance=1.4,
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[70]:


# IARC publications OA
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_iarc_publications_oa_pie_chart.png'
labels = 'IARC publications\nwith DOIs and OA', 'IARC publications\nwith DOIs and not OA', 'IARC publications\nwith DOIs but OA unknown'
sizes = [iarc_publications_oa_n,
         iarc_publications_not_oa_n,
         iarc_publications_oa_unknown_n]
explode = (0.1, 0.1, 0.1)
colors = [IARC_color, 'black', 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', pctdistance=1.2, labeldistance=1.4,
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[71]:


# citations
unige_citations_oa = unige_all.loc[unige_all['citation_doi_oa_status'].isin(oas)]
unige_citations_not_oa = unige_all.loc[unige_all['citation_doi_oa_status'] == 'closed']
unige_citations_oa_unknown = unige_all.loc[unige_all['citation_doi_oa_status'].isna() & unige_all['citation_doi'].notna()]
iarc_citations_oa = iarc_all.loc[iarc_all['citation_doi_oa_status'].isin(oas)]
iarc_citations_not_oa = iarc_all.loc[iarc_all['citation_doi_oa_status'] == 'closed']
iarc_citations_oa_unknown = iarc_all.loc[iarc_all['citation_doi_oa_status'].isna() & iarc_all['citation_doi'].notna()]


# In[72]:


unige_citations_oa['citation_doi_oa_status'].value_counts()


# In[73]:


unige_citations_not_oa['citation_doi_oa_status'].value_counts()


# In[74]:


iarc_citations_oa['citation_doi_oa_status'].value_counts()


# In[75]:


iarc_citations_not_oa['citation_doi_oa_status'].value_counts()


# In[76]:


# UNIGE citations OA
unige_citations_oa_n = unige_citations_oa.shape[0]
unige_citations_oa_p = unige_citations_oa_n / unige_citations_dois_n
print ('UNIGE citations with DOIs : ' + str(unige_citations_dois_n))
print ('UNIGE citations with DOIs that are OA : ' + str(unige_citations_oa_n))
print ('UNIGE citations with DOIs that are OA  % : ' + str(unige_citations_oa_p))
unige_citations_not_oa_n = unige_citations_not_oa.shape[0]
unige_citations_not_oa_p = unige_citations_not_oa_n / unige_citations_dois_n
print ('UNIGE citations with DOIs that are not OA : ' + str(unige_citations_not_oa_n))
print ('UNIGE citations with DOIs that are not OA  % : ' + str(unige_citations_not_oa_p))
unige_citations_oa_unknown_n = unige_citations_oa_unknown.shape[0]
unige_citations_oa_unknown_p = unige_citations_oa_unknown_n / unige_citations_dois_n
print ('UNIGE citations with DOIs but OA unknown : ' + str(unige_citations_oa_unknown_n))
print ('UNIGE citations with DOIs but OA unknown % : ' + str(unige_citations_oa_unknown_p))


# In[77]:


# IARC citations OA
iarc_citations_oa_n = iarc_citations_oa.shape[0]
iarc_citations_oa_p = iarc_citations_oa_n / iarc_citations_dois_n
print ('IARC citations with DOIs : ' + str(iarc_citations_dois_n))
print ('IARC citations with DOIs that are OA : ' + str(iarc_citations_oa_n))
print ('IARC citations with DOIs that are OA  % : ' + str(iarc_citations_oa_p))
iarc_citations_not_oa_n = iarc_citations_not_oa.shape[0]
iarc_citations_not_oa_p = iarc_citations_not_oa_n / iarc_citations_dois_n
print ('IARC citations with DOIs that are not OA : ' + str(iarc_citations_not_oa_n))
print ('IARC citations with DOIs that are not OA  % : ' + str(iarc_citations_not_oa_p))
iarc_citations_oa_unknown_n = iarc_citations_oa_unknown.shape[0]
iarc_citations_oa_unknown_p = iarc_citations_oa_unknown_n / iarc_citations_dois_n
print ('IARC citations with DOIs but OA unknown : ' + str(iarc_citations_oa_unknown_n))
print ('IARC citations with DOIs but OA unknown % : ' + str(iarc_citations_oa_unknown_p))


# In[78]:


# write  results on file
with open('27_oa_citations.txt', 'a') as f:
    f.write('27. Within the cited articles, what proportion are OA?\n')
    f.write('----------------------------------------\n\n')
    f.write('  \n')
    f.write('UNIGE citations with DOIs : ' + str(unige_citations_dois_n) + '\n')
    f.write('UNIGE citations with DOIs that are OA : ' + str(unige_citations_oa_n) + '\n')
    f.write('UNIGE citations with DOIs that are OA  % : ' + str(unige_citations_oa_p) + '\n')
    f.write('UNIGE citations with DOIs that are not OA : ' + str(unige_citations_not_oa_n) + '\n')
    f.write('UNIGE citations with DOIs that are not OA  % : ' + str(unige_citations_not_oa_p) + '\n')
    f.write('UNIGE citations with DOIs but OA unknown : ' + str(unige_citations_oa_unknown_n) + '\n')
    f.write('UNIGE citations with DOIs but OA unknown % : ' + str(unige_citations_oa_unknown_p) + '\n')
    f.write('  \n')
    f.write('IARC citations with DOIs : ' + str(iarc_citations_dois_n) + '\n')
    f.write('IARC citations with DOIs that are OA : ' + str(iarc_citations_oa_n) + '\n')
    f.write('IARC citations with DOIs that are OA  % : ' + str(iarc_citations_oa_p) + '\n')
    f.write('IARC citations with DOIs that are not OA : ' + str(iarc_citations_not_oa_n) + '\n')
    f.write('IARC citations with DOIs that are not OA  % : ' + str(iarc_citations_not_oa_p) + '\n')
    f.write('IARC citations with DOIs but OA unknown : ' + str(iarc_citations_oa_unknown_n) + '\n')
    f.write('IARC citations with DOIs but OA unknown % : ' + str(iarc_citations_oa_unknown_p) + '\n')


# In[79]:


# UNIGE citations OA
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_unige_citations_oa_pie_chart.png'
labels = 'UNIGE citations\nwith DOIs and OA', 'UNIGE citations\nwith DOIs and not OA', 'UNIGE citations\nwith DOIs but OA unknown'
sizes = [unige_citations_oa_n,
         unige_citations_not_oa_n,
         unige_citations_oa_unknown_n]
explode = (0.1, 0.1, 0.1)
colors = [UNIGE_color, 'black', 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', pctdistance=1.2, labeldistance=1.4,
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[80]:


# IARC citations OA
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_iarc_citations_oa_pie_chart.png'
labels = 'IARC citations\nwith DOIs and OA', 'IARC citations\nwith DOIs and not OA', 'IARC citations\nwith DOIs but OA unknown'
sizes = [iarc_citations_oa_n,
         iarc_citations_not_oa_n,
         iarc_citations_oa_unknown_n]
explode = (0.1, 0.1, 0.1)
colors = [IARC_color, 'black', 'gray']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', pctdistance=1.2, labeldistance=1.4,
        shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[202]:


# IARC publications OA Roads
row_iarc_publications_oa_unknown = {'OA Color' : 'unknown', 'counts' : iarc_publications_oa_unknown_n}
row_iarc_publications_not_oa = {'OA Color' : 'closed', 'counts' : iarc_publications_not_oa_n}
iarc_publications_oa_roads = iarc_publications_oa.drop_duplicates(subset='publication_wos_id')['publication_doi_oa_status'].value_counts().rename_axis('OA Color').to_frame('counts')
iarc_publications_oa_roads = iarc_publications_oa_roads.reset_index()
iarc_publications_oa_roads = iarc_publications_oa_roads.append(row_iarc_publications_oa_unknown, ignore_index=True)
iarc_publications_oa_roads = iarc_publications_oa_roads.append(row_iarc_publications_not_oa, ignore_index=True)
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'gold', 'position'] = 1
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'hybrid', 'position'] = 2
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'bronze', 'position'] = 3
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'green', 'position'] = 4
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'closed', 'position'] = 5
iarc_publications_oa_roads.loc[iarc_publications_oa_roads['OA Color'] == 'unknown', 'position'] = 6
iarc_publications_oa_roads = iarc_publications_oa_roads.sort_values(by='position')
iarc_publications_oa_roads = iarc_publications_oa_roads.reset_index(drop=True)
iarc_publications_oa_roads = iarc_publications_oa_roads.set_index('OA Color')
iarc_publications_oa_roads


# In[203]:


# IARC publications OA Roads
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_iarc_publications_oa_roads.png'
labels = 'Gold', 'Hybrid', 'Bronze', 'Green', 'Closed', 'Unknown'
colors = ['#FCD820', '#FA810E', '#B1561D', '#35962F', 'black', 'gray']
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(iarc_publications_oa_roads['counts'], explode=explode, autopct='%1.1f%%', labels=labels, shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('IARC publications with DOIs : OA Colors (n=' + str(iarc_publications_dois_n) + ')', fontsize=16)
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[204]:


# UNIGE publications OA Roads
row_unige_publications_oa_unknown = {'OA Color' : 'unknown', 'counts' : unige_publications_oa_unknown_n}
row_unige_publications_not_oa = {'OA Color' : 'closed', 'counts' : unige_publications_not_oa_n}
unige_publications_oa_roads = unige_publications_oa.drop_duplicates(subset='publication_wos_id')['publication_doi_oa_status'].value_counts().rename_axis('OA Color').to_frame('counts')
unige_publications_oa_roads = unige_publications_oa_roads.reset_index()
unige_publications_oa_roads = unige_publications_oa_roads.append(row_unige_publications_oa_unknown, ignore_index=True)
unige_publications_oa_roads = unige_publications_oa_roads.append(row_unige_publications_not_oa, ignore_index=True)
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'gold', 'position'] = 1
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'hybrid', 'position'] = 2
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'bronze', 'position'] = 3
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'green', 'position'] = 4
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'closed', 'position'] = 5
unige_publications_oa_roads.loc[unige_publications_oa_roads['OA Color'] == 'unknown', 'position'] = 6
unige_publications_oa_roads = unige_publications_oa_roads.sort_values(by='position')
unige_publications_oa_roads = unige_publications_oa_roads.reset_index(drop=True)
unige_publications_oa_roads = unige_publications_oa_roads.set_index('OA Color')
unige_publications_oa_roads


# In[205]:


# UNIGE publications OA Roads
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_unige_publications_oa_roads.png'
labels = 'Gold', 'Hybrid', 'Bronze', 'Green', 'Closed', 'Unknown'
colors = ['#FCD820', '#FA810E', '#B1561D', '#35962F', 'black', 'gray']
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(unige_publications_oa_roads['counts'], explode=explode, autopct='%1.1f%%', labels=labels, shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('UNIGE publications with DOIs : OA Colors (n=' + str(unige_publications_dois_n) + ')', fontsize=16)
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[206]:


# IARC citations OA Roads
row_iarc_citations_oa_unknown = {'OA Color' : 'unknown', 'counts' : iarc_citations_oa_unknown_n}
row_iarc_citations_not_oa = {'OA Color' : 'closed', 'counts' : iarc_citations_not_oa_n}
iarc_citations_oa_roads = iarc_citations_oa['citation_doi_oa_status'].value_counts().rename_axis('OA Color').to_frame('counts')
iarc_citations_oa_roads = iarc_citations_oa_roads.reset_index()
iarc_citations_oa_roads = iarc_citations_oa_roads.append(row_iarc_citations_oa_unknown, ignore_index=True)
iarc_citations_oa_roads = iarc_citations_oa_roads.append(row_iarc_citations_not_oa, ignore_index=True)
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'gold', 'position'] = 1
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'hybrid', 'position'] = 2
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'bronze', 'position'] = 3
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'green', 'position'] = 4
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'closed', 'position'] = 5
iarc_citations_oa_roads.loc[iarc_citations_oa_roads['OA Color'] == 'unknown', 'position'] = 6
iarc_citations_oa_roads = iarc_citations_oa_roads.sort_values(by='position')
iarc_citations_oa_roads = iarc_citations_oa_roads.reset_index(drop=True)
iarc_citations_oa_roads = iarc_citations_oa_roads.set_index('OA Color')
iarc_citations_oa_roads


# In[207]:


# IARC citations OA Roads
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_iarc_citations_oa_roads.png'
labels = 'Gold', 'Hybrid', 'Bronze', 'Green', 'Closed', 'Unknown'
colors = ['#FCD820', '#FA810E', '#B1561D', '#35962F', 'black', 'gray']
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(iarc_citations_oa_roads['counts'], explode=explode, autopct='%1.1f%%', labels=labels, shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('IARC citations with DOIs : OA Colors (n=' + str(iarc_citations_dois_n) + ')', fontsize=16)
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[208]:


# UNIGE citations OA Roads
row_unige_citations_oa_unknown = {'OA Color' : 'unknown', 'counts' : unige_citations_oa_unknown_n}
row_unige_citations_not_oa = {'OA Color' : 'closed', 'counts' : unige_citations_not_oa_n}
unige_citations_oa_roads = unige_citations_oa['citation_doi_oa_status'].value_counts().rename_axis('OA Color').to_frame('counts')
unige_citations_oa_roads = unige_citations_oa_roads.reset_index()
unige_citations_oa_roads = unige_citations_oa_roads.append(row_unige_citations_oa_unknown, ignore_index=True)
unige_citations_oa_roads = unige_citations_oa_roads.append(row_unige_citations_not_oa, ignore_index=True)
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'gold', 'position'] = 1
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'hybrid', 'position'] = 2
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'bronze', 'position'] = 3
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'green', 'position'] = 4
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'closed', 'position'] = 5
unige_citations_oa_roads.loc[unige_citations_oa_roads['OA Color'] == 'unknown', 'position'] = 6
unige_citations_oa_roads = unige_citations_oa_roads.sort_values(by='position')
unige_citations_oa_roads = unige_citations_oa_roads.reset_index(drop=True)
unige_citations_oa_roads = unige_citations_oa_roads.set_index('OA Color')
unige_citations_oa_roads


# In[210]:


# UNIGE citations OA Roads
get_ipython().run_line_magic('matplotlib', 'inline')
myfileoutfig = 'figures/27_unige_citations_oa_roads.png'
labels = 'Gold', 'Hybrid', 'Bronze', 'Green', 'Closed', 'Unknown'
colors = ['#FCD820', '#FA810E', '#B1561D', '#35962F', 'black', 'gray']
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(unige_citations_oa_roads['counts'], explode=explode, autopct='%1.1f%%', labels=labels, shadow=False, startangle=0, colors=colors, textprops={'fontsize': 14})
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('UNIGE citations with DOIs : OA Colors (n=' + str(unige_citations_dois_n) + ')', fontsize=16)
fig1.set_size_inches(12, 5)
fig1.savefig(myfileoutfig, bbox_inches='tight')
plt.show()


# In[211]:


# Export values
# IARC publications OA Roads
iarc_publications_oa_roads.to_csv('results/27_iarc_publications_oa_roads.csv', sep='\t', encoding='utf-8', index=True)
# UNIGE publications OA Roads
unige_publications_oa_roads.to_csv('results/27_unige_publications_oa_roads.csv', sep='\t', encoding='utf-8', index=True)
# IARC citations OA Roads
iarc_citations_oa_roads.to_csv('results/27_iarc_citations_oa_roads.csv', sep='\t', encoding='utf-8', index=True)
# UNIGE citations OA Roads
unige_citations_oa_roads.to_csv('results/27_unige_citations_oa_roads.csv', sep='\t', encoding='utf-8', index=True)


# ## 27.  Does it evolve with time?

# In[81]:


# publications DOIs by year of primary publication
unige_publications_doi_counts = unige_all.loc[unige_all['publication_doi'].notna()]['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_with_doi').sort_values(by='publication_year')
# OA publications by year
unige_publications_oa_counts = unige_publications_oa['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_is_oa_count').sort_values(by='publication_year')
# merge
unige_publications_oa_counts = pd.merge(unige_publications_oa_counts, unige_publications_doi_counts, on='publication_year')
# add %
unige_publications_oa_counts['publication_is_oa_percent'] = unige_publications_oa_counts['publication_is_oa_count'] / unige_publications_oa_counts['publications_with_doi']
# remove errors
unige_publications_oa_counts = unige_publications_oa_counts.loc[(unige_publications_oa_counts['publication_year'] > 2000) & (unige_publications_oa_counts['publication_year'] < 2021)]
unige_publications_oa_counts


# In[82]:


# OA status of citations by primary publication year
unige_publications_oa_counts.to_csv('results/27_publications_unige_oa_by_year.csv', sep='\t', encoding='utf-8')


# In[83]:


# publication DOIs by year of primary publication
iarc_publications_doi_counts = iarc_all.loc[iarc_all['publication_doi'].notna()]['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publications_with_doi').sort_values(by='publication_year')
# OA publications by year
iarc_publications_oa_counts = iarc_publications_oa['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='publication_is_oa_count').sort_values(by='publication_year')
# merge
iarc_publications_oa_counts = pd.merge(iarc_publications_oa_counts, iarc_publications_doi_counts, on='publication_year')
# add %
iarc_publications_oa_counts['publication_is_oa_percent'] = iarc_publications_oa_counts['publication_is_oa_count'] / iarc_publications_oa_counts['publications_with_doi']
# remove errors
iarc_publications_oa_counts = iarc_publications_oa_counts.loc[(iarc_publications_oa_counts['publication_year'] > 2000) & (iarc_publications_oa_counts['publication_year'] < 2021)]
iarc_publications_oa_counts


# In[84]:


# OA status of citations by primary publication year
iarc_publications_oa_counts.to_csv('results/27_publications_iarc_oa_by_year.csv', sep='\t', encoding='utf-8')


# In[85]:


# citation DOIs by year of primary publication
unige_citations_doi_counts = unige_all.loc[unige_all['citation_doi'].notna()]['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_with_doi').sort_values(by='publication_year')
# OA citations by year
unige_citations_oa_counts = unige_citations_oa['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citation_is_oa_count').sort_values(by='publication_year')
# merge
unige_citations_oa_counts = pd.merge(unige_citations_oa_counts, unige_citations_doi_counts, on='publication_year')
# add %
unige_citations_oa_counts['citation_is_oa_percent'] = unige_citations_oa_counts['citation_is_oa_count'] / unige_citations_oa_counts['citations_with_doi']
# remove errors
unige_citations_oa_counts = unige_citations_oa_counts.loc[(unige_citations_oa_counts['publication_year'] > 2000) & (unige_citations_oa_counts['publication_year'] < 2021)]
unige_citations_oa_counts


# In[86]:


# OA status of citations by primary publication year
unige_citations_oa_counts.to_csv('results/27_citations_unige_oa_by_year.csv', sep='\t', encoding='utf-8')


# In[87]:


# citation DOIs by year of primary publication
iarc_citations_doi_counts = iarc_all.loc[iarc_all['citation_doi'].notna()]['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citations_with_doi').sort_values(by='publication_year')
# OA citations by year
iarc_citations_oa_counts = iarc_citations_oa['publication_year'].value_counts().rename_axis('publication_year').reset_index(name='citation_is_oa_count').sort_values(by='publication_year')
# merge
iarc_citations_oa_counts = pd.merge(iarc_citations_oa_counts, iarc_citations_doi_counts, on='publication_year')
# add %
iarc_citations_oa_counts['citation_is_oa_percent'] = iarc_citations_oa_counts['citation_is_oa_count'] / iarc_citations_oa_counts['citations_with_doi']
# remove errors
iarc_citations_oa_counts = iarc_citations_oa_counts.loc[(iarc_citations_oa_counts['publication_year'] > 2000) & (iarc_citations_oa_counts['publication_year'] < 2021)]
iarc_citations_oa_counts


# In[88]:


# OA status of citations by primary publication year
iarc_citations_oa_counts.to_csv('results/27_citations_iarc_oa_by_year.csv', sep='\t', encoding='utf-8')


# In[89]:


# merge both tables for publications
publications_oa_counts_by_year = iarc_publications_oa_counts[['publication_year', 'publication_is_oa_percent']]
publications_oa_counts_by_year = publications_oa_counts_by_year.rename(columns={'publication_is_oa_percent' : 'IARC'})
publications_oa_counts_by_year = publications_oa_counts_by_year.merge(unige_publications_oa_counts[['publication_year', 'publication_is_oa_percent']], on='publication_year')
publications_oa_counts_by_year = publications_oa_counts_by_year.rename(columns={'publication_is_oa_percent' : 'UNIGE'})
publications_oa_counts_by_year = publications_oa_counts_by_year.set_index('publication_year')
publications_oa_counts_by_year


# In[90]:


# merge both tables for citations
citations_oa_counts_by_year = iarc_citations_oa_counts[['publication_year', 'citation_is_oa_percent']]
citations_oa_counts_by_year = citations_oa_counts_by_year.rename(columns={'citation_is_oa_percent' : 'IARC'})
citations_oa_counts_by_year = citations_oa_counts_by_year.merge(unige_citations_oa_counts[['publication_year', 'citation_is_oa_percent']], on='publication_year')
citations_oa_counts_by_year = citations_oa_counts_by_year.rename(columns={'citation_is_oa_percent' : 'UNIGE'})
citations_oa_counts_by_year = citations_oa_counts_by_year.set_index('publication_year')
citations_oa_counts_by_year


# In[91]:


# export 26 csv and excel
# publications
publications_oa_counts_by_year.to_csv('results/27_publications_iarc_unige_oa_by_year.csv', index=True, sep='\t', encoding='utf-8')
publications_oa_counts_by_year.to_excel('results/27_publications_iarc_unige_oa_by_year.xlsx', index=True)
# citations
citations_oa_counts_by_year.to_csv('results/27_citations_iarc_unige_oa_by_year.csv', index=True, sep='\t', encoding='utf-8')
citations_oa_counts_by_year.to_excel('results/27_citations_iarc_unige_oa_by_year.xlsx', index=True)


# In[92]:


# year counts for publications
myfileoutfig = 'figures/27_publications_iarc_unige_oa_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = publications_oa_counts_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5,xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of publications with DOIs and OA', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# In[93]:


# year counts for citations
myfileoutfig = 'figures/27_citations_iarc_unige_oa_by_year.png'
plt.rcParams.update({'font.size': 30})
ax = citations_oa_counts_by_year.plot.bar(color=[IARC_color, UNIGE_color], rot=70, width=0.7, edgecolor='white', linewidth=5, xlim=[2000,2020], ylim=[0,1])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('Publication date', fontsize=40)
ax.set_ylabel('Percent', fontsize=40)
ax.set_title('Percent of citations with DOIs and OA', fontsize=40)
ax = ax.legend(loc=2, prop={'size': 40})
fig = ax.get_figure()
fig.set_size_inches(50, 25)
fig.savefig(myfileoutfig, dpi=100)


# ## 27.  Do article that are themselves OA cite more OA journals than articles that are not OA ?

# In[94]:


unige_publications_oa


# In[95]:


unige_publications_not_oa


# In[96]:


unige_publications_oa_unknown


# In[97]:


unige_publications_without_doi_and_citation_with_oa_status


# In[98]:


# OA status of citations from UNIGE OA publications
unige_publications_oa_citaition_oa_status_counts = unige_publications_oa['citation_doi_oa_status'].value_counts().rename_axis('OA_status').reset_index(name='citations_count').sort_values(by='OA_status')
unige_publications_oa_citaition_oa_status_counts


# In[99]:


# OA status of citations from UNIGE closed publications
unige_publications_not_oa_citaition_oa_status_counts = unige_publications_not_oa['citation_doi_oa_status'].value_counts().rename_axis('OA_status').reset_index(name='citations_count').sort_values(by='OA_status')
unige_publications_not_oa_citaition_oa_status_counts


# In[100]:


# OA status of citations from UNIGE OA unknown publications
unige_publications_oa_unknown_citaition_oa_status_counts = unige_publications_oa_unknown['citation_doi_oa_status'].value_counts().rename_axis('OA_status').reset_index(name='citations_count').sort_values(by='OA_status')
unige_publications_oa_unknown_citaition_oa_status_counts


# In[101]:


# OA status of citations from UNIGE publications without DOI
unige_publications_without_doi_and_citation_with_oa_status_counts = unige_publications_without_doi_and_citation_with_oa_status['citation_doi_oa_status'].value_counts().rename_axis('OA_status').reset_index(name='citations_count').sort_values(by='OA_status')
unige_publications_without_doi_and_citation_with_oa_status_counts


# In[102]:


# add 1 to OA citations
unige_publications_oa.loc[unige_publications_oa['citation_doi_oa_status'].isin(oas), 'isoa'] = 1
unige_publications_oa.loc[unige_publications_oa['citation_doi_oa_status'] == 'closed', 'isoa'] = 0
unige_publications_not_oa.loc[unige_publications_not_oa['citation_doi_oa_status'].isin(oas), 'isoa'] = 1
unige_publications_not_oa.loc[unige_publications_not_oa['citation_doi_oa_status'] == 'closed', 'isoa'] = 0
iarc_publications_oa.loc[iarc_publications_oa['citation_doi_oa_status'].isin(oas), 'isoa'] = 1
iarc_publications_oa.loc[iarc_publications_oa['citation_doi_oa_status'] == 'closed', 'isoa'] = 0
iarc_publications_not_oa.loc[iarc_publications_not_oa['citation_doi_oa_status'].isin(oas), 'isoa'] = 1
iarc_publications_not_oa.loc[iarc_publications_not_oa['citation_doi_oa_status'] == 'closed', 'isoa'] = 0


# In[103]:


# UNIGE publications OA and citations OA
unige_publications_oa_citations_oa = unige_publications_oa.loc[unige_publications_oa['citation_doi_oa_status'].isin(oas)]
# UNIGE publications OA and citations not OA
unige_publications_oa_citations_not_oa = unige_publications_oa.loc[unige_publications_oa['citation_doi_oa_status'] == 'closed']
# UNIGE publications not OA and citations OA
unige_publications_not_oa_citations_oa = unige_publications_not_oa.loc[unige_publications_not_oa['citation_doi_oa_status'].isin(oas)]
# UNIGE publications not OA and citations not OA
unige_publications_not_oa_citations_not_oa = unige_publications_not_oa.loc[unige_publications_not_oa['citation_doi_oa_status'] == 'closed']

# IARC publications OA and citations OA
iarc_publications_oa_citations_oa = iarc_publications_oa.loc[iarc_publications_oa['citation_doi_oa_status'].isin(oas)]
# IARC publications OA and citations OA
iarc_publications_oa_citations_not_oa = iarc_publications_oa.loc[iarc_publications_oa['citation_doi_oa_status'] == 'closed']
# IARC publications not OA and citations OA
iarc_publications_not_oa_citations_oa = iarc_publications_not_oa.loc[iarc_publications_not_oa['citation_doi_oa_status'].isin(oas)]
# IARC publications not OA and citations not OA
iarc_publications_not_oa_citations_not_oa = iarc_publications_not_oa.loc[iarc_publications_not_oa['citation_doi_oa_status'] == 'closed']


# In[104]:


# print data results
unige_publications_oa_citations_oa_n = unige_publications_oa_citations_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_oa_citations_oa_p = unige_publications_oa_citations_oa_n / unige_publications_oa_n
print ('UNIGE publications OA : ' + str(unige_publications_oa_n))
print ('UNIGE publications OA with one or more citations OA : ' + str(unige_publications_oa_citations_oa_n))
print ('UNIGE publications OA with one or more citations OA  % : ' + str(unige_publications_oa_citations_oa_p))
unige_publications_oa_citations_not_oa_n = unige_publications_oa_citations_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_oa_citations_not_oa_p = unige_publications_oa_citations_not_oa_n / unige_publications_oa_n
print ('UNIGE publications OA with one or more citations not OA : ' + str(unige_publications_oa_citations_not_oa_n))
print ('UNIGE publications OA with one or more citations not OA  % : ' + str(unige_publications_oa_citations_not_oa_p))
unige_publications_not_oa_citations_oa_n = unige_publications_not_oa_citations_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_not_oa_citations_oa_p = unige_publications_not_oa_citations_oa_n / unige_publications_not_oa_n
print ('UNIGE publications not OA : ' + str(unige_publications_not_oa_n))
print ('UNIGE publications not OA with one or more citations OA : ' + str(unige_publications_not_oa_citations_oa_n))
print ('UNIGE publications not OA with one or more citations OA  % : ' + str(unige_publications_not_oa_citations_oa_p))
unige_publications_not_oa_citations_not_oa_n = unige_publications_not_oa_citations_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
unige_publications_not_oa_citations_not_oa_p = unige_publications_not_oa_citations_not_oa_n / unige_publications_not_oa_n
print ('UNIGE publications not OA with one or more citations not OA : ' + str(unige_publications_not_oa_citations_not_oa_n))
print ('UNIGE publications not OA with one or more citations not OA  % : ' + str(unige_publications_not_oa_citations_not_oa_p))


# In[105]:


unige_publications_oa.groupby(['publication_wos_id'])['isoa'].mean()


# In[106]:


unige_publications_oa_citations_oa_means = unige_publications_oa.groupby(['publication_wos_id'])['isoa'].mean()
unige_publications_oa_citations_oa_mean = unige_publications_oa_citations_oa_means.mean()
print ('UNIGE publications OA : ' + str(unige_publications_oa_n))
print ('UNIGE mean of citations OA per publication within publications OA : ' + str(unige_publications_oa_citations_oa_mean))
unige_publications_not_oa_citations_oa_means = unige_publications_not_oa.groupby(['publication_wos_id'])['isoa'].mean()
unige_publications_not_oa_citations_oa_mean = unige_publications_not_oa_citations_oa_means.mean()
print ('UNIGE publications not OA : ' + str(unige_publications_not_oa_n))
print ('UNIGE mean of citations OA per publication within publications not OA : ' + str(unige_publications_not_oa_citations_oa_mean))


# In[107]:


# print data results
iarc_publications_oa_citations_oa_n = iarc_publications_oa_citations_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_oa_citations_oa_p = iarc_publications_oa_citations_oa_n / iarc_publications_oa_n
print ('IARC publications OA : ' + str(iarc_publications_oa_n))
print ('IARC publications OA with one or more citations OA : ' + str(iarc_publications_oa_citations_oa_n))
print ('IARC publications OA with one or more citations OA  % : ' + str(iarc_publications_oa_citations_oa_p))
iarc_publications_oa_citations_not_oa_n = iarc_publications_oa_citations_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_oa_citations_not_oa_p = iarc_publications_oa_citations_not_oa_n / iarc_publications_oa_n
print ('IARC publications OA with one or more citations not OA : ' + str(iarc_publications_oa_citations_not_oa_n))
print ('IARC publications OA with one or more citations not OA  % : ' + str(iarc_publications_oa_citations_not_oa_p))
iarc_publications_not_oa_citations_oa_n = iarc_publications_not_oa_citations_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_not_oa_citations_oa_p = iarc_publications_not_oa_citations_oa_n / iarc_publications_not_oa_n
print ('IARC publications not OA : ' + str(iarc_publications_not_oa_n))
print ('IARC publications not OA with one or more citations OA : ' + str(iarc_publications_not_oa_citations_oa_n))
print ('IARC publications not OA with one or more citations OA  % : ' + str(iarc_publications_not_oa_citations_oa_p))
iarc_publications_not_oa_citations_not_oa_n = iarc_publications_not_oa_citations_not_oa.drop_duplicates(subset='publication_wos_id').shape[0]
iarc_publications_not_oa_citations_not_oa_p = iarc_publications_not_oa_citations_not_oa_n / iarc_publications_not_oa_n
print ('IARC publications not OA with one or more citations not OA : ' + str(iarc_publications_not_oa_citations_not_oa_n))
print ('IARC publications not OA with one or more citations not OA  % : ' + str(iarc_publications_not_oa_citations_not_oa_p))


# In[108]:


iarc_publications_oa_citations_oa_means = iarc_publications_oa.groupby(['publication_wos_id'])['isoa'].mean()
iarc_publications_oa_citations_oa_mean = iarc_publications_oa_citations_oa_means.mean()
print ('IARC publications OA : ' + str(iarc_publications_oa_n))
print ('IARC mean of citations OA per publication within publications OA : ' + str(iarc_publications_oa_citations_oa_mean))
iarc_publications_not_oa_citations_oa_means = iarc_publications_not_oa.groupby(['publication_wos_id'])['isoa'].mean()
iarc_publications_not_oa_citations_oa_mean = iarc_publications_not_oa_citations_oa_means.mean()
print ('IARC publications not OA : ' + str(iarc_publications_not_oa_n))
print ('IARC mean of citations OA per publication within publications not OA : ' + str(iarc_publications_not_oa_citations_oa_mean))


# In[109]:


# write  results on file
with open('27_oa_citations_means.txt', 'a') as f:
    f.write('27. 27. Do article that are themselves OA cite more OA journals than articles that are not OA?\n')
    f.write('----------------------------------------\n')
    f.write('  \n')
    f.write('UNIGE publications OA : ' + str(unige_publications_oa_n) + '\n')
    f.write('UNIGE publications OA with one or more citations OA : ' + str(unige_publications_oa_citations_oa_n) + '\n')
    f.write('UNIGE publications OA with one or more citations OA  % : ' + str(unige_publications_oa_citations_oa_p) + '\n')
    f.write('UNIGE publications OA with one or more citations not OA : ' + str(unige_publications_oa_citations_not_oa_n) + '\n')
    f.write('UNIGE publications OA with one or more citations not OA  % : ' + str(unige_publications_oa_citations_not_oa_p) + '\n')
    f.write('UNIGE publications not OA : ' + str(unige_publications_not_oa_n) + '\n')
    f.write('UNIGE publications not OA with one or more citations OA : ' + str(unige_publications_not_oa_citations_oa_n) + '\n')
    f.write('UNIGE publications not OA with one or more citations OA  % : ' + str(unige_publications_not_oa_citations_oa_p) + '\n')
    f.write('UNIGE publications not OA with one or more citations not OA : ' + str(unige_publications_not_oa_citations_not_oa_n) + '\n')
    f.write('UNIGE publications not OA with one or more citations not OA  % : ' + str(unige_publications_not_oa_citations_not_oa_p) + '\n')
    f.write('UNIGE mean of citations OA per publication within publications OA : ' + str(unige_publications_oa_citations_oa_mean) + '\n')
    f.write('UNIGE mean of citations OA per publication within publications not OA : ' + str(unige_publications_not_oa_citations_oa_mean) + '\n')
    f.write('  \n')
    f.write('IARC publications OA : ' + str(iarc_publications_oa_n) + '\n')
    f.write('IARC publications OA with one or more citations OA : ' + str(iarc_publications_oa_citations_oa_n) + '\n')
    f.write('IARC publications OA with one or more citations OA  % : ' + str(iarc_publications_oa_citations_oa_p) + '\n')
    f.write('IARC publications OA with one or more citations not OA : ' + str(iarc_publications_oa_citations_not_oa_n) + '\n')
    f.write('IARC publications OA with one or more citations not OA  % : ' + str(iarc_publications_oa_citations_not_oa_p) + '\n')
    f.write('IARC publications not OA : ' + str(iarc_publications_not_oa_n) + '\n')
    f.write('IARC publications not OA with one or more citations OA : ' + str(iarc_publications_not_oa_citations_oa_n) + '\n')
    f.write('IARC publications not OA with one or more citations OA  % : ' + str(iarc_publications_not_oa_citations_oa_p) + '\n')
    f.write('IARC publications not OA with one or more citations not OA : ' + str(iarc_publications_not_oa_citations_not_oa_n) + '\n')
    f.write('IARC publications not OA with one or more citations not OA  % : ' + str(iarc_publications_not_oa_citations_not_oa_p) + '\n')
    f.write('IARC mean of citations OA per publication within publications OA : ' + str(iarc_publications_oa_citations_oa_mean) + '\n')
    f.write('IARC mean of citations OA per publication within publications not OA : ' + str(iarc_publications_not_oa_citations_oa_mean) + '\n')


# In[110]:


unige_publications_oa_citations_oa_means = unige_publications_oa_citations_oa_means.reset_index()
unige_publications_oa_citations_oa_means = unige_publications_oa_citations_oa_means.rename(columns = {'isoa' : 'UNIGE publications OA'})
unige_publications_oa_citations_oa_means


# In[111]:


unige_publications_not_oa_citations_oa_means = unige_publications_not_oa_citations_oa_means.reset_index()
unige_publications_not_oa_citations_oa_means = unige_publications_not_oa_citations_oa_means.rename(columns = {'isoa' : 'UNIGE publications NOT OA'})
unige_publications_not_oa_citations_oa_means


# In[112]:


iarc_publications_oa_citations_oa_means = iarc_publications_oa_citations_oa_means.reset_index()
iarc_publications_oa_citations_oa_means = iarc_publications_oa_citations_oa_means.rename(columns = {'isoa' : 'IARC publications OA'})
iarc_publications_oa_citations_oa_means


# In[113]:


iarc_publications_not_oa_citations_oa_means = iarc_publications_not_oa_citations_oa_means.reset_index()
iarc_publications_not_oa_citations_oa_means = iarc_publications_not_oa_citations_oa_means.rename(columns = {'isoa' : 'IARC publications NOT OA'})
iarc_publications_not_oa_citations_oa_means


# In[114]:


citations_oa_means = unige_publications_oa_citations_oa_means.append(unige_publications_not_oa_citations_oa_means)
citations_oa_means = citations_oa_means.append(iarc_publications_oa_citations_oa_means)
citations_oa_means = citations_oa_means.append(iarc_publications_not_oa_citations_oa_means)
citations_oa_means


# In[115]:


# box plot
myfileoutfig = 'figures/27_citations_oa_means.png'
boxprops = dict(linestyle='-', linewidth=2.5)  
colors = [IARC_color, IARC_color, UNIGE_color, UNIGE_color]
plt.rcParams.update({'font.size': 20})

# fig, ax = plt.subplots()
ax = citations_oa_means[['IARC publications OA', 'IARC publications NOT OA', 'UNIGE publications OA', 'UNIGE publications NOT OA']].plot(kind='box', boxprops=boxprops, color=IARC_color)
# ax = plt.boxplot(publications_oa_citations_oa_means[['UNIGE', 'IARC']])
# ax.boxplot(citations_oa_means[['IARC publications OA', 'IARC publications NOT OA']], positions=[1], boxprops=boxprops)
# ax.boxplot(citations_oa_means[['UNIGE publications OA', 'UNIGE publications NOT OA']], positions=[2], boxprops=boxprops)


ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel('', fontsize=20)
ax.set_ylabel('Percent', fontsize=20)
ax.set_title('Mean of citations OA per publication', fontsize=30)

fig = ax.get_figure()
# fig.suptitle('Mean of citations OA per publication')

# adding horizontal grid lines
# ax.yaxis.grid(True)

fig.set_size_inches(20, 10)
fig.savefig(myfileoutfig, dpi=200)
# plt.show()


# In[269]:


# UNIGE Chi square test
cats = ['gold', 'hybrid', 'bronze', 'green', 'closed']
oas = ['gold', 'hybrid', 'bronze', 'green']
unige_oa_test = unige_all[['publication_wos_id', 'publication_year', 'citation_year', 'publication_doi_oa_status', 'citation_doi_oa_status']]
unige_oa_test = unige_oa_test.dropna(subset=['publication_doi_oa_status', 'citation_doi_oa_status'], how='any')
unige_oa_test.loc[unige_oa_test['publication_doi_oa_status'].isin(oas), 'Publication OA'] = 'Yes'
unige_oa_test.loc[unige_oa_test['publication_doi_oa_status'] == 'closed', 'Publication OA'] = 'No'
unige_oa_test.loc[unige_oa_test['citation_doi_oa_status'].isin(oas), 'Citation OA'] = 'Yes'
unige_oa_test.loc[unige_oa_test['citation_doi_oa_status'] == 'closed', 'Citation OA'] = 'No'
unige_oa_test


# In[270]:


# test with small group
# unige_oa_test = unige_oa_test.iloc[:100]
# unige_oa_test


# In[280]:


unige_oa_test['Publication OA'].value_counts()


# In[272]:


crosstab = pd.crosstab(unige_oa_test['Publication OA'], unige_oa_test['Citation OA'])
crosstab 


# In[273]:


stats.chi2_contingency(crosstab)


# In[274]:


chi2, p, dof, expected = stats.chi2_contingency(crosstab)
nl = '\n'
print(f'Chi2 value= {chi2}{nl}p-value= {p:.10f}{nl}Degrees of freedom= {dof:.10f}{nl}')


# In[275]:


contigency= pd.crosstab(unige_oa_test['Publication OA'], unige_oa_test['Citation OA']) 
contigency


# In[276]:


contigency_pct = pd.crosstab(unige_oa_test['Publication OA'], unige_oa_test['Citation OA'], normalize='index')
contigency_pct


# In[277]:


from scipy.stats import chi2_contingency
import seaborn as sns
plt.figure(figsize=(12,8)) 
sns.heatmap(contigency, annot=True, cmap="YlGnBu")


# In[256]:


# IARC chi square test
cats = ['gold', 'hybrid', 'bronze', 'green', 'closed']
oas = ['gold', 'hybrid', 'bronze', 'green']
iarc_oa_test = iarc_all[['publication_wos_id', 'publication_year', 'citation_year', 'publication_doi_oa_status', 'citation_doi_oa_status']]
iarc_oa_test = iarc_oa_test.dropna(subset=['publication_doi_oa_status', 'citation_doi_oa_status'], how='any')
iarc_oa_test.loc[iarc_oa_test['publication_doi_oa_status'].isin(oas), 'Publication OA'] = 'Yes'
iarc_oa_test.loc[iarc_oa_test['publication_doi_oa_status'] == 'closed', 'Publication OA'] = 'No'
iarc_oa_test.loc[iarc_oa_test['citation_doi_oa_status'].isin(oas), 'Citation OA'] = 'Yes'
iarc_oa_test.loc[iarc_oa_test['citation_doi_oa_status'] == 'closed', 'Citation OA'] = 'No'
iarc_oa_test


# In[257]:


iarc_oa_test['Publication OA'].value_counts()


# In[258]:


from scipy import stats
crosstab = pd.crosstab(iarc_oa_test['Publication OA'], iarc_oa_test['Citation OA'])
crosstab 


# In[259]:


stats.chi2_contingency(crosstab)


# In[260]:


chi2, p, dof, expected = stats.chi2_contingency(crosstab)
nl = '\n'
print(f'Chi2 value= {chi2}{nl}p-value= {p:.10f}{nl}Degrees of freedom= {dof:.10f}{nl}')


# In[262]:


contigency= pd.crosstab(iarc_oa_test['Publication OA'], iarc_oa_test['Citation OA']) 
contigency


# In[263]:


contigency_pct = pd.crosstab(iarc_oa_test['Publication OA'], iarc_oa_test['Citation OA'], normalize='index')
contigency_pct


# In[264]:


from scipy.stats import chi2_contingency
import seaborn as sns
plt.figure(figsize=(12,8)) 
sns.heatmap(contigency, annot=True, cmap="YlGnBu")


# In[ ]:





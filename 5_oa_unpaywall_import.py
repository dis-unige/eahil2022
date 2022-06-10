#!/usr/bin/env python
# coding: utf-8

# # Open Access status for WoS DOIs
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
# 
# ## API unpaywall
# 
# https://unpaywall.org/products/api
# 
# ### Schema
# 
# https://unpaywall.org/data-format
# 
# ### Authentication
# 
# Requests must include your email as a parameter at the end of the URL, like this: api.unpaywall.org/my/request?email=YOUR_EMAIL.
# 
# ### Rate limits
# 
# Please limit use to 100,000 calls per day
# 
# ### Exemple
# 
# https://api.unpaywall.org/v2/10.1038/nature12373?email=YOUR_EMAIL
# 

# In[1]:


import re
import os
import pandas as pd
import time
import datetime
import requests


# ## Extract DOIs for UNIGE
# 

# In[2]:


# open UNIGE data
unige_citations = pd.read_csv('WoS UNIGE results 2001_2020/UNIGE_WoS.csv', encoding='utf-8', header=0, usecols=['Accession Number', 'DOI', 'DOI of cited article'])
unige_citations


# In[3]:


# test values
unige_citations.loc[unige_citations['DOI of cited article'].isna()]


# In[5]:


# unige publications
unige_publications = unige_citations[['Accession Number', 'DOI']].drop_duplicates(subset='Accession Number')
unige_publications


# In[6]:


# test values
unige_publications.loc[unige_publications['DOI'].isna()]


# In[8]:


# open IARC data
iarc_citations = pd.read_csv('WoS IARC results 2001_2020/IARC_WoS.csv', encoding='utf-8', header=0, usecols=['Accession Number', 'DOI', 'DOI of cited article'])
iarc_citations


# In[9]:


# test values
iarc_citations.loc[iarc_citations['DOI of cited article'].isna()]


# In[10]:


# iarc publications
iarc_publications = iarc_citations[['Accession Number', 'DOI']].drop_duplicates(subset='Accession Number')
iarc_publications


# In[11]:


# test values
iarc_publications.loc[iarc_publications['DOI'].isna()]


# In[12]:


# % of UNIGE publications with DOIs
1 - (unige_publications.loc[unige_publications['DOI'].isna()].shape[0] / unige_publications.shape[0])


# In[13]:


# % of UNIGE citations with DOIs
1 - (unige_citations.loc[unige_citations['DOI of cited article'].isna()].shape[0] / unige_citations.shape[0])


# In[15]:


# % of IARC publications with DOIs
1 - (iarc_publications.loc[iarc_publications['DOI'].isna()].shape[0] / iarc_publications.shape[0])


# In[14]:


# % of IARC citations with DOIs
1 - (iarc_citations.loc[iarc_citations['DOI of cited article'].isna()].shape[0] / iarc_citations.shape[0])


# In[16]:


# add dois
dois = unige_publications.append(iarc_publications)
dois


# In[17]:


# rename column to add dois of citations
unige_citations = unige_citations.rename(columns = {'DOI' : 'DOI_publication', 'DOI of cited article': 'DOI'})
unige_citations


# In[18]:


# rename column to add dois of citations
iarc_citations = iarc_citations.rename(columns = {'DOI' : 'DOI_publication', 'DOI of cited article': 'DOI'})
iarc_citations


# In[19]:


# remove nas
unige_citations_dois = unige_citations[['Accession Number', 'DOI']].loc[unige_citations['DOI'].notna()]
unige_citations_dois


# In[20]:


# remove nas
iarc_citations_dois = iarc_citations[['Accession Number', 'DOI']].loc[iarc_citations['DOI'].notna()]
iarc_citations_dois


# In[21]:


# add dois
dois = dois.append(unige_citations_dois)
dois = dois.append(iarc_citations_dois)
dois


# In[22]:


# remove nas and dedup
dois = dois.loc[dois['DOI'].notna()]
dois


# In[23]:


# trim
dois['DOI'] = dois['DOI'].str.strip()
dois


# In[24]:


# dedup
dois_dedup = dois.drop_duplicates(subset='DOI')
dois_dedup


# In[25]:


# reset index
dois_dedup.reset_index(drop=True, inplace=True)
dois_dedup


# In[26]:


# add ID on the first file after that it has to be obtained by DOI merge with the precedent export
# dois_dedup['ID'] = dois_dedup.index + 1
# dois_dedup


# In[27]:


# export
dois_dedup.to_csv('export_dois_all_dedup_2.tsv', sep='\t', index=False)


# ## Import unpaywall data

# In[28]:


import re
import os
import pandas as pd
import time
import datetime
import requests
from requests.exceptions import Timeout
dois_dedup = pd.read_csv('export_dois_without_unpaywall.tsv', sep='\t')
dois_dedup


# In[32]:


# import data from unpaywall
# format natifjson
for index, row in dois_dedup.iterrows():
    if (((index/100) - int(index/100)) == 0) :
        print(index)
    mydoi = row['doi']
    myid = str(row['id']).zfill(10)
    
    # test if file exists (in case of reload of errors)
    # if os.path.exists('E:/data_sources/unpaywall/eahil_2022/' + myid + '.json'):
    #     continue
    
    # start from (in case of error)
    # if row['id'] < 644200 :
    #     continue
    
    # folder
    myfolder = str(int(row['id']/100000)+1)
    # 1 sec pause (not necessary, without it we don't make more than 100'000 per day)
    # time.sleep(1)
    searchurl = 'https://api.unpaywall.org/v2/' + mydoi + '?email=pablo.iriarte@unige.ch'
    headers = {'Accept': 'application/json'}
    try:
        resp = requests.get(searchurl, headers=headers, timeout=30)
    except Timeout:
        print('ERROR TIMEOUT - ID:' + myid + ' - DOI:' +  mydoi)
    else:
        # print(resp)
        if (resp.status_code == 200):
            # export
            with open('E:/data_sources/unpaywall/eahil_2022/eahil_2022_' + myfolder + '/' + myid + '.json', 'w', encoding='utf-8') as f:
                f.write(resp.text)
        else :
            print('ERROR - ID:' + myid + ' - DOI:' +  mydoi)


# In[ ]:





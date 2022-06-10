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
# * unpaywall data downloaded using the notebook "doi_unpaywall.ipynb" or queries made directly on unpaywall website
# 
# ## unpaywall data extraction
# 
# https://unpaywall.org/data-format
# 
# Fields to extract:
# 
#  - is_oa : Boolean (Is there an OA copy of this resource
#  - oa_status : Strin (The OA status, or color, of this resource: gold, hybrid, bronze, green or closed)
#  - has_repository_copy : Boolean (Whether there is a copy of this resource in a repository. True if this resource has at least one OA Location with host_type = "repository". False otherwise.)
# 
# 
# 

# In[1]:


import re
import os
import pandas as pd
import time
import datetime
import json
import numpy as np


# ## DOIs
# 

# In[2]:


# open DOIs data
dois = pd.read_csv('export_dois_all_dedup.tsv', encoding='utf-8', sep='\t', header=0)
dois


# In[3]:


# del and rename cols
del dois['Accession Number']
dois = dois.rename(columns={'DOI' : 'doi', 'ID': 'id'})
dois


# In[4]:


# open the second series of DOIs (obtained after fixing the bug on the parsing code)
dois_2 = pd.read_csv('export_dois_without_unpaywall.tsv', encoding='utf-8', sep='\t', header=0)
dois_2


# In[5]:


# append
dois = dois.append(dois_2, ignore_index=True)
dois


# In[6]:


# dedup by DOI and keep only the last
dois = dois.drop_duplicates(subset='doi', keep='last')
dois


# In[7]:


# export to csv and excel
dois.to_csv('export_dois_1_and_2_dedup.tsv', sep='\t', encoding='utf-8', index=False)
dois.to_excel('export_dois_1_and_2_dedup.xlsx', index=False)


# ## Publications from UNIGE
# 

# In[8]:


# open UNIGE data
unige_citations = pd.read_csv('WoS UNIGE results 2001_2020/UNIGE_WoS.csv', encoding='utf-8', header=0, usecols=['ID', 'Accession Number', 'DOI', 'DOI of cited article'])
unige_citations


# In[9]:


unige_citations.loc[unige_citations['Accession Number'].isna()]


# In[10]:


unige_citations.loc[unige_citations['Accession Number']=='']


# In[11]:


# unige publications by ID
unige_publications_rows = unige_citations[['ID', 'Accession Number', 'DOI']].drop_duplicates(subset='ID').shape[0]
unige_publications_rows


# In[12]:


# unige publications
unige_publications = unige_citations[['Accession Number', 'DOI']].drop_duplicates(subset='Accession Number')
del unige_publications['Accession Number']
unige_publications = unige_publications.rename(columns={'DOI' : 'doi'})
unige_publications_dois = unige_publications.loc[unige_publications['doi'].notna()]
unige_publications_dois


# In[13]:


unige_publications


# In[14]:


# unige citations with DOIs
del unige_citations['Accession Number']
del unige_citations['ID']
del unige_citations['DOI']
unige_citations = unige_citations.rename(columns={'DOI of cited article' : 'doi'})
unige_citations_dois = unige_citations.loc[unige_citations['doi'].notna()]
unige_citations_dois


# In[15]:


# open IARC data
iarc_citations = pd.read_csv('WoS IARC results 2001_2020/IARC_WoS.csv', encoding='utf-8', header=0, usecols=['Accession Number', 'DOI', 'DOI of cited article'])
iarc_citations


# In[16]:


# iarc publications with DOIs
iarc_publications = iarc_citations[['Accession Number', 'DOI']].drop_duplicates(subset='Accession Number')
del iarc_publications['Accession Number']
iarc_publications = iarc_publications.rename(columns={'DOI' : 'doi'})
iarc_publications_dois = iarc_publications.loc[iarc_publications['doi'].notna()]
iarc_publications_dois


# In[17]:


# iarc citations with DOIs
del iarc_citations['Accession Number']
del iarc_citations['DOI']
iarc_citations = iarc_citations.rename(columns={'DOI of cited article' : 'doi'})
iarc_citations_dois = iarc_citations.loc[iarc_citations['doi'].notna()]
iarc_citations_dois


# In[18]:


# add columns
unige_publications_dois['doi'] = unige_publications_dois['doi'].str.strip()
unige_citations_dois['doi'] = unige_citations_dois['doi'].str.strip()
iarc_publications_dois['doi'] = iarc_publications_dois['doi'].str.strip()
iarc_citations_dois['doi'] = iarc_citations_dois['doi'].str.strip()
unige_publications_dois['publication_unige'] = 1
unige_citations_dois['citation_unige'] = 1
iarc_publications_dois['publication_iarc'] = 1
iarc_citations_dois['citation_iarc'] = 1


# In[19]:


# merge the publication and citation information
dois = pd.merge(dois, unige_publications_dois, on='doi', how='left')
dois = pd.merge(dois, unige_citations_dois, on='doi', how='left')
dois = pd.merge(dois, iarc_publications_dois, on='doi', how='left')
dois = pd.merge(dois, iarc_citations_dois, on='doi', how='left')
dois


# In[20]:


# drop duplicates
dois = dois.drop_duplicates(subset='id')
dois


# In[21]:


# reset index
dois.reset_index(drop=True, inplace=True)
dois


# In[22]:


# test empty rows
dois.loc[dois['publication_unige'].isna() & dois['citation_unige'].isna() & dois['publication_iarc'].isna() & dois['citation_iarc'].isna()]


# In[23]:


# export
dois.to_csv('export_dois_all_dedup_publications_citations.tsv', sep='\t', index=False)


# ## unpaywall OA status

# In[22]:


# extract informtation on downloaded data from unpaywall
for index, row in dois.iterrows():
    mydoi = row['doi']
    myid = str(row['id']).zfill(10)
    myfolder = str(int(row['id']/100000)+1)
    # print(myid)
    if (((index/1000) - int(index/1000)) == 0) :
        print(index)
    # open the json file
    if os.path.exists('E:/data_sources/unpaywall/eahil_2022/eahil_2022_' + myfolder + '/' + myid + '.json'):
        # initialising variables
        doi_unpaywall = ''
        oa_status = ''
        has_repository_copy = ''
        with open('E:/data_sources/unpaywall/eahil_2022/eahil_2022_' + myfolder + '/' + myid + '.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if ('doi' in data):
                doi_unpaywall = data['doi']
            if ('oa_status' in data):
                oa_status = data['oa_status']
            if ('has_repository_copy' in data):
                has_repository_copy = data['has_repository_copy']

        dois.at[index,'doi_unpaywall'] = doi_unpaywall
        dois.at[index,'oa_status'] = oa_status
        dois.at[index,'has_repository_copy'] = has_repository_copy
    else :
        # print(str(row['id']) + ' - not found')
        with open('unpaywall_extract_errors.txt', 'a', encoding='utf-8') as g:
            g.write(str(row['id']) + '	file not found\n')


# In[23]:


dois


# In[24]:


dois['oa_status'].value_counts()


# In[25]:


dois['has_repository_copy'].value_counts()


# In[26]:


# dois found
dois.loc[dois['doi_unpaywall'].notna()].shape[0]


# In[27]:


# dois found
dois.loc[dois['doi_unpaywall'].notna()].shape[0] / dois.shape[0]


# In[28]:


# dois not found
dois.loc[dois['doi_unpaywall'].isna()].shape[0]


# In[29]:


# dois not found
dois.loc[dois['doi_unpaywall'].isna()].shape[0] / dois.shape[0]


# In[30]:


# dois not equal
dois.loc[(dois['doi'] != dois['doi_unpaywall']) & dois['doi_unpaywall'].notna()]


# In[31]:


# normalize DOIs
dois.loc[dois['doi'].notna(), 'doi_normalized'] = dois['doi'].str.upper()
dois.loc[dois['doi_unpaywall'].notna(), 'doi_unpaywall_normalized'] = dois['doi_unpaywall'].str.upper()
dois


# In[32]:


# dois not equal
dois.loc[(dois['doi_normalized'] != dois['doi_unpaywall_normalized']) & dois['doi_unpaywall_normalized'].notna()]


# In[33]:


# dois not equal
dois.loc[(dois['doi_normalized'] != dois['doi_unpaywall_normalized']) & dois['doi_unpaywall_normalized'].notna()].shape[0]


# In[34]:


# export dois not equal
dois.loc[(dois['doi_normalized'] != dois['doi_unpaywall_normalized']) & dois['doi_unpaywall_normalized'].notna()].to_excel('export_dois_wos_unpaywall_not_equal.xlsx', index=False)


# In[35]:


# export to csv and excel
dois.to_csv('export_dois_oa_status.tsv', sep='\t', encoding='utf-8', index=False)
dois.to_excel('export_dois_oa_status.xlsx', index=False)


# # Add OA status to publications and citations

# In[36]:


# open UNIGE data
unige_all = pd.read_csv('WoS UNIGE results 2001_2020/UNIGE_WoS.csv', encoding='utf-8', header=0, usecols=['Accession Number', 'Document Type', 'Year Published', '29 Character Source Abbreviation', 'Open Access Indicator', 'PubMed ID', 'DOI', 'Year of cited article', 'Journal of cited article', 'DOI of cited article'])
unige_all


# In[37]:


# open IARC data
iarc_all = pd.read_csv('WoS IARC results 2001_2020/IARC_WoS.csv', encoding='utf-8', header=0, usecols=['Accession Number', 'Document Type', 'Year Published', '29 Character Source Abbreviation', 'Open Access Indicator', 'PubMed ID', 'DOI', 'Year of cited article', 'Journal of cited article', 'DOI of cited article'])
iarc_all


# In[38]:


# rename columns
unige_all = unige_all.rename(columns={'Accession Number' : 'publication_wos_id',
                                      'Year Published' : 'publication_year',
                                     'Document Type' : 'publication_type',
                                     '29 Character Source Abbreviation' : 'publication_journal',
                                     'DOI' : 'publication_doi',
                                     'PubMed ID' : 'publication_pmid',
                                     'Open Access Indicator' : 'publication_wos_oa',
                                     'Year of cited article' : 'citation_year',
                                     'Journal of cited article' : 'citation_journal',
                                     'DOI of cited article' : 'citation_doi'})
unige_all


# In[39]:


# rename columns
iarc_all = iarc_all.rename(columns={'Accession Number' : 'publication_wos_id',
                                      'Year Published' : 'publication_year',
                                     'Document Type' : 'publication_type',
                                     '29 Character Source Abbreviation' : 'publication_journal',
                                     'DOI' : 'publication_doi',
                                     'PubMed ID' : 'publication_pmid',
                                     'Open Access Indicator' : 'publication_wos_oa',
                                     'Year of cited article' : 'citation_year',
                                     'Journal of cited article' : 'citation_journal',
                                     'DOI of cited article' : 'citation_doi'})
iarc_all


# In[40]:


# strip DOIs
unige_all['publication_doi'] = unige_all['publication_doi'].str.strip()
unige_all['citation_doi'] = unige_all['citation_doi'].str.strip()
iarc_all['publication_doi'] = iarc_all['publication_doi'].str.strip()
iarc_all['citation_doi'] = iarc_all['citation_doi'].str.strip()


# In[41]:


# merge in UNIGE file for publications
unige_all = pd.merge(unige_all, dois, left_on='publication_doi', right_on='doi', how='left')
unige_all


# In[42]:


# merge in UNIGE file for citations
unige_all = pd.merge(unige_all, dois, left_on='citation_doi', right_on='doi', how='left')
unige_all


# In[43]:


unige_all.columns


# In[44]:


# merge in IARC file
iarc_all = pd.merge(iarc_all, dois, left_on='publication_doi', right_on='doi', how='left')
iarc_all


# In[45]:


# merge in IARC file for citations
iarc_all = pd.merge(iarc_all, dois, left_on='citation_doi', right_on='doi', how='left')
iarc_all


# In[46]:


iarc_all.columns


# In[47]:


# del columns not used and rename
del unige_all['doi_normalized_x']
del unige_all['doi_unpaywall_normalized_x']
del unige_all['doi_unpaywall_x']
del unige_all['id_x']
del unige_all['doi_x']
del unige_all['doi_normalized_y']
del unige_all['doi_unpaywall_normalized_y']
del unige_all['doi_unpaywall_y']
del unige_all['id_y']
del unige_all['doi_y']
# rename columns
unige_all = unige_all.rename(columns={'publication_unige_x' : 'publication_doi_is_unige_publication',
                                      'publication_unige_y' : 'citation_doi_is_unige_publication',
                                      'citation_unige_x' : 'publication_doi_is_unige_citation',
                                      'citation_unige_y' : 'citation_doi_is_unige_citation',
                                     'publication_iarc_x' : 'publication_doi_is_iarc_publication',
                                      'publication_iarc_y' : 'citation_doi_is_iarc_publication',
                                      'citation_iarc_x' : 'publication_doi_is_iarc_citation',
                                      'citation_iarc_y' : 'citation_doi_is_iarc_citation',
                                     'oa_status_x' : 'publication_doi_oa_status',
                                     'oa_status_y' : 'citation_doi_oa_status',
                                     'has_repository_copy_x' : 'publication_doi_has_repository_copy',
                                     'has_repository_copy_y' : 'citation_doi_has_repository_copy'})
unige_all


# In[48]:


unige_all.columns


# In[49]:


del iarc_all['doi_normalized_x']
del iarc_all['doi_unpaywall_normalized_x']
del iarc_all['doi_unpaywall_x']
del iarc_all['id_x']
del iarc_all['doi_x']
del iarc_all['doi_normalized_y']
del iarc_all['doi_unpaywall_normalized_y']
del iarc_all['doi_unpaywall_y']
del iarc_all['id_y']
del iarc_all['doi_y']
# rename columns
iarc_all = iarc_all.rename(columns={'publication_unige_x' : 'publication_doi_is_unige_publication',
                                      'publication_unige_y' : 'citation_doi_is_unige_publication',
                                      'citation_unige_x' : 'publication_doi_is_unige_citation',
                                      'citation_unige_y' : 'citation_doi_is_unige_citation',
                                     'publication_iarc_x' : 'publication_doi_is_iarc_publication',
                                      'publication_iarc_y' : 'citation_doi_is_iarc_publication',
                                      'citation_iarc_x' : 'publication_doi_is_iarc_citation',
                                      'citation_iarc_y' : 'citation_doi_is_iarc_citation',
                                     'oa_status_x' : 'publication_doi_oa_status',
                                     'oa_status_y' : 'citation_doi_oa_status',
                                     'has_repository_copy_x' : 'publication_doi_has_repository_copy',
                                     'has_repository_copy_y' : 'citation_doi_has_repository_copy'})
iarc_all


# In[50]:


iarc_all.columns


# In[51]:


# export of dois without unpaywall information to test a new download
unige_publications_with_dois_without_unpaywall = unige_all.loc[unige_all['publication_doi'].notna() & unige_all['publication_doi_oa_status'].isna()][['publication_wos_id', 'publication_doi']]
unige_citations_with_dois_without_unpaywall = unige_all.loc[unige_all['citation_doi'].notna() & unige_all['citation_doi_oa_status'].isna()][['publication_wos_id', 'citation_doi']]
iarc_publications_with_dois_without_unpaywall = iarc_all.loc[iarc_all['publication_doi'].notna() & iarc_all['publication_doi_oa_status'].isna()][['publication_wos_id', 'publication_doi']]
iarc_citations_with_dois_without_unpaywall = iarc_all.loc[iarc_all['citation_doi'].notna() & iarc_all['citation_doi_oa_status'].isna()][['publication_wos_id', 'citation_doi']]
# rename columns
unige_publications_with_dois_without_unpaywall = unige_publications_with_dois_without_unpaywall.rename(columns={'publication_doi' : 'doi'})
unige_citations_with_dois_without_unpaywall = unige_citations_with_dois_without_unpaywall.rename(columns={'citation_doi' : 'doi'})
iarc_publications_with_dois_without_unpaywall = iarc_publications_with_dois_without_unpaywall.rename(columns={'publication_doi' : 'doi'})
iarc_citations_with_dois_without_unpaywall = iarc_citations_with_dois_without_unpaywall.rename(columns={'citation_doi' : 'doi'})


# In[52]:


# append dfs and reindex
dois_without_unpaywall = unige_publications_with_dois_without_unpaywall.append(unige_citations_with_dois_without_unpaywall, ignore_index=True)
dois_without_unpaywall = dois_without_unpaywall.append(iarc_publications_with_dois_without_unpaywall, ignore_index=True)
dois_without_unpaywall = dois_without_unpaywall.append(iarc_citations_with_dois_without_unpaywall, ignore_index=True)
# dedup
dois_without_unpaywall = dois_without_unpaywall.drop_duplicates(subset='doi')
# reset index
dois_without_unpaywall.reset_index(drop=True, inplace=True)
# add new id
dois_without_unpaywall['id'] = dois_without_unpaywall.index + 800001
dois_without_unpaywall


# In[53]:


dois_without_unpaywall[['id', 'doi']].to_csv('export_dois_without_unpaywall.tsv', sep='\t', index=False)


# In[54]:


# export files
unige_all.to_csv('unige_all_oa_status_citations.csv', sep='\t', index=False, encoding='utf-8')
# unige_all.to_excel('unige_all_oa_status_citations.xlsx', index=False)
iarc_all.to_csv('iarc_all_oa_status_citations.csv', sep='\t', index=False, encoding='utf-8')
iarc_all.to_excel('iarc_all_oa_status_citations.xlsx', index=False)


# In[ ]:





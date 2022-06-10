#!/usr/bin/env python
# coding: utf-8

# # Automating exports using Web of Science
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
# ## Required python libraries 
# 1. selenium
# 1. os
# 1. time
# 1. datetime
# 
# 
# ## Export steps
# 1. Launch WoS advanced search, accept cookies and close tutorial pop-ups
# 1. Exclude editions not needed (in our case we remove SSCI and AHCI edition keeping only SCI edition and Emerging sources)
# 1. Search by affiliation name\*, range of publication years (in our case "2001-2020") and categories\**
# 1. Export results by groups of articles (max. 500 at a time) with the cited refs
# 1. Rename the file with the range of records
# 
# \* using the name given by WoS on the affiliation list (in our case "University of Geneva")  
# \** using a choice of subjetcs from the list available on Clarivate Website: https://support.clarivate.com/ScientificandAcademicResearch/s/article/Web-of-Science-List-of-Subject-Classifications-for-All-Databases?language=en_US
# 

# In[2]:


import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
import datetime

# search criteria
affiliation = 'University of Geneva'
publication_years = '2001-2020'
categories = '"Life Sciences & Biomedicine - Other Topics" OR "Allergy" OR "Anatomy & Morphology" OR "Anesthesiology" OR "Biochemistry & Molecular Biology" OR "Biophysics" OR "Biotechnology & Applied Microbiology" OR "Cardiovascular System & Cardiology" OR "Cell Biology" OR "Critical Care Medicine" OR "Dentistry, Oral Surgery & Medicine" OR "Dermatology" OR "Developmental Biology" OR "Emergency Medicine" OR "Endocrinology & Metabolism" OR "Evolutionary Biology" OR "Gastroenterology & Hepatology" OR "General & Internal Medicine" OR "Genetics & Heredity" OR "Geriatrics & Gerontology" OR "Health Care Sciences & Services" OR "Hematology" OR "Immunology" OR "Infectious Diseases" OR "Integrative & Complementary Medicine" OR "Legal Medicine" OR "Mathematical & Computational Biology" OR "Medical Ethics" OR "Medical Informatics" OR "Medical Laboratory Technology" OR "Microbiology" OR "Neurosciences & Neurology" OR "Nursing" OR "Nutrition & Dietetics" OR "Obstetrics & Gynecology" OR "Oncology" OR "Ophthalmology" OR "Orthopedics" OR "Otorhinolaryngology" OR "Parasitology" OR "Pathology" OR "Pediatrics" OR "Pharmacology & Pharmacy" OR "Physiology" OR "Psychiatry" OR "Public, Environmental & Occupational Health" OR "Radiology, Nuclear Medicine & Medical Imaging" OR "Rehabilitation" OR "Reproductive Biology" OR "Research & Experimental Medicine" OR "Respiratory System" OR "Rheumatology" OR "Sport Sciences" OR "Substance Abuse" OR "Surgery" OR "Toxicology" OR "Transplantation" OR "Tropical Medicine" OR "Urology & Nephrology" OR "Veterinary Sciences" OR "Virology"'

# WoS editions to exclude (yes|no)
exclude_ssci = 'yes'
exclude_ahci = 'yes'

# downloads parameters
download_dir = 'D:\\switchdrive\\EAHIL\\EAHIL_2022\\code\\data\\sources'

# number of records to be downloaded at a time (max. 500)
download_records = 500

# in case of interruption of downloads define the files to skip
skip_files = 0

# URL for WoS advanced search
wos_url = 'https://www.webofscience.com/wos/woscc/advanced-search'

# construct WoS query
query = 'OG=(' + affiliation + ')'
if (publication_years != '') :
    query = query + ' AND PY=(' + publication_years + ')'
if (categories != '') :
    query = query + ' AND WC=(' + categories + ')'

# options for selenium browser and downloads
options = Options()
options.set_preference('browser.download.folderList',2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', download_dir)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream,text/csv,application/csv,text/plain')
driver = webdriver.Firefox(executable_path = r'geckodriver\geckodriver.exe', options = options)
driver.maximize_window()


# In[3]:


# go to WoS search page
driver.get(wos_url)

# accept cookies
time.sleep(1)
driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()

# close tutorial windows
time.sleep(1)
driver.find_element_by_xpath('//*[@class="bb-button _pendo-button-primaryButton _pendo-button"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="bb-button _pendo-button-secondaryButton _pendo-button"]').click()

# exclude SSCI
if (exclude_ssci == 'yes'):
    # select WoS editions
    time.sleep(1)
    driver.find_element_by_xpath('//*[@aria-label="selectEdition Science Citation Index Expanded<br/>(SCI-EXPANDED)--1900-present"]').click()
    # unselect SSCI
    time.sleep(1)
    driver.find_element_by_xpath('//*[@title="Social Sciences Citation Index<br/>(SSCI)--1956-present"]').click()


# exclude AHCI
if (exclude_ahci == 'yes'):
    # select WoS editions
    time.sleep(1)
    driver.find_element_by_xpath('//*[@aria-label="selectEdition Science Citation Index Expanded<br/>(SCI-EXPANDED)--1900-present"]').click()
    # unselect AHCI
    time.sleep(1)
    driver.find_element_by_xpath('//*[@title="Arts & Humanities Citation Index<br/>(AHCI)--1975-present"]').click()

# input search query
time.sleep(1)
driver.find_element_by_id('advancedSearchInputArea').send_keys(query)

# send query
time.sleep(1)
driver.find_element_by_xpath('//*[@data-ta="run-search"]').click()

# extract the number of results
time.sleep(3)
results = driver.find_element_by_xpath('//*[@data-ta-search-info-count]').get_attribute('data-ta-search-info-count')

# count files needed
results = int(results)
if (results <= download_records):
    files = 1
else :
    files = int(results / download_records) + 1


# In[3]:


# export results by sets of 500 records
print ('Results: ' + str(results))
print ('Files to export: ' + str(files))
print('Start time: ' + str(datetime.datetime.now()))
print('-----------------------------------')
print(' ')

for i in range(files):
    if (skip_files > 0 and i < skip_files):
        continue
    time.sleep(1)
    file_start = i * download_records + 1
    if (i + 1 == files):
        file_end = results
    else :
        file_end = i * download_records + download_records
    filename = 'savedrecs_' + str(file_start).zfill(10) + '_' + str(file_end).zfill(10) + '.txt'
    print ('File ' + str(i + 1) + ' of ' + str(files) + ' "' + filename + '" from ' + str(file_start) + ' to ' + str(file_end), end='')
    
    # downloads loop
    download_successful = False
    while not download_successful:
        # click on export button
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="mat-focus-indicator mat-menu-trigger cdx-but-md cdx-but-white-background margin-right-10--reversible mat-button mat-stroked-button mat-button-base mat-primary"]').click()

        # click on export button
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="exportToTabWinButton"]').click()

        # click on records range
        time.sleep(1)
        driver.find_element_by_xpath('//*[@for="radio3-input"]').click()

        # empty from range
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="Input starting record range"]').clear()

        # put from range
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="Input starting record range"]').send_keys(str(file_start))

        # empty to range
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="Input ending record range"]').clear()

        # put to range
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="Input ending record range"]').send_keys(str(file_end))

        # select record content dropdown
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label=" Author, Title, Source"]').click()

        # select record content fields
        time.sleep(1)
        driver.find_element_by_xpath('//*[@title="Full Record and Cited References"]').click()

        # run export
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="mat-focus-indicator cdx-but-md mat-stroked-button mat-button-base mat-primary"]').click()

        # wait for download to finish
        print(' - Waiting for download ', end='')
        while not any([filename == 'savedrecs.txt' for filename in os.listdir('data/sources/')]):
            time.sleep(2)
            print('.', end='')
        print(' done!')

        # test file size
        time.sleep(1)
        filesize = os.path.getsize('data/sources/savedrecs.txt')
        if (filesize > 0):
            download_successful = True
        else :
            os.remove('data/sources/savedrecs.txt')
    
    # rename file
    time.sleep(1)
    os.rename('data/sources/savedrecs.txt', 'data/sources/' + filename)

print(' ')
print('-----------------------------------')
print('End time: ' + str(datetime.datetime.now()))


# In[ ]:





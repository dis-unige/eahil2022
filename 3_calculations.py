# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:49:56 2022

@author: Ramon
"""
##############################################################################################################
##############################################################################################################

def calculations_WoS(file_name, folder, year1, year2):
    # import modules
    import pandas as pd
    from statistics import mode
    # import numpy as np
    
    ##############################################################################################################
    
    # file name + directory
    file = folder + file_name

    # read csv file in chuncks, its more efficient
    df_chuncks = pd.read_csv(file, chunksize=10000, sep=",")  # the number of rows per chunk
    df_chunk_list = []
    for sub_df in df_chuncks:
        df_chunk_list.append(sub_df)
    del(file); del(sub_df); del(df_chuncks)
    # merge them together
    df_original = pd.concat(df_chunk_list,sort=False)
    del(df_chunk_list)
    
    # change column names 
    df_original.columns = df_original.columns.str.replace(' ','_')
    # return(df_original)
    
    ##############################################################################################################
    
    # Summary
    report_lines = []
    df_shape1 = df_original.shape[0]
    report_lines.append("CALCULATIONS REPORT")
    report_lines.append("")
    report_lines.append("Number of publications retrieved from WoS:                                           " + str(len(list(set(list(df_original["ID"]))))))
    report_lines.append("Number of citations retrieved from WoS:                                              " + str(df_shape1))
    report_lines.append("")
    
    # filters    
    ### Remove need to be checked with Yes
    df = df_original[df_original['Need_to_be_checked']=="No"]
    df_shape2 = df.shape[0]
    report_lines.append("Number of entries removed due to human revision:                                     " + str(df_shape1 - df_shape2))
    
    ### Remove abstract meetings
    df_doctype = df[df.Document_Type.str.match("\W*(Meeting Abstract)\W*")]
    meeting_abstract_combinations = (list(set(list(df_doctype["Document_Type"]))))  
    df = df[~df['Document_Type'].isin(meeting_abstract_combinations)]
    df_shape3 = df.shape[0]
    report_lines.append("Number of entries removed due to Abstract meeting document type:                     " + str(df_shape2 - df_shape3))
    del(df_doctype)
    
    ### Remove negative year diff
    ### Correct values with reasonable negative year
    report_lines.append("Number of entries with an years difference of -1 or -2 changed to 0:                 " + str(df.loc[df["Years_difference"] == -1].shape[0] + df.loc[df["Years_difference"] == -2].shape[0]))
    df.loc[df["Years_difference"] == -1] = 0
    df.loc[df["Years_difference"] == -2] = 0
    
    ### Conflictive time issues
    df = df[df['Years_difference'] >= 0]
    df_shape4 = df.shape[0]
    report_lines.append("Number of entries removed due to conflictive time differences                        " + str(df_shape3 - df_shape4))
    
    ### Keep references of selected years range
    df = df[(df['Year_Published'] <= year2) & (df['Year_Published'] >= year1)]
    df_shape5 = df.shape[0]
    report_lines.append("Number of entries removed because of the selected years range (" + str(year1) + ", " + str(year2) + ")           " + str(df_shape4 - df_shape5))
    
    ### Change missing ISSN to "Empty"
    df['ISSN'] = df['ISSN'].fillna("Empty")#; df_missing_ISSN = df[df.ISSN == 'Empty'].shape[0]
    
    ### Change missing citation journal to "Empty"
    df['Journal_of_cited_article'] = df['Journal_of_cited_article'].fillna("Empty")#; df_missing_ISSN = df[df.ISSN == 'Empty'].shape[0]
    
    ### Save deleted rows
    df_deleted = df_original.loc[~df_original.index.isin(list(df.index))]
    df_deleted.to_csv(folder + "//" + file_name.replace(".csv","") + "_deleted.csv", index=False, sep=";", chunksize=10000)
    report_lines.append("")
    report_lines.append("Final number of entries                                                              " + str(df.shape[0]))
    report_lines.append("Final number of publications                                                         " + str(len(list(set(list(df["ID"]))))))
    report_lines.append("Number of removed entries                                                            " + str(df_original.shape[0] - df.shape[0]))
    report_lines.append("Number of removed publications                                                       " + str(len(list(set(list(df_original["ID"])))) - len(list(set(list(df["ID"]))))))
    report_lines.append("")
    
    control = df_deleted.shape[0] == ((df_shape1 - df_shape2) + (df_shape2 - df_shape3) + (df_shape3 - df_shape4) + (df_shape4 - df_shape5))
    report_lines.append("Control                                                                              " + str(control))
    
    # Save report
    report_file = folder + "Calculations_report.txt"
    with open(report_file, 'w') as f:
        for line in report_lines:
            f.write(line)
            f.write('\n')
            
    # Save df after filters
    # df.to_excel(folder + "df_filtered.xlsx", index=False)
    df.to_csv(folder + "df_filtered.csv", index=False, sep=",", chunksize=10000)
    # return(df)

    ##############################################################################################################
    
    # 13 - Average age of citations as global average
    print("")
    print("13 ############################################################################")
    print("")
    print("Control: ", df[["Years_difference"]].dropna().shape[0] == df.shape[0]) # if True no NA's in this column

    df_yeardiff = df[["Years_difference"]].describe()
    df_yeardiff['Calculation'] = df_yeardiff.index
    df_yeardiff = pd.concat([df_yeardiff, pd.DataFrame({'Calculation':['mode'], 'Years_difference':[mode(list(df["Years_difference"]))]})],
                            ignore_index = True)
    df["Years_difference"].value_counts().rename_axis('Year_difference').reset_index(name='Counts').head(5)
    df_yeardiff = df_yeardiff[list(df_yeardiff.columns)[::-1]]
    
    ### Rename labels
    df_yeardiff = df_yeardiff.rename(columns={"Years_difference":"Value"})
    df_yeardiff.loc[(df_yeardiff.Calculation == 'count'),'Calculation'] = "Citations"
    df_yeardiff.loc[(df_yeardiff.Calculation == 'mean'),'Calculation'] = "YD_mean"
    df_yeardiff.loc[(df_yeardiff.Calculation == 'std'),'Calculation'] = "YD_std"
    df_yeardiff.loc[(df_yeardiff.Calculation == 'min'),'Calculation'] = "YD_min"
    df_yeardiff.loc[(df_yeardiff.Calculation == '25%'),'Calculation'] = "YD_25%"
    df_yeardiff.loc[(df_yeardiff.Calculation == '50%'),'Calculation'] = "YD_50%"
    df_yeardiff.loc[(df_yeardiff.Calculation == '75%'),'Calculation'] = "YD_75%"
    df_yeardiff.loc[(df_yeardiff.Calculation == 'max'),'Calculation'] = "YD_max"
    df_yeardiff.loc[(df_yeardiff.Calculation == 'mode'),'Calculation'] = "YD_mode"

    df_yeardiff.to_excel(folder + "13.xlsx", index=False)
    print("excel file saved correctly")
    print("")
    
    ### Plot last 50 years difference
    sub_df = df["Years_difference"].value_counts().rename_axis('Year_difference').reset_index(name='Counts')
    sub_df = sub_df.sort_values('Year_difference',ascending=True).head(25)
    sub_df = sub_df.astype(int)
    ax = sub_df.plot.bar(x='Year_difference', y='Counts', rot=70, fontsize = 6)
    ax.figure.savefig(folder + '13.pdf')
    
    ##############################################################################################################
    
    # 14 and 15 - Range of dates based on each article
    print("14 and 15 #####################################################################")
    print("")
    article_df = df.groupby('Accession_Number').agg({'Years_difference': ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: pd.Series.mode(x) if len(pd.Series.mode(x)) <= 1 else "NA"]})
    article_df = article_df.dropna()
    article_df.columns = ['Citations', 'YD_mean', 'YD_median', 'YD_min', 'YD_max', 'YD_std', 'YD_mode']
    article_df["YD_mean_article"] = (article_df["YD_mean"] / len(list(set(list(article_df.index)))))
    
    # Fix problem mode single citations
    article_df.loc[article_df['Citations'] == "1", 'YD_mode'] = 'NA'
    # Fix problem mode more than one equal value
    def clean_mode(x):
        if str(x).find("[") != -1:
            return("NA")
        else:
            return(x)
    article_df['YD_mode'] = article_df['YD_mode'].apply(clean_mode)
    
    # print(article_df.head(n=5))
    print("Average age of citaton based on an average for each article", str(sum(article_df["YD_mean_article"])))
    print("")
    article_df.to_excel(folder + "14_15.xlsx", index=True)
    print("excel file saved correctly")
    print("")
    
    ##############################################################################################################
    
    # 16 - Average age of citation by year of original article publication.
    print("16 ############################################################################")
    print("")
    year_df = df.groupby('Year_Published').agg({'Years_difference': ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: pd.Series.mode(x) if len(pd.Series.mode(x)) <= 1 else "NA"]})
    year_df = year_df.dropna()
    year_df.columns = ['Citations', 'YD_mean', 'YD_median', 'YD_min', 'YD_max', 'YD_std', 'YD_mode']
    
    ### New
    year_df.insert(0, "Publications", 0)
    year_df.insert(2, "Journals", 0)
    
    list_of_years = list(year_df.index)
    for year in list_of_years:
        sub_df = df[df["Year_Published"] == year]
        number_WOS = len(list(set(list(sub_df["Accession_Number"]))))
        number_Journals = len(list(set(list(sub_df["ISSN"]))))
        year_df.loc[year, 'Publications'] = number_WOS
        year_df.loc[year, 'Journals'] = number_Journals
        
    year_df.insert(2, "Ratio C/P", 0)
    year_df["Ratio C/P"] = (round(year_df["Citations"] / year_df["Publications"], 2))
    ###
    
    # Fix problem mode single citations
    year_df.loc[year_df['Citations'] == "1", 'YD_mode'] = 'NA'
    # Fix problem mode more than one equal value
    def clean_mode(x):
        if str(x).find("[") != -1:
            return("NA")
        else:
            return(x)
    year_df['YD_mode'] = year_df['YD_mode'].apply(clean_mode)
    
    ### Save file
    year_df.to_excel(folder + "16.xlsx", index=True)
    print("excel file saved correctly")
    print("")
    
    ### Plot number of articles published by year
    year_df['Year_Published'] = year_df.index
    year_df = year_df[["Year_Published", "Citations"]]
    year_df = year_df.astype(int)
    ax1 = year_df.plot.bar(x='Year_Published', y='Citations', rot=70, fontsize = 6, color = "red")
    ax1.figure.savefig(folder + '16.pdf')
       
    ##############################################################################################################
    
    # 18 The average age of citation based on the journal title of the primary article. 
    # If you publish in Journal A vs. Journal B, would there be an expectation of newer/older 
    # bibliography items in your article? (Question: should we base Journal on ISSN field?)
    print("18 ############################################################################")
    print("")
    journal_df = df.groupby('ISSN').agg({'Years_difference': ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: pd.Series.mode(x) if len(pd.Series.mode(x)) <= 1 else "NA"]}) 
    journal_df = journal_df.dropna()
    journal_df.columns = ['Citations', 'YD_mean', 'YD_median', 'YD_min', 'YD_max', 'YD_std', 'YD_mode']
    journal_df["YD_mean_journal"] = (journal_df["YD_mean"] / len(list(set(list(journal_df.index)))))

    ### New
    journal_df.insert(0, "Publications", 0)
    
    list_of_journals = list(journal_df.index)
    for journal in list_of_journals:
        sub_df = df[df["ISSN"] == journal]
        number_WOS = len(list(set(list(sub_df["Accession_Number"]))))
        journal_df.loc[journal, 'Publications'] = number_WOS
        
    journal_df.insert(2, "Ratio C/P", 0)
    journal_df["Ratio C/P"] = (round(journal_df["Citations"] / journal_df["Publications"], 2))
    ###
    
    # Fix problem mode single citations
    journal_df.loc[journal_df['Citations'] == "1", 'YD_mode'] = 'NA'
    # Fix problem mode more than one equal value
    def clean_mode(x):
        if str(x).find("[") != -1:
            return("NA")
        else:
            return(x)
    journal_df['YD_mode'] = journal_df['YD_mode'].apply(clean_mode)

    ### Save file
    journal_df.to_excel(folder + "18.xlsx", index=True)
    print("excel file saved correctly")
    print("")
    
    ### Plot the top 50 journals with more citations
    journal_df['Journal'] = journal_df.index
    journal_df = journal_df.sort_values('Citations',ascending=False).head(25)
    ax2 = journal_df.plot.bar(x='Journal', y='Citations', rot=90, fontsize = 6, color = "green")
    ax2.figure.savefig(folder + '18.pdf')
    
    ##############################################################################################################
    
    # 19 Review articles vs. original articles -- difference in average age of citations and number of cited items?
    print("19 ############################################################################")
    print("")    
    df.Document_Type = df.Document_Type.apply(lambda x: 'Review' if 'Review' in x else x)
    df.Document_Type = df.Document_Type.apply(lambda x: 'Article' if 'Article' in x else x)
    
    doc_type_df = df.groupby('Document_Type').agg({'Years_difference': ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: pd.Series.mode(x) if len(pd.Series.mode(x)) <= 1 else "NA"]})
    doc_type_df = doc_type_df.dropna()
    doc_type_df.columns = ['Citations', 'YD_mean', 'YD_median', 'YD_min', 'YD_max', 'YD_std', 'YD_mode']
    
    ### New
    doc_type_df.insert(0, "Publications", 0)
    
    list_of_doctypes = list(doc_type_df.index)
    for doctype in list_of_doctypes:
        sub_df = df[df["Document_Type"] == doctype]
        number_WOS = len(list(set(list(sub_df["Accession_Number"]))))
        doc_type_df.loc[doctype, 'Publications'] = number_WOS
        
    doc_type_df.insert(2, "Ratio C/P", 0)
    doc_type_df["Ratio C/P"] = (round(doc_type_df["Citations"] / doc_type_df["Publications"], 2))
    ### 
    
    # Fix problem mode single citations
    doc_type_df.loc[doc_type_df['Citations'] == "1", 'YD_mode'] = 'NA'
    # Fix problem mode more than one equal value
    def clean_mode(x):
        if str(x).find("[") != -1:
            return("NA")
        else:
            return(x)
    doc_type_df['YD_mode'] = doc_type_df['YD_mode'].apply(clean_mode)
    
    # Save file
    doc_type_df.to_excel(folder + "19.xlsx", index=True)
    print("excel file saved correctly")
    print("")
    
    ##############################################################################################################
    
    # 20 - top 10, 25 most frequently cited journals for each institution
    print("20 ############################################################################")
    print("")
    journal_citedref_df = df["Journal_of_cited_article"].value_counts().rename_axis('Journal').reset_index(name='Absolute_freq')
    journal_citedref_df["Relative_freq"] = (journal_citedref_df["Absolute_freq"] / sum(journal_citedref_df["Absolute_freq"]))
    journal_citedref_df["Percent"] = (100 * journal_citedref_df["Absolute_freq"] / sum(journal_citedref_df["Absolute_freq"]))
    journal_citedref_df['Cumulative Frequency'] = journal_citedref_df['Absolute_freq'].cumsum()
    journal_citedref_df.to_excel(folder + "20.xlsx", index=False)
    print("excel file saved correctly")
    print("")
    
    ### Plot the top most frequenctly cited  journals
    journal_citedref_df = journal_citedref_df.sort_values('Absolute_freq',ascending=False).head(25)
    ax3 = journal_citedref_df.plot.bar(x='Journal', y='Absolute_freq', rot=90, fontsize = 5, color = "orange")
    ax3.figure.savefig(folder + '20.pdf')
    
    ##############################################################################################################
    
    # # 21 - Which journal has the largest difference between lowest Age Difference and highest Age Difference
    # print("21 ############################################################################")
    # print("")
    # ### cited ref 
    # journal_differences_citedref_df = df.groupby('Journal_of_cited_article').agg({'Years_difference': ['count', 'mean', 'median', 'min', 'max', 'std', lambda x: pd.Series.mode(x) if len(pd.Series.mode(x)) <= 1 else "NA"]})
    # journal_differences_citedref_df.columns = ['Citations', 'YD_mean', 'YD_median', 'YD_min', 'YD_max', 'YD_std', 'YD_mode']
    # ### New
    # journal_differences_citedref_df.insert(0, "Publications", 0)
    
    # list_of_cited_journals = list(journal_differences_citedref_df.index)
    # for cited_journal in list_of_cited_journals:
    #     sub_df = df[df["Journal_of_cited_article"] == cited_journal]
    #     number_WOS = len(list(set(list(sub_df["Accession_Number"]))))
    #     journal_differences_citedref_df.loc[cited_journal, 'Publications'] = number_WOS
        
    # journal_differences_citedref_df.insert(2, "Ratio C/P", 0)
    # journal_differences_citedref_df["Ratio C/P"] = (round(journal_differences_citedref_df["Citations"] / journal_differences_citedref_df["Publications"], 2))
    # ### 

    # # Fix problem mode single citations
    # journal_differences_citedref_df.loc[journal_differences_citedref_df['Citations'] == "1", 'YD_mode'] = 'NA'
    
    # # Fix problem mode more than one equal value
    # def clean_mode(x):
    #     if str(x).find("[") != -1:
    #         return("NA")
    #     else:
    #         return(x)
    # journal_differences_citedref_df['YD_mode'] = journal_differences_citedref_df['YD_mode'].apply(clean_mode)
 
    # ### Save file
    # journal_differences_citedref_df.to_excel(folder + "21.xlsx", index=True)
    # print("excel file saved correctly")
    # print("")
    
    # ##############################################################################################################
    
    # # 22 - What is the title range of journals published in by an UNIGE or IARC vs. the title range of cited items? 
    # # For instance IARC published in XXX titles for a certain period. The corresponding cited/bibliography items 
    # # encompassed XXX number of titles.
    # print("22 ############################################################################")
    # print("")
    # unique_journals_original = len(list(set(list(df["ISSN"]))))
    # unique_journals_cited = len(list(set(list(df["Journal_of_cited_article"]))))
    # print("Number of unique journals in primary article: ", unique_journals_original)
    # print("Number of unique journals in cited article:   ", unique_journals_cited)
    # del(unique_journals_original); del(unique_journals_cited)
    
    # 23 - New suggestion, mean delay between publication date of cited ref and citing article, per journal

##################################################################################################################
##################################################################################################################

### IARC
folder_IARC = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//"
file_name_IARC = "IARC_WoS.csv"
df_IARC = calculations_WoS(file_name_IARC, folder_IARC, 2001, 2020)
del(folder_IARC); del(file_name_IARC)
### UNIGE
folder_UNIGE = "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//"
file_name_UNIGE = "UNIGE_WoS.csv"
df_UNIGE = calculations_WoS(file_name_UNIGE, folder_UNIGE, 2001, 2020)
del(folder_UNIGE); del(file_name_UNIGE)

##################################################################################################################
##################################################################################################################
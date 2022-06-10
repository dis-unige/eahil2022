# -*- coding: utf-8 -*-

#######################################################################################################################
#######################################################################################################################

def parse_WoS(input_directory, output_directory, output_file):
    
    # import modules
    import pandas as pd
    import os
    import re
    import math
    
    # Change working directory
    os.chdir(input_directory)
    os.getcwd()
    
    # read file names with txt extension
    list_of_txt_files = []
    for file in os.listdir():
        if file.endswith(".txt"):
            list_of_txt_files.append(file)
            
    # Sort Strings on numerical substrings
    list_of_txt_files.sort(key=lambda list_of_txt_files : list(map(int, re.findall(r'\d+', list_of_txt_files)))[0])
    # print(len(list_of_txt_files))
    # print(list_of_txt_files)
    
    # loop files in the directory
    list_of_dfs = []
    for file in list_of_txt_files:
        
        # read file
        target_df = pd.read_csv(file, sep='\t', lineterminator='\r', index_col=False, skip_blank_lines=True)
        
        # remove nan rows
        target_df.drop(target_df.tail(1).index,inplace=True)
        
        # add df to list of df
        list_of_dfs.append(target_df)
        
    del(file); del(target_df); del(list_of_txt_files)    
        
    # concatenate all df
    df_concatenated = pd.concat(list_of_dfs)
    # print(df_concatenated.shape)
    # print(len(list(set(df_concatenated["UT"]))))

    # remove duplicates
    df_concatenated = df_concatenated.drop_duplicates(keep="last")
    df_concatenated = df_concatenated.reset_index(drop=True)
    # print(print(df_concatenated.shape))
    # print(len(list(set(df_concatenated["UT"]))))
    # return(df_concatenated)
    
    #######################################################################################################################
    #######################################################################################################################
    
    def create_dataframe(df):
        
        # Get all the data from the columns (source: https://images.webofknowledge.com/images/help/WOS/hs_wos_fieldtags.html)
        # Main reference
        column_ID = list(df.index) # Custom ID
        column_WOS = list(df["UT"]) # Accession Number
        column_PY = list(df["PY"]) # Year Published
        column_LA = list(df["LA"]) # Language
        column_DT = list(df["DT"]) # Document Type
        column_PT = list(df["PT"]) # Publication Type (J=Journal; B=Book; S=Series; P=Patent)
        column_TI = list(df["TI"]) # Document Title
        column_SO = list(df["SO"]) # Publication Name
        column_PU = list(df["PU"]) # Publisher
        column_SN = list(df["SN"]) # International Standard Serial Number (ISSN)
        column_EI = list(df["EI"]) # Electronic International Standard Serial Number (eISSN)
        column_BN = list(df["BN"]) # International Standard Book Number (ISBN)
        column_J9 = list(df["J9"]) # 29-Character Source Abbreviation
        column_JI = list(df["JI"]) # ISO Source Abbreviation
        column_VL = list(df["VL"]) # Volume
        column_IS = list(df["IS"]) # Issue
        column_SU = list(df["SU"]) # Supplement
        column_BP = list(df["BP"]) # Beginning Page
        column_EP = list(df["EP"]) # Ending Page
        column_AR = list(df["AR"]) # Article Number
        column_DI = list(df["DI"]) # Digital Object Identifier (DOI)
        column_D2 = list(df["D2"]) # Book Digital Object Identifier (DOI)
        column_PG = list(df["PG"]) # Page Count
        column_WC = list(df["WC"]) # Web of Science Categories
        column_WE = list(df["WE"]) # Web of Science Index
        column_SC = list(df["SC"]) # Research Areas
        column_PM = list(df["PM"]) # PubMed ID
        column_OA = list(df["OA"]) # Open Access Indicator
        column_HC = list(df["HC"]) # ESI Highly Cited Paper. Note that this field is valued only for ESI subscribers.
        column_HP = list(df["HP"]) # ESI Hot Paper. Note that this field is valued only for ESI subscribers.
        column_DA = list(df["DA"]) # Date this report was generated.    
        column_TC = list(df["TC"]) # Web of Science Core Collection Times Cited Count
        column_Z9 = list(df["Z9"]) # Total Times Cited Count (Web of Science Core Collection, Arabic Citation Index, BIOSIS Citation Index, Chinese Science Citation Database, Data Citation Index, Russian Science Citation Index, SciELO Citation Index)
            
        # Cited references
        column_CR = list(df["CR"]) # Cited References
        column_NR = list(df["NR"]) # Cited Reference Count
    
        # length df rows 
        length_df_rows = df.shape[0]
        
        # Create variable for all dataframe rows
        dataframe_rows = []
        
        # Add columns    
        dataframe_rows.append(["ID",
                            "Accession Number",                  # UT
                            "Year Published",                       # PY
                            "Language",                             # LA
                            "Document Type",                        # DT
                            "Publication Type",                     # PT
                            "Document Title",                       # TI
                            "Publication Name",                     # SO
                            "Publisher",                            # PU
                            "ISSN",                                 # SN
                            "eISSN",                                # EI
                            "ISBN",                                 # BN
                            "29 Character Source Abbreviation",     # J9
                            "ISO Source Abbreviation",              # JI
                            "Volume",                               # VL
                            "Issue",                                # IS
                            "Supplement",                           # SU
                            "Beginning Page",                       # BP
                            "Ending Page",                          # EP
                            "Article Number",                       # AR
                            "DOI",                                  # DI
                            "Book DOI",                             # D2
                            "Page Count",                           # PG
                            "Web of Science Categories",            # WC
                            "Web of Science Index",                 # WE
                            "Research Areas",                       # SC
                            "PubMed ID",                            # PM
                            "Open Access Indicator",                # OA
                            "ESI Highly Cited Paper",               # HC
                            "ESI Hot Paper",                        # HP
                            "Date of report",                       # DA
                            "WoS  Core Collection Times Cited Count",# TC
                            "Total Times Cited Count",              # Z9
                            "Author of cited article",              # New columns generated on the script
                            "Year of cited article",                #
                            "Journal of cited article",             #
                            "Years difference",                     #
                            "DOI of cited article",                  #
                            "Need to be checked"])                  # New columns generated on the script
        # print(len(dataframe_rows[0]))
        
        # loop all df rows
        no_cited_articles = 0
        yes_cited_articles = 0
        wrong_articles = 0
        # need_to_be_checked = 0
        
        for x in range(0, length_df_rows):
            
            # ID
            ID = column_ID[x]
             
            # Accession Number
            WOS = column_WOS[x]
            if type(WOS) != str:
                if math.isnan(WOS) == True:
                    WOS = "Empty"
                if type(WOS) != str and WOS != "Empty":
                    WOS = str(WOS)
            if type(WOS) == str:
                if WOS != "Empty":
                    WOS = str(WOS)
                    WOS = WOS.lstrip()
                
            # Year Published
            PY = column_PY[x]
            if math.isnan(PY) == False:
                PY = int(PY)
            if math.isnan(PY) == True:
                PY = 0

            # Language
            LA = column_LA[x]
            LA = str(LA)
            
            # Document Type
            DT = column_DT[x]
            DT = str(DT)
            
            # Publication Type (J=Journal; B=Book; S=Series; P=Patent)
            PT = column_PT[x]
            PT = str(PT)
            
            # Document Title
            TI = column_TI[x]
            TI = str(TI)
            
            # Publication Name
            SO = column_SO[x]
            SO = str(SO)
            
            # Publisher
            PU = column_PU[x]
            PU = str(PU)
            
            # International Standard Serial Number (ISSN)
            SN = column_SN[x]
            SN = str(SN)
            
            # Electronic International Standard Serial Number (eISSN)
            EI = column_EI[x]
            EI = str(EI)
            
            # International Standard Book Number (ISBN)
            BN = column_BN[x]
            BN = str(BN)
            
            # 29-Character Source Abbreviation
            J9 = column_J9[x]
            J9 = str(J9)
            
            # ISO Source Abbreviation
            JI = column_JI[x]
            JI = str(JI)
            
            # Volume
            VL = column_VL[x]
            VL = str(VL)
            
            # Issue
            IS = column_IS[x]
            IS = str(IS)
            
            # Supplement
            SU = column_SU[x]
            SU = str(SU)
            
            # Beginning Page
            BP = column_BP[x]
            BP = str(BP)
            
            # Ending Page
            EP = column_EP[x]
            EP = str(EP)
            
            # Article Number
            AR = column_AR[x]
            AR = str(AR)
            
            # Digital Object Identifier (DOI)
            DI = column_DI[x]
            DI = str(DI)
            
            # Book Digital Object Identifier (DOI)
            D2 = column_D2[x]
            D2 = str(D2)
            
            # Page Count
            PG = column_PG[x]
            PG = str(PG)
            
            # Web of Science Categories
            WC = column_WC[x]
            WC = str(WC)
            
            # Web of Science Index
            WE = column_WE[x]
            WE = str(WE)
            
            # Research Areas
            SC = column_SC[x]
            SC = str(SC)
            
            # PubMed ID
            PM = column_PM[x]
            PM = str(PM)
    
            # Open Access Indicator
            OA = column_OA[x]
            OA = str(OA)
            
            # ESI Highly Cited Paper
            HC = column_HC[x]
            HC = str(HC)
            
            # ESI Hot Paper
            HP = column_HP[x]
            HP = str(HP)
            
            # Date this report was generated.    
            DA = column_DA[x]
            DA = str(DA)
            
            # Web of Science Core Collection Times Cited Count  
            TC = column_TC[x]
            TC = int(TC)
            
            # Total Times Cited Count   
            Z9 = column_Z9[x]
            Z9 = int(Z9)
                
            # cited references
            cited_articles = column_CR[x]
            try:
                number_of_articles = float(column_NR[x])
            except:
                number_of_articles = 0
            
            # Control for wrong articles
            if WOS == "Empty" or PY == 0:
                # need_to_be_checked = need_to_be_checked + 1
                wrong_articles = wrong_articles + 1
                
                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                            BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                            D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                            TC, Z9,
                            "", 
                            "", 
                            "", 
                            "",
                            "",
                            "Yes"]
                # add row
                dataframe_rows.append(row)
                
            if WOS != "Empty" and PY != 0:                                              
                # control for empty cited references
                if number_of_articles <= 0:
                    no_cited_articles = no_cited_articles + 1
                    # need_to_be_checked = need_to_be_checked + 1
                    
                    row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                            BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                            D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                            TC, Z9,
                                "", 
                                "", 
                                "", 
                                "",
                                "",
                                "Yes"]                    
                    # add row
                    dataframe_rows.append(row)
                
                if number_of_articles > 0:
                    yes_cited_articles = yes_cited_articles + 1
                
                    # loop all cited articles
                    cited_articles = column_CR[x]
                    cited_articles = cited_articles.split(";")
                    
                    for article in cited_articles:

                        article_list = article.split(", ")
                        
                        if len(article_list) < 3:
                            # row values
                            row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                    BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                    D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                    TC, Z9,
                                    article_list, 
                                    "", 
                                    "", 
                                    "", 
                                    "",
                                    "Yes"]
                            # need_to_be_checked = need_to_be_checked + 1
                            
                        if len(article_list) == 3:
                            try:
                                cited_article_author = article_list[0].lstrip()
                                cited_article_year = int(article_list[1].lstrip())
                                cited_article_journal = article_list[2].lstrip()
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        cited_article_author, 
                                        cited_article_year, 
                                        cited_article_journal, 
                                        PY - cited_article_year, 
                                        "",
                                        "No"]
                            except:
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        article_list, 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "Yes"]
                                # need_to_be_checked = need_to_be_checked + 1
                            
                        if len(article_list) == 4:
                            try:
                                cited_article_author = article_list[0].lstrip()
                                cited_article_year = int(article_list[1].lstrip())
                                cited_article_journal = article_list[2].lstrip()
                                # check if doi in last position
                                if article_list[-1].find("DOI") != -1:
                                    cited_article_doi = article_list[-1].lstrip()
                                    cited_article_doi = cited_article_doi.replace("DOI ","")
                                    # row values
                                    row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                            BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                            D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                            TC, Z9,
                                            cited_article_author, 
                                            cited_article_year, 
                                            cited_article_journal, 
                                            PY - cited_article_year,
                                            cited_article_doi,
                                            "No"]
                                if article_list[-1].find("DOI") == -1:
                                    # row values
                                    row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                            BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                            D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                            TC, Z9,
                                            cited_article_author, 
                                            cited_article_year, 
                                            cited_article_journal, 
                                            PY - cited_article_year, 
                                            "",
                                            "No"]
                            except:
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        article_list, 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "Yes"]
                                # need_to_be_checked =  + 1
                                
                        if len(article_list) == 5:
                            try:
                                cited_article_author = article_list[0].lstrip()
                                cited_article_year = int(article_list[1].lstrip())
                                cited_article_journal = article_list[2].lstrip()
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        cited_article_author, 
                                        cited_article_year, 
                                        cited_article_journal, 
                                        PY - cited_article_year, 
                                        "",
                                        "No"]
                            except:
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        article_list, 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "Yes"]
                                
                        if len(article_list) == 6:
                            try:
                                cited_article_author = article_list[0].lstrip()
                                cited_article_year = int(article_list[1].lstrip())
                                cited_article_journal = article_list[2].lstrip()
                                cited_article_doi = article_list[5].lstrip()
                                cited_article_doi = cited_article_doi.replace("DOI ","")
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        cited_article_author, 
                                        cited_article_year, 
                                        cited_article_journal, 
                                        PY - cited_article_year,
                                        cited_article_doi,
                                        "No"]
                            except:
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        article_list, 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "Yes"]
                                #  =  + 1
                                 
                        if len(article_list) >= 7:
                            try:
                                cited_article_author = article_list[0].lstrip()
                                cited_article_year = int(article_list[1].lstrip())
                                cited_article_journal = article_list[2].lstrip()
                                
                                for pos in range(0, len(article_list)):
                                    if article_list[pos].find("DOI") != -1:
                                        cited_article_doi = article_list[pos:]
                                        cited_article_doi = ", ".join(cited_article_doi)
                                        cited_article_doi = cited_article_doi.replace("DOI ", "")
                                        # row values
                                        row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                                BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                                D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                                TC, Z9,
                                                cited_article_author, 
                                                cited_article_year, 
                                                cited_article_journal, 
                                                PY - cited_article_year,
                                                cited_article_doi,
                                                "No"]
                                        break
                                    
                                    if pos == len(article_list) and article_list[pos].find("DOI") == -1:                                         
                                        row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                                BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                                D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                                TC, Z9,
                                                cited_article_author, 
                                                cited_article_year, 
                                                cited_article_journal, 
                                                PY - cited_article_year,
                                                "",
                                                "No"]
                            except:
                                # row values
                                row = [ID, WOS, PY, LA, DT, PT, TI, SO, PU, SN, EI, 
                                        BN, J9, JI, VL, IS, SU, BP, EP, AR, DI,
                                        D2, PG, WC, WE, SC, PM, OA, HC, HP, DA,
                                        TC, Z9,
                                        article_list, 
                                        "", 
                                        "", 
                                        "", 
                                        "",
                                        "Yes"]
                                #  =  + 1
                                                 
                        # add row
                        dataframe_rows.append(row)
                    
        ########################
        
        df_final = pd.DataFrame(dataframe_rows[1:], columns = dataframe_rows[0])
        
        control1 = df.shape[0] == (no_cited_articles + yes_cited_articles + wrong_articles)
        control2 = (df_final[df_final["Need to be checked"] == "Yes"].shape[0] + df_final[df_final["Need to be checked"] == "No"].shape[0]) == df_final.shape[0]
    
        # Write a report
        report_lines = ["PARSING REPORT",
                 "",            
                 "Number of articles retrieved from WoS:             " + str(df.shape[0]),
                 "Articles without cited articles:                   " + str(no_cited_articles),
                 "Articles with cited articles:                      " + str(yes_cited_articles),
                 "Articles with a not accessible format:             " + str(wrong_articles),
                 "",
                 "Cited references that don't need human revision:   " + str(df_final[df_final["Need to be checked"] == "No"].shape[0]) + " (" + str(round(df_final['Need to be checked'].value_counts(normalize=True)[0], 2)*100) + "%)",
                 "Cited references that need human revision:         " + str(df_final[df_final["Need to be checked"] == "Yes"].shape[0]) + " (" + str(round(df_final['Need to be checked'].value_counts(normalize=True)[1], 2)*100) + "%)",
                 "",
                 "Control of complete parsing 1:                     " + str(control1),
                 "Control of complete parsing 2:                     " + str(control2)]
        report_file = output_directory + 'Parsing_report.txt'
        with open(report_file, 'w') as f:
            for line in report_lines:
                f.write(line)
                f.write('\n')
        
        return(df_final)
    
    ###################################################################################################################
    ###################################################################################################################

    # Generate df
    df_clean = create_dataframe(df_concatenated)
       
    # Save df
    df_clean.to_csv(output_directory + "//" + output_file + ".csv", index=False, sep=",", chunksize=10000)
    print("csv file saved correctly")
    
    return(df_clean)

#######################################################################################################################
#######################################################################################################################

# Get tables
df_IARC = parse_WoS("C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//WoS raw text files//sources//",
                    "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//IARC data and calculations 2001_2020//",
                    "IARC_WoS")

df_UNIGE = parse_WoS("C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//sources",
                     "C://Users//ciercor//OneDrive - IARC//EAHIL 2022 proposal//UNIGE data and calculations 2001_2020//",
                     "UNIGE_Wos")

#######################################################################################################################
#######################################################################################################################

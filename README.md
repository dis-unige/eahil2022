
# EAHIL 2022

Repository to share code and data used for the study presented at the EAHIL 2022 conference (https://eahil2022.nl)

## Title: Computational assistance in the analysis of cited references in biomedical literature: a case study from two institutions.

## Authors
 * Teresa Lee, Knowledge Manager, International Agency for Research on Cancer (IARC/WHO) LeeT@iarc.fr  
 * Pablo Iriarte, IT Coordinator, Library of the University of Geneva Pablo.Iriarte@unige.ch 
 * Floriane Muller, Librarian (Medical Library), Library of the University of Geneva Floriane.Muller@unige.ch  
 * Ramon Cierco Jimenez, Doctoral Student, International Agency for Research on Cancer (IARC/WHO) CiercoR@iarc.fr  

## Introduction 

At Institution A, a building move in 2022 requires a 40% reduction of its physical collection and a weeding strategy for the library’s print journals. From this scenario a question emerges: how old, on average, is the literature cited by in-house scientists in their own publications? According to Kaplan et al.  recent materials are accessed more frequently than older ones, with a significant drop for anything older than 15 years. In this project, we empirically test this assertion using computational assistance. Institution A’s librarian teamed up with a doctoral student in bioinformatics to parse citations retrieved from Web of Science based on an OG (enhanced organization) field search. University of B collaborators joined the experimental effort to test not only Kaplan et al.’s rule1, but to interrogate the dataset in ways that may shed light on historic citation trends, open-access and the electronic availability of research literature, the lasting prominence of super-cited references, and more. 

## Aim  

 * To build a librarian-friendly utility for the parsing of Web of Science records that allows analysis of the cited items associated with the primary set of records. 
 * To see whether the 15-year rule for cited literature holds true of the article outputs of Institution A and the University of B’s biomedical faculty.  
 * To ascertain what other findings regarding historical citation trends, open-access and the electronic availability of literature arise from an experimental parsing and interrogation of the dataset resulting from Web of Science affiliation-based searches. 

## Methods 

Sets of records based on OG (enhanced organization) field searches for the University of B and for Institution A will be retrieved and parsed using Python or R. A methodology for cleaning up the parsed set of records will be determined, implemented, and reported. Parsed and cleaned data from this initial process will be correlated with data from other sources of information (for e.g., CrossRef) to find answers to questions that go beyond what analysing Web of Science records alone can provide.  

## Research questions to tackle 
We listed and numbered questions we thought would be interesting to tackle, and after a selection phase, ended up with the following list:
- n°13 STRAIGHT AVERAGE: Average age of citations (years difference) as global average. Does 15-year rule hold? Add all of the Years Difference and divide by total number of cited items. 
- n°14 ARTICLE-NORMALIZED AVERAGE: Average age of citation based on an average for each article. Take the average years difference for each article, and then divide the total by the number of primary items/articles.
- n°15 Range of dates based on each article. For each primary article (i.e. same WoS accession number), what is the lowest Year Difference, the highest Years Difference, and then the Highest minus Lowest? Also, what is the MODE, standard deviation?
- n°16 AVERAGE YEARS DIFFERENCE, SEGMENTED BY YEAR OF ORIGINAL PUBLICATION: Average age of citation by year of original article publication. Is there a trend towards citing more and more recent papers? If we look at each year's articles as a set, for example 2018, what is the average Years Difference?
- n°18 ORIGINATING JOURNAL TITLE-NORMALIZED AVERAGE YEARS DIFFERENCE: The average age of citation based on the journal title of the primary article. Related question is: If you publish in Journal A vs. Journal B, would there be an expectation of newer/older bibliography items in your article? 
- n°19: DATA BY PUBLICATION TYPE: Review articles vs. original articles -- difference in average age of citations and number of cited items?
- n°20: Absolute and relative frequency by cited journal title + cumulative frequency. Top 10, 25 most frequently cited journals for each institution.
- n°21: Cited journals with the largest age ranges. Correlation with the top 10, 25 journals list. (Which journal has the largest difference between lowest Age Difference and highest Age Difference?)
- n°22: What is the title range of journals published in by an institution vs. the title range of cited items? For instance, institution A published in XXX titles (number of unique ISSNs) for a certain period. The corresponding cited/bibliography items encompassed XXX number of titles (number of unique journal abbreviations).
- n°25: Within the cited articles, what proportion exist in digital form (or at least have a DOI). Does it evolve with time?
- n°26: Self citation at the institutional level: which articles DOIs are present both in the original publication corpus and the citations corpus? What percentage of the publications/citations does it represent?
- n°27: Within the citing and cited articles, what proportion are Open Access (OA)? Does it evolve with time? Do article that are themselves OA cite more OA journals than articles that are not OA?

## Output files 
The files/figures produced by the scripts and notebooks bear the same number that the one of the question their contents should help tackle.
This means looking at the data with a few different perspectives.
- BY CITED JOURNAL	# 20, 21, 22
- BY CITING JOURNAL 	# 18, 22
- BY PUBLICATION TYPE	# 19
- BY YEAR OF ORIGINAL PUBLICATION	#16, 25, 27
- BY CITING ARTICLE 	#14, 15, 25, 26, 27
- BY CITED ARTICLE	#26, 27
- BY UNIQUE DOI 	#25, 26, 27
- BY OPEN ACCESS STATUS & COLOR	#27

## Results 

- The 15-year rule holds
- Authors are citing more papers & older papers 
- Articles have DOIs more often 
- Citations have DOIs more often too (but still less often than publications)
- Open Access is increasing
- OA publications tend to cite more OA papers
- Institutions cite themselves often, but maybe even more often if they are specialized in a narrow field of research

## References 

 * Kaplan R, Steinberg M, Doucette J. Retention of retrospective print journals in the digital age: trends and analysis. J Med Libr Assoc. 2006;94(4):387-e200. 
 * Van Rossum, G., & Drake Jr, F. L. (1995). Python reference manual. Centrum voor Wiskunde en Informatica Amsterdam. 
 * R Core Team (2021). R: A language and environment for statistical  computing. R Foundation for Statistical Computing, Vienna, Austria. URL https://www.R-project.org/. 


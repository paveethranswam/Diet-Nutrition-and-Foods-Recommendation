# Diet-Nutrition-and-Foods-recommendation-for-Cancer-Patients-and-extend-this-to-build-as-application
To deliver high level research in two directions, named statistical analysis of molecular omics data and nature language processing analysis of literature data. Need to develop new mathematical models and computational approaches to integrate the findings from the two data sources. The expected deliverables include (1) new computational model, (2) inference of highly explainable dependencies among biological or biomedical features.

## Metabolism and nutrients and drug recommendation
1. Drug recommendation and repurposing (a warnup topic)
For a given patient with some features, can we recommend the best therapeutic strategy for this patient? A lot of recommendations are based on association analysis (note, associate does not mean for casual relations). A lot of unsolved things in providing explainable recommendations.
2. Nutrients and Diet recommendations
Examples, 2.1 People who want to boost their muscles.  Can we recommend some nutrients or more exactly, protein and other carbon sources, to optimize muscle growth, for different clients? (1). NLP on literature, (2). Mouse or human molecular data of samples have taken different diets and have different outcomes in terms of muscle growth (limited public data), (3). we can collect some blood samples locally, (4). personal wearable devices (sensors).
A more straightforward example: A person who has breast cancer and just has done neoadjuvant chemotherapy and surgical removal. She asked us for some recommendations of food. How can we make some recommendations? 1. NLP, a list of nutrients, a list of foods, and the unit level of different nutrients in each type of food -> NLP on pubmed papers/abstracts to if some nutrients can have a positive or negative effect on breast cancer cells. 2 We have a lot of breast cancer patient data, with prognosis, and by using the metabolic analysis we have developed, we can predict which nutrients have good or bad effect to the cancer patients.
3. Knowledge graph construction
A heterogenous graph representation of biological functions and relations. 
Step 1. Derive a graph-based representation of explainable biological relations from omics data.
Step 2. Align the term  "explainable biological relations " derived from data with the reports from the literature.
Step 3. We know a lot of patterns conceived in the omics data were not reported, can we use AI to generate biological stories (i.e biological relations) for these unreported patterns.![image](https://user-images.githubusercontent.com/90008433/190922937-6e11fbd1-93dc-4ef6-b9fd-7a8d64712cc2.png)

## Current Progress:
▪ Delivered high-level research in statistical analysis of molecular omics data and natural language processing analysis of literature data to infer highly explainable dependencies among biomedical features.
▪ Improved the efficiency of abstract-mining operation by developing rigorous pattern matching program using NLTK and Regex in Python
▪ Working on constructing a Knowledge-Graph by integrating findings from various data sources using BERT and unsupervised classification, which is directly used for nutrients-diet recommendations for diseased patients.
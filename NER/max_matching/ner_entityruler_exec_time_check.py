# #!/usr/bin/env python
# # coding: utf-8

"""
Old codes last updated Jan 28

# import spacy
# from spacy.lang.en import English 
# from spacy.tokens import Doc
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import time
# import os

# metabolite_file = '/N/u/paswam/Carbonate/Desktop/Link to Pavi/KD-DocRE/hmdb_mDivided.csv'
# met_lib = pd.read_csv(metabolite_file)
# print(met_lib.shape)
# # 200000 rows

# # Need to remove that b character (represents bytes but it is string here in df) from iupac_name and name
# metabolites_patterns = []
# record_per_word_times = []
# total_entries = 20000  # Change values and try which works (tried till 50k, can try more than that) # For full use len(met_lib)

# # For each value in metabolite library, decode it and then add to patterns 
#   # While adding to patterns, aplit the full word on all special characters and each word put as {LOWER: that_word} for every full word
# total_words_start_time = time.time()
# for i in range(total_entries):
#     try:
#         start_time = time.time()
#         # Clean text, remove 'b' from the beginning of string
#         full_name = met_lib.iloc[i]['name'].strip("b\'\"")
#         full_name_decoded = full_name.encode().decode() # \u2019 - ' urindine
#         id_name = full_name_decoded
        
#         # Have the original name as a pattern for exact match of main name, so process the word also
#         full_name_spaced = ''.join((' {} '.format(el.lower()) if not el.isalnum() and not el.isspace() else el for el in full_name_decoded))
#         full_name_list = full_name_spaced.split()
#         add_split_pattern = []
    
#         for split_word in full_name_list:
#             add_split_pattern.append({"LOWER": str(split_word.lower())}) # The first lower did not work
        
#         metabolites_patterns.append({"label": "Metabolites", "pattern": add_split_pattern, "id": id_name })

#         # IUPAC Names has \xc2\\xb2,\\xe2\\x81\\xb7.0\\xc2\\xb9\\xc2\\xb9,\\xc2\\xb9\\x characters
#         # Check if this is correct format
#         # iupac = met_lib.iloc[i]['iupac_name'].strip("b\'\"")
        
#         # There are many metabolites with nan synonyms, so ignore them
#         if(str(met_lib.iloc[i]['synonym']) != 'nan' ):
            
#             # Need to split synonym - delim is : character
#             syn_list = met_lib.iloc[i]['synonym'].split(':')
            
#             # Fixing issue of synonyms being just numbers. 
#             # Solution is to filter and check if a name contains only numbers (isnumeric), if so then do not include in patterns file.
#             syn_list = [item for item in syn_list if not item.isnumeric()] # This greater than 1 condition to avoid single alphabets
#             for syn in syn_list:
#                 # Doing encode.decode even on normal strings does not affect anything, but helps with strings having unicode characters
#                 syn_decoded = syn.encode().decode()
#                 syn_spaced = ''.join((' {} '.format(el.lower()) if not el.isalnum() and not el.isspace() else el for el in syn_decoded))

#                 # Having double spaces also does not affect as .split() removes any word between any number of spaces
#                 syn_list = syn_spaced.split()
#                 add_split_pattern = []
            
#                 for split_word in syn_list:
#                     add_split_pattern.append({"LOWER": str(split_word.lower())}) # The first lower did not work
#                 # if((add_split_pattern[0]['LOWER'] == "as") and (len(add_split_pattern)==1) ):
#                 #     print('werid', add_split_pattern, met_lib.iloc[i]['synonym'], full_name)

#                 metabolites_patterns.append({"label": "Metabolites", "pattern": add_split_pattern, "id": id_name })

#         record_per_word_times.append(round(time.time() - start_time, 5))
#     except Exception as e:
#         print('Exception at', i,  'as ', e)

# total_words_end_time = round(time.time() - total_words_start_time, 5)  
# print('Total entries in Metabolite Patterns file ', len(metabolites_patterns)) 

# # print("--- %s seconds ---" % (time.time() - start_time))


# nlp = None
# nlp = English()
# ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"}) #can only work for non-token pattern
# record_ruler_add_times = 0
# start_time = time.time()
# with nlp.select_pipes(enable="tagger"):
#     ruler.add_patterns(metabolites_patterns)
# record_ruler_add_times = round(time.time() - start_time, 5)
# # print("--- %s seconds ---" % (time.time() - start_time))

# # ruler.to_disk("patterns_spaced.jsonl")
# # ruler.from_disk("patterns_spaced.jsonl")
# print('Adding to ruler done')

# # Now we have the pattern ruler ready, run on one abstract
# # Now preprocessing on abstracts (including unicode character removal) - IS THIS STEP NECESSARY BECAUSE IT SEEMS LIKE ABSTRACTS ALREADY HAVE SPACED WORDS (NOT SURE 
# # IF THIS APPLIES TO ALL ABSTRACTS )
# record_per_abstract_times = []
# record_per_abstract_length = []

# # What is the basis we choose abstracts - do we take on of A list?

# sample_abstracts = ["Uridine 5 ' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides .UDP - glucuronic acid is also a sugar donor for the glycosylation of various plant specialized metabolites .Nevertheless , the roles of UGDs in plant specialized metabolism remain poorly understood .Glycyrrhiza species ( licorice ) , which are medicinal legumes , biosynthesize triterpenoid saponins , soyasaponins and glycyrrhizin , commonly glucuronosylated at the C - 3 position of the triterpenoid scaffold .",
# "Uridine diphosphate glycosyltransferases (UGTs) are the key enzymes in glycosylation processes for decorating plant natural products with sugars. Crystallography, one of the powerful techniques for determining protein structures, was used as the main experimental technique and combined with biochemical methods to study the structure-function relationship and molecular mechanisms of UGTs. Crystal structures of plant UGTs have revealed their exquisite architectures and provided the structural basis for understanding their catalytic mechanism and substrate specificity. In this chapter, some protocols and experimental details of all key stages of protein structure determination are provided, and the structural insights on plant UGTs are also highlighted in combination of method description.",
# "Lung cancer (LC) is the second most common cause of death in men after prostate cancer, and the third most recurrent type of tumor in women after breast and colon cancers. Unfortunately, when LC symptoms begin to appear, the disease is already in an advanced stage and the survival rate only reaches 2%. Thus, there is an urgent need for early diagnosis of LC using specific biomarkers, as well as effective therapies and strategies against LC. On the other hand, the influence of metals on more than 50% of proteins is responsible for their catalytic properties or structure, and their presence in molecules is determined in many cases by the genome. Research has shown that redox metal dysregulation could be the basis for the onset and progression of LC disease. Moreover, metals can interact between them through antagonistic, synergistic and competitive mechanisms, and for this reason metals ratios and correlations in LC should be explored. One of the most studied antagonists against the toxic action of metals is selenium, which plays key roles in medicine, especially related to selenoproteins. The study of potential biomarkers able to diagnose the disease in early stage is conditioned by the development of new analytical methodologies. In this sense, omic methodologies like metallomics, proteomics and metabolomics can greatly assist in the discovery of biomarkers for LC early diagnosis.",
# "Omega-3 polyunsaturated fatty acid (ω-3 PUFA) supplements for chemoprevention of different types of cancer including lung cancer has been investigated in recent years. ω-3 PUFAs are considered immunonutrients, commonly used in the nutritional therapy of cancer patients. ω-3 PUFAs play essential roles in cell signaling and in cell structure and fluidity of membranes. They participate in the resolution of inflammation and have anti-inflammatory effects. Lung cancer patients suffer complications, such as anorexia-cachexia syndrome, pain and depression. The European Society for Clinical Nutrition and Metabolism (ESPEN) 2017 guidelines for cancer patients only discuss the use of ω-3 PUFAs for cancer-cachexia treatment, leaving aside other cancer-related complications that could potentially be managed by ω-3 PUFAs. This review aims to elucidate whether the effects of ω-3 PUFAs in lung cancer is supplementary, pharmacological or both. In addition, clinical studies, evidence in cell lines and animal models suggest how ω-3 PUFAs induce anticancer effects. ω-3 PUFAs and their metabolites are suggested to modulate pivotal pathways underlying the progression or complications of lung cancer, indicating that this is a promising field to be explored. Further investigation is still required to analyze the benefits of ω-3 PUFAs as supplementation or pharmacological treatment in lung cancer.",
# "A causal association has been established between alcohol consumption and cancers of the oral cavity, pharynx, larynx, oesophagus, liver, colon, rectum, and, in women, breast; an association is suspected for cancers of the pancreas and lung. Evidence suggests that the effect of alcohol is modulated by polymorphisms in genes encoding enzymes for ethanol metabolism (eg, alcohol dehydrogenases, aldehyde dehydrogenases, and cytochrome P450 2E1), folate metabolism, and DNA repair. The mechanisms by which alcohol consumption exerts its carcinogenic effect have not been defined fully, although plausible events include: a genotoxic effect of acetaldehyde, the main metabolite of ethanol; increased oestrogen concentration, which is important for breast carcinogenesis; a role as solvent for tobacco carcinogens; production of reactive oxygen species and nitrogen species; and changes in folate metabolism. Alcohol consumption is increasing in many countries and is an important cause of cancer worldwide.",
# "Ethanol is neither genotoxic nor mutagenic. Its first metabolite acetaldehyde, however, is a powerful local carcinogen. Point mutation in ALDH2 gene proves the causal relationship between acetaldehyde and upper digestive tract cancer in humans. Salivary acetaldehyde concentration and exposure time are the two major and quantifiable factors regulating the degree of local acetaldehyde exposure in the ideal target organ, oropharynx. Instant microbial acetaldehyde formation from alcohol represents >70% of total ethanol associated acetaldehyde exposure in the mouth. In the oropharynx and achlorhydric stomach acetaldehyde is not metabolized to safe products, instead in the presence of alcohol it accumulates in saliva and gastric juice in mutagenic concentrations. A common denominator in alcohol, tobacco and food associated upper digestive tract carcinogenesis is acetaldehyde. Epidemiological studies on upper GI tract cancer are biased, since they miss information on acetaldehyde exposure derived from alcohol and acetaldehyde present in 'non-alcoholic' beverages and food.",
# "Infertility is a severe medical problem and is considered a serious global public health issue affecting a large proportion of humanity. Oxidative stress is one of the most crucial factors involved in infertility. Recent studies indicate that the overproduction of reactive oxygen species (ROS) or reactive nitrogen species (RNS) may cause damage to the male and female reproductive systems leading to infertility. Low amounts of ROS and RNS are essential for the normal functioning of the male and female reproductive systems, such as sperm motility, acrosome reaction, interactions with oocytes, ovulation, and the maturation of follicles. Environmental factors such as heavy metals can cause reproductive dysfunction in men and women through the overproduction of ROS and RNS. It is suggested that oxidative stress caused by arsenic is associated with male and female reproductive disorders such as through the alteration in sperm counts and motility, decreased sex hormones, dysfunction of the testis and ovary, as well as damage to the processes of spermatogenesis and oogenesis. This review paper highlights the relationship between arsenic-induced oxidative stress and the prevalence of infertility, with detailed explanations of potential underlying mechanisms.",
# "The microbiota-gut-brain axis is a bidirectional signaling mechanism between the gastrointestinal tract and the central nervous system. The complexity of the intestinal ecosystem is extraordinary; it comprises more than 100 trillion microbial cells that inhabit the small and large intestine, and this interaction between microbiota and intestinal epithelium can cause physiological changes in the brain and influence mood and behavior. Currently, there has been an emphasis on how such interactions affect mental health. Evidence indicates that intestinal microbiota are involved in neurological and psychiatric disorders. This review covers evidence for the influence of gut microbiota on the brain and behavior in Alzheimer disease, dementia, anxiety, autism spectrum disorder, bipolar disorder, major depressive disorder, Parkinson's disease, and schizophrenia. The primary focus is on the pathways involved in intestinal metabolites of microbial origin, including short-chain fatty acids, tryptophan metabolites, and bacterial components that can activate the host's immune system. We also list clinical evidence regarding prebiotics, probiotics, and fecal microbiota transplantation as adjuvant therapies for neuropsychiatric disorders.",
# "O - linked N - acetylglucosamine ( O - GlcNAc ) is a dynamic post - translational modification occurring on myriad proteins in the cell nucleus , cytoplasm , and mitochondria .The donor sugar for O - GlcNAcylation , uridine - diphosphate N - acetylglucosamine ( UDP - GlcNAc ) , is synthesized from glucose through the hexosamine biosynthetic pathway ( HBP ) .",
# "Cholesterol is a multifaceted metabolite that is known to modulate processes in cancer, atherosclerosis, and autoimmunity. A common denominator between these diseases appears to be the immune system, in which many cholesterol-associated metabolites impact both adaptive and innate immunity. Many cancers display altered cholesterol metabolism, and recent studies demonstrate that manipulating systemic cholesterol metabolism may be useful in improving immunotherapy responses. However, cholesterol can have both proinflammatory and anti-inflammatory roles in mammals, acting via multiple immune cell types, and depending on context. Gaining mechanistic insights into various cholesterol-related metabolites can improve our understanding of their functions and extensive effects on the immune system, and ideally will inform the design of future therapeutic strategies against cancer and/or other pathologies.",
# "The recycling of O - GlcNAc on proteins is mediated by two enzymes in cells - O - GlcNAc transferase ( OGT ) and O - GlcNAcase ( OGA ) , which catalyze the addition and removal of O - GlcNAc , respectively .O - GlcNAcylation is involved in a number of important cell processes including transcription , translation , metabolism , signal transduction , and apoptosis .Deregulation of O - GlcNAcylation has been reported to be associated with various human diseases such as cancer , diabetes , neurodegenerative diseases , and cardiovascular diseases .(0 - not any proper association)"]
# # new_abstract = []

# for abstract in sample_abstracts:
#     start_time = time.time()
#     abstract_spaced = "".join((' {} '.format(el.encode().decode()) if (not el.isalnum() and not el.isspace()) else el for el in abstract))
#     abstract_preprocessed = " ".join(abstract_spaced.split())
#     # new_abstract.append(abstract_preprocessed)

#     ''' For list of documents (DO THIS OUTSIDE LOOP)
#     docs = list(nlp.pipe(new_abstract))
#     c_doc = Doc.from_docs(docs)
#     doc = nlp(c_doc)
#     '''

#     ''' For single document at a time
#     doc = nlp(abstract)
#     '''

#     doc = nlp(abstract_preprocessed)

#     #print NER result
#     print('\n')
#     print('Next abstract results:')
#     print([(ent.text, ent.label_, ent.ent_id_) for ent in doc.ents])
#     record_per_abstract_times.append(round(time.time() - start_time, 5))
#     record_per_abstract_length.append(len(abstract))
#     # print("--- %s seconds ---" % (time.time() - start_time))



# # Log times into file
# if(os.path.exists('per_word_times_log.csv')):
#     per_word_times_df = pd.read_csv('per_word_times_log.csv')
#     per_word_times_df.loc[len(per_word_times_df.index)] = [total_entries, min(record_per_word_times), max(record_per_word_times), \
#     round(np.mean(record_per_word_times), 6), round(total_words_end_time, 6), record_ruler_add_times, record_per_abstract_length, record_per_abstract_times]
# else:
#     per_word_times_df = pd.DataFrame(columns=['Total entries', 'Min time', 'Max time', 'Mean time', 'Total time for building patterns', \
#     'Time taken at adding to ruler', 'Abstract length (number of words)', 'Time taken in abstract'])
#     per_word_times_df['Total entries'] = total_entries
#     # per_word_times_df['Total metabolite patterns'] = len(metabolites_patterns)) 
#     per_word_times_df['Min time'] = min(record_per_word_times)
#     per_word_times_df['Max time'] = max(record_per_word_times)
#     per_word_times_df['Mean time'] = round(np.mean(record_per_word_times), 6)
#     per_word_times_df['Total time for building patterns'] = round(total_words_end_time, 6)
#     per_word_times_df['Time taken at adding to ruler'] = record_ruler_add_times
#     per_word_times_df['Abstract length (number of words)'] = record_per_abstract_length
#     per_word_times_df['Time taken in abstract'] = record_per_abstract_times    

# per_word_times_df.to_csv('per_word_times_log.csv', index = False)


# # Issues on 10k rows:
#     # {"label":"Metabolites","pattern":[{"LOWER":"5"}],"id":"Cholesterol"} how is 5 an entity, where was this extracted from
#         # This was from 5 ['5'] (3beta,14beta,17alpha)-Cholest-5-en-3-ol:Cholest-5-en-3beta-ol:Cholesterin:(3b,14b,17a)-Cholest-5-en-3-ol:(3Β,14β,17α)-cholest-5-en-3-ol:Cholest-5-en-3b-ol:Cholest-5-en-3β-ol:(3Β)-cholest-5-en-3-ol:(3beta)-Cholest-5-en-3-ol:3Β-hydroxycholest-5-ene:3beta-Hydroxycholest-5-ene:5:6-Cholesten-3β-ol:5:6-Cholesten-3beta-ol:(-)-Cholesterol:Cholesterine:Cholesterol base H:Cholesteryl alcohol:Cholestrin:Cholestrol:Cordulan:Dastar:Dusoline:Dusoran:Dythol:Fancol CH:Hydrocerin:Kathro:Lanol:Super hartolan:Tegolan:Cholesterol:delta5-Cholesten-3beta-ol:Δ5-Cholesten-3β-ol' b'Cholesterol'
#         # There is a synonym just with name '5' - what is this? 
#         # Solution to remove this is to filter and check if a name contains only numbers - if so then do not include in patterns file.

#     # {"label":"Metabolites","pattern":[{"LOWER":"a"}],"id":"Adenine"} what to do with this?

#     # Does the pattern matching work on first see basis?
#         # If {"label":"Metabolites","pattern":[{"LOWER":"Uridin"}],"id":"Uridine"} was seen before Uridine 5'-dips, then would that
#         # be matched first?
#         # Fixed

# # Check times on each word for building pattern - get all values and tabulate min, max, mean, std dev, mode, median
# # Check times for add pattern to ruler - compare with 10k, 20k 30k
# # Check times for each abstract and tabulate values with length of abstract and time taken to get tokens and then report bin values
# # like abstract size 500 to 1000: takes average 10 seconds and max and min, abstract size 100 to 1500: takes average 15 seconds and max and min 


# # Check with accepting whole caps (AT) or exact case-sensitive match - deal with two char term for now.
# # RoS - we want match with RoS not rOS.
# # Ignore 1-word terms - number or char.

"""


'''

Pipeline update Jan 01

'''
# coding: utf-8

import spacy
from spacy.lang.en import English 
from spacy.tokens import Doc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os

metabolite_file = '../../Data/hmdb_mDivided.csv'
met_lib = pd.read_csv(metabolite_file)
print(met_lib.shape)

import json
syn_lib = json.load(open('../../Data/SYNONYMS.json'))
print(len(syn_lib))

# names_processed = []
total_entries = 10000  # Change values and try which works (tried till 50k, can try more than that) # For full use len(met_lib)
# start_time = time.time()

'''
If we have A list already do not run this again

# for i in range(total_entries):

#     # Clean text, remove 'b' from the beginning of string
#     full_name = met_lib.iloc[i]['name'].strip("b\'\"")
#     full_name_decoded = full_name.encode().decode() # \u2019 - ' urindine
#     names_processed.append(full_name_decoded)
    
# print('Metabolite names processed', len(names_processed))

# A_list = set() # Set to keep unique values

# # Select only one-word names, and these one-word names must have maximum 5 to 10 characters
# for i in range(len(names_processed)):
#     if(len(names_processed[i]) <= 11 and len(names_processed[i].split()) == 1): 
#          Can 10 Oleic acid and 11 Adipic acid be considered even though they have two words? - No 
#         A_list.add(names_processed[i])

# A_list = list(A_list)
# print('Number of names in A_list ', len(A_list), A_list[:5])
# print('Time taken to prepare A list ', round(time.time() - start_time, 4))
'''

# Directly import A list
A_list_df = pd.read_csv('A_list_31_01.csv')
A_list = A_list_df['A_list_names']

print('A_list ', len(A_list) )

start_time = time.time()
new_met_lib_index = []

# Need to remove that b character (represents bytes but it is string here in df) from iupac_name and name
metabolites_patterns = []

verbose_frequency1=200
verbose_frequency2=200
nn1,nn2=0,0
for i in range(total_entries):
    
    # Clean text, remove 'b' from the beginning of string
    full_name = met_lib.iloc[i]['name'].strip("b\'\"")
    full_name_decoded = full_name.encode().decode() # \u2019 - ' urindine
    id_name = full_name_decoded

    ## process name column
    flag_i1=False
    # Check if word is acceptable - to be acceptable it should have some occurence of any word from A_list
    if any(x.lower() in full_name_decoded.lower() for x in A_list) :
        # Add to patterns file
        flag_i1=True
        # Have the original name as a pattern for exact match of main name, so process the word also
        full_name_spaced = ''.join((' {} '.format(el.lower()) if not el.isalnum() and not el.isspace() else el for el in full_name_decoded))
        full_name_list = full_name_spaced.split()
        add_split_pattern = []
    
        for split_word in full_name_list:
            add_split_pattern.append({"LOWER": str(split_word.lower())}) # The first lower did not work
        metabolites_patterns.append({"label": "Metabolites", "pattern": add_split_pattern, "id": id_name })
        
    if flag_i1:
        nn1+=1
        if verbose_frequency1 and nn1%verbose_frequency1==0:
            for x in A_list:
                if x.lower() in full_name_decoded.lower():
                    print("name col:",nn1,i,"::",full_name_decoded,"::",x)
                    print(metabolites_patterns[-1])
                    print()
                    break

    ## process synonyms column
    flag_i2=False
    syn_spaced2=''
    x2=''
    # There are many metabolites with nan synonyms, so ignore them
    if(syn_lib[i] != ['nan'] and syn_lib[i] != [''] and syn_lib[i] != [' '] ):
        
        # No Need to split synonym
        syn_list = syn_lib[i]

        # Fixing issue of synonyms being just numbers. 
        # Solution is to filter and check if a name contains only numbers (isnumeric), if so then do not include in patterns file.
        
        syn_list = [item for item in syn_list if not item.isnumeric() and len(item) > 1] # This greater than 1 condition to avoid single alphabets

        for syn in syn_list:
            # Doing encode.decode even on normal strings does not affect anything, but helps with strings having unicode characters
            syn_decoded = syn.encode().decode()
            syn_spaced = ''.join((' {} '.format(el.lower()) if not el.isalnum() and not el.isspace() else el for el in syn_decoded))
            syn_split = syn_spaced.split()

            ##check whether A_list in current syn
            flag=False
            if any(x.lower() in syn_spaced.lower() for x in A_list):
                flag=True
                flag_i2=True
                syn_spaced2=syn_spaced

            if flag:
	            # If two letter word then do case sensitive exact match. This is to handle AS, AT words, not to be confused with as, at.
	            if(len(syn_spaced) == 2):
	                metabolites_patterns.append({"label": "Metabolites", "pattern": syn_spaced, "id": id_name })
	            else:  
	                # Having double spaces also does not affect as .split() removes any word between any number of spaces
	                add_split_pattern = []
	                for split_word in syn_split:
	                    add_split_pattern.append({"LOWER": str(split_word.lower())}) # The first lower did not work
	                metabolites_patterns.append({"label": "Metabolites", "pattern": add_split_pattern, "id": id_name })
    if flag_i2:
        nn2+=1
        if verbose_frequency2 and nn2%verbose_frequency2==0:
            for x in A_list:
                if x.lower() in syn_spaced2.lower():
                    print("syn col:",nn2,i,"::",syn_spaced2,"::",x)
                    print(metabolites_patterns[-1])
                    print()
                    break      
        
print('Total patterns:', len(metabolites_patterns), metabolites_patterns[:2]) # 34k



nlp = None
nlp = English()
ruler = nlp.add_pipe("entity_ruler") #can only work for non-token pattern
with nlp.select_pipes(enable="tagger"):
    ruler.add_patterns(metabolites_patterns)

"""
Use this once we have proper A list to avoid re-computing patterns and ruler componenets

# ruler.to_disk("patterns_spaced.jsonl")
# ruler.from_disk("patterns_spaced.jsonl")

"""
print('Adding to ruler done')

# Apply to abstracts 
# sample_abstracts = ["Uridine 5 ' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides .UDP - glucuronic acid is also a sugar donor for the glycosylation of various plant specialized metabolites .Nevertheless , the roles of UGDs in plant specialized metabolism remain poorly understood .Glycyrrhiza species ( licorice ) , which are medicinal legumes , biosynthesize triterpenoid saponins , soyasaponins and glycyrrhizin , commonly glucuronosylated at the C - 3 position of the triterpenoid scaffold . Later we get Uridine 5 ' - diphosphate ( UDP ) from this process and method.",
# "Cholesterol is a multifaceted metabolite that is known to modulate processes in cancer, atherosclerosis, and autoimmunity. A common denominator between these diseases appears to be the immune system, in which many cholesterol-associated metabolites impact both adaptive and innate immunity. Many cancers display altered cholesterol metabolism, and recent studies demonstrate that manipulating systemic cholesterol metabolism may be useful in improving immunotherapy responses. However, cholesterol can have both proinflammatory and anti-inflammatory roles in mammals, acting via multiple immune cell types, and depending on context. Gaining mechanistic insights into various cholesterol-related metabolites can improve our understanding of their functions and extensive effects on the immune system, and ideally will inform the design of future therapeutic strategies against cancer and/or other pathologies."]

# sample_abstracts = ["Uridine 5 ' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides .UDP - glucuronic acid is also a sugar donor for the glycosylation of various plant specialized metabolites .Nevertheless , the roles of UGDs in plant specialized metabolism remain poorly understood .Glycyrrhiza species ( licorice ) , which are medicinal legumes , biosynthesize triterpenoid saponins , soyasaponins and glycyrrhizin , commonly glucuronosylated at the C - 3 position of the triterpenoid scaffold .",
# "Uridine diphosphate glycosyltransferases (UGTs) are the key enzymes in glycosylation processes for decorating plant natural products with sugars. Crystallography, one of the powerful techniques for determining protein structures, was used as the main experimental technique and combined with biochemical methods to study the structure-function relationship and molecular mechanisms of UGTs. Crystal structures of plant UGTs have revealed their exquisite architectures and provided the structural basis for understanding their catalytic mechanism and substrate specificity. In this chapter, some protocols and experimental details of all key stages of protein structure determination are provided, and the structural insights on plant UGTs are also highlighted in combination of method description.",
# "Lung cancer (LC) is the second most common cause of death in men after prostate cancer, and the third most recurrent type of tumor in women after breast and colon cancers. Unfortunately, when LC symptoms begin to appear, the disease is already in an advanced stage and the survival rate only reaches 2%. Thus, there is an urgent need for early diagnosis of LC using specific biomarkers, as well as effective therapies and strategies against LC. On the other hand, the influence of metals on more than 50% of proteins is responsible for their catalytic properties or structure, and their presence in molecules is determined in many cases by the genome. Research has shown that redox metal dysregulation could be the basis for the onset and progression of LC disease. Moreover, metals can interact between them through antagonistic, synergistic and competitive mechanisms, and for this reason metals ratios and correlations in LC should be explored. One of the most studied antagonists against the toxic action of metals is selenium, which plays key roles in medicine, especially related to selenoproteins. The study of potential biomarkers able to diagnose the disease in early stage is conditioned by the development of new analytical methodologies. In this sense, omic methodologies like metallomics, proteomics and metabolomics can greatly assist in the discovery of biomarkers for LC early diagnosis.",
# "Omega-3 polyunsaturated fatty acid (ω-3 PUFA) supplements for chemoprevention of different types of cancer including lung cancer has been investigated in recent years. ω-3 PUFAs are considered immunonutrients, commonly used in the nutritional therapy of cancer patients. ω-3 PUFAs play essential roles in cell signaling and in cell structure and fluidity of membranes. They participate in the resolution of inflammation and have anti-inflammatory effects. Lung cancer patients suffer complications, such as anorexia-cachexia syndrome, pain and depression. The European Society for Clinical Nutrition and Metabolism (ESPEN) 2017 guidelines for cancer patients only discuss the use of ω-3 PUFAs for cancer-cachexia treatment, leaving aside other cancer-related complications that could potentially be managed by ω-3 PUFAs. This review aims to elucidate whether the effects of ω-3 PUFAs in lung cancer is supplementary, pharmacological or both. In addition, clinical studies, evidence in cell lines and animal models suggest how ω-3 PUFAs induce anticancer effects. ω-3 PUFAs and their metabolites are suggested to modulate pivotal pathways underlying the progression or complications of lung cancer, indicating that this is a promising field to be explored. Further investigation is still required to analyze the benefits of ω-3 PUFAs as supplementation or pharmacological treatment in lung cancer.",
# "A causal association has been established between alcohol consumption and cancers of the oral cavity, pharynx, larynx, oesophagus, liver, colon, rectum, and, in women, breast; an association is suspected for cancers of the pancreas and lung. Evidence suggests that the effect of alcohol is modulated by polymorphisms in genes encoding enzymes for ethanol metabolism (eg, alcohol dehydrogenases, aldehyde dehydrogenases, and cytochrome P450 2E1), folate metabolism, and DNA repair. The mechanisms by which alcohol consumption exerts its carcinogenic effect have not been defined fully, although plausible events include: a genotoxic effect of acetaldehyde, the main metabolite of ethanol; increased oestrogen concentration, which is important for breast carcinogenesis; a role as solvent for tobacco carcinogens; production of reactive oxygen species and nitrogen species; and changes in folate metabolism. Alcohol consumption is increasing in many countries and is an important cause of cancer worldwide.",
# "Ethanol is neither genotoxic nor mutagenic. Its first metabolite acetaldehyde, however, is a powerful local carcinogen. Point mutation in ALDH2 gene proves the causal relationship between acetaldehyde and upper digestive tract cancer in humans. Salivary acetaldehyde concentration and exposure time are the two major and quantifiable factors regulating the degree of local acetaldehyde exposure in the ideal target organ, oropharynx. Instant microbial acetaldehyde formation from alcohol represents >70% of total ethanol associated acetaldehyde exposure in the mouth. In the oropharynx and achlorhydric stomach acetaldehyde is not metabolized to safe products, instead in the presence of alcohol it accumulates in saliva and gastric juice in mutagenic concentrations. A common denominator in alcohol, tobacco and food associated upper digestive tract carcinogenesis is acetaldehyde. Epidemiological studies on upper GI tract cancer are biased, since they miss information on acetaldehyde exposure derived from alcohol and acetaldehyde present in 'non-alcoholic' beverages and food.",
# "Infertility is a severe medical problem and is considered a serious global public health issue affecting a large proportion of humanity. Oxidative stress is one of the most crucial factors involved in infertility. Recent studies indicate that the overproduction of reactive oxygen species (ROS) or reactive nitrogen species (RNS) may cause damage to the male and female reproductive systems leading to infertility. Low amounts of ROS and RNS are essential for the normal functioning of the male and female reproductive systems, such as sperm motility, acrosome reaction, interactions with oocytes, ovulation, and the maturation of follicles. Environmental factors such as heavy metals can cause reproductive dysfunction in men and women through the overproduction of ROS and RNS. It is suggested that oxidative stress caused by arsenic is associated with male and female reproductive disorders such as through the alteration in sperm counts and motility, decreased sex hormones, dysfunction of the testis and ovary, as well as damage to the processes of spermatogenesis and oogenesis. This review paper highlights the relationship between arsenic-induced oxidative stress and the prevalence of infertility, with detailed explanations of potential underlying mechanisms.",
# "The microbiota-gut-brain axis is a bidirectional signaling mechanism between the gastrointestinal tract and the central nervous system. The complexity of the intestinal ecosystem is extraordinary; it comprises more than 100 trillion microbial cells that inhabit the small and large intestine, and this interaction between microbiota and intestinal epithelium can cause physiological changes in the brain and influence mood and behavior. Currently, there has been an emphasis on how such interactions affect mental health. Evidence indicates that intestinal microbiota are involved in neurological and psychiatric disorders. This review covers evidence for the influence of gut microbiota on the brain and behavior in Alzheimer disease, dementia, anxiety, autism spectrum disorder, bipolar disorder, major depressive disorder, Parkinson's disease, and schizophrenia. The primary focus is on the pathways involved in intestinal metabolites of microbial origin, including short-chain fatty acids, tryptophan metabolites, and bacterial components that can activate the host's immune system. We also list clinical evidence regarding prebiotics, probiotics, and fecal microbiota transplantation as adjuvant therapies for neuropsychiatric disorders.",
# "O - linked N - acetylglucosamine ( O - GlcNAc ) is a dynamic post - translational modification occurring on myriad proteins in the cell nucleus , cytoplasm , and mitochondria .The donor sugar for O - GlcNAcylation , uridine - diphosphate N - acetylglucosamine ( UDP - GlcNAc ) , is synthesized from glucose through the hexosamine biosynthetic pathway ( HBP ) .",
# "Cholesterol is a multifaceted metabolite that is known to modulate processes in cancer, atherosclerosis, and autoimmunity. A common denominator between these diseases appears to be the immune system, in which many cholesterol-associated metabolites impact both adaptive and innate immunity. Many cancers display altered cholesterol metabolism, and recent studies demonstrate that manipulating systemic cholesterol metabolism may be useful in improving immunotherapy responses. However, cholesterol can have both proinflammatory and anti-inflammatory roles in mammals, acting via multiple immune cell types, and depending on context. Gaining mechanistic insights into various cholesterol-related metabolites can improve our understanding of their functions and extensive effects on the immune system, and ideally will inform the design of future therapeutic strategies against cancer and/or other pathologies.",
# "The recycling of O - GlcNAc on proteins is mediated by two enzymes in cells - O - GlcNAc transferase ( OGT ) and O - GlcNAcase ( OGA ) , which catalyze the addition and removal of O - GlcNAc , respectively .O - GlcNAcylation is involved in a number of important cell processes including transcription , translation , metabolism , signal transduction , and apoptosis .Deregulation of O - GlcNAcylation has been reported to be associated with various human diseases such as cancer , diabetes , neurodegenerative diseases , and cardiovascular diseases .(0 - not any proper association)"]

# Import our file
sample_abstracts = pd.read_csv('abstract_writer_31_01.csv')
print('Abstract file :', sample_abstracts.shape)

# Check acceptance of an entity and save if it is included (save information of which keyword it belongs to and the iloc of abstracts csv)
accepted_entities = pd.DataFrame(columns=['Entity name', 'Entity label', 'Entity ID', 'Index of abstract in csv', 'Start position in document', 'End position in document'])
count = 0

# Check with Xin if this is correct
A_list = list(map(str.lower, A_list)) # Making it lower because we use lower in phrase matcher and our detected entity might not be same case as A_list text, so might miss out on those strings


for abs_index in range(500): # Change this to 10 or some low number and check results
    start_time = time.time()
    abstract = sample_abstracts.iloc[abs_index]['abstract']
    abstract_spaced = "".join((' {} '.format(el.encode().decode()) if (not el.isalnum() and not el.isspace()) else el for el in abstract))
    abstract_preprocessed = " ".join(abstract_spaced.split())

    ''' For list of documents (DO THIS OUTSIDE LOOP)
    docs = list(nlp.pipe(new_abstract))
    c_doc = Doc.from_docs(docs)
    doc = nlp(c_doc)
    '''

    ''' For single document at a time
    doc = nlp(abstract)
    '''
    doc = None
    doc = nlp(abstract_preprocessed)

    #print NER result
    for ent in doc.ents:
        # print(ent.text)
        """ 
        In new Feb 01 Update, we remove this check condition and include long terms also.

        if(str(ent.text).lower() in A_list): # If accepted as exact match in our needed A_list, then save it
        
        """
        accepted_entities = accepted_entities.append( {'Entity name':str(ent.text), 'Entity label':str(ent.label_), 'Entity ID':str(ent.ent_id_), 'Index of abstract in csv':abs_index, 'Start position in document':ent.start_char,\
        'End position in document': ent.end_char}, ignore_index=True )

    if(abs_index % 100 == 0):
        print('Processing abstract number ', abs_index)
        print('\n')
        print(accepted_entities.shape)
    # print([(ent.text, ent.label_, ent.ent_id_, ent.start_char, ent.end_char) for ent in doc.ents])

print(accepted_entities.shape)
accepted_entities.to_csv('accepted_entities_31_01_test.csv', index=False)
print('Program done')


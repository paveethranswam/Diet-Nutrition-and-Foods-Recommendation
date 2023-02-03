#!/usr/bin/env python
# coding: utf-8

import spacy
from spacy.lang.en import English 
from spacy.tokens import Doc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

metabolite_file = '/N/u/paswam/Carbonate/Desktop/Link to Pavi/KD-DocRE/hmdb_mDivided.csv'
met_lib = pd.read_csv(metabolite_file)
print(met_lib.shape)


# Need to remove that b character (represents bytes but it is string here in df) from iupac_name and name
metabolites_patterns = []
start_time = time.time()

for i in range(len(met_lib)): # Change values and try which works (tried till 50k, can try more than that)
    try:
        # Clean text
        name = met_lib.iloc[i]['name'].strip("b\'\"")
        
        # Have the original name as a pattern for exact match of main name
        metabolites_patterns.append({"label": "Metabolites", "pattern": name, "id": name })

        # IUPAC Names has \xc2\\xb2,\\xe2\\x81\\xb7.0\\xc2\\xb9\\xc2\\xb9,\\xc2\\xb9\\x characters
        # Check if this is correct format
        # iupac = met_lib.iloc[i]['iupac_name'].strip("b\'\"")
        
        # There are many metabolites with nan synonyms, so ignore them
        if(str(met_lib.iloc[i]['synonym']) != 'nan' ):
            
            # Need to split synonym - delim is : character
            syn_list = met_lib.iloc[i]['synonym'].split(':')
            syn_dict = {}
            for syn in syn_list:
                metabolites_patterns.append({"label": "Metabolites", "pattern": syn, "id": name })
    except:
        print(i)
    
print(len(metabolites_patterns)) 
print(metabolites_patterns[:5])

print("--- %s seconds ---" % (time.time() - start_time))



# Now we have the pattern ruler ready, run on one abstract

nlp = None
nlp = English()
ruler = nlp.add_pipe("entity_ruler",  config={"phrase_matcher_attr": "LOWER")
start_time = time.time()


# How do we specify the label or tagger name
# Can we use spacy Span Matcher instead of Entity rule matching?
with nlp.select_pipes(enable="tagger"):
    ruler.add_patterns(metabolites_patterns)

ruler.to_disk("patterns.jsonl")

sample_abstract = ["Uridine 5 '-diphosphate ( UDP ) - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides .UDP - glucuronic acid is also a sugar donor for the glycosylation of various plant specialized metabolites .Nevertheless , the roles of UGDs in plant specialized metabolism remain poorly understood .Glycyrrhiza species ( licorice ) , which are medicinal legumes , biosynthesize triterpenoid saponins , soyasaponins and glycyrrhizin , commonly glucuronosylated at the C - 3 position of the triterpenoid scaffold ."]

docs = list(nlp.pipe(sample_abstract))
c_doc = Doc.from_docs(docs)
doc = nlp(c_doc)

#print NER result
print([(ent.text, ent.label_, ent.ent_id_) for ent in doc.ents])
print("--- %s seconds ---" % (time.time() - start_time))





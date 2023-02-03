'''
Based on spacy v3.4

Please read the following docs for reference:
	https://spacy.io/usage/rule-based-matching#entityruler
	https://spacy.io/api/doc
	https://stackoverflow.com/questions/48783876/whats-the-ideal-way-to-include-dictionaries-gazetteer-in-spacy-to-improve-ner
	https://www.google.com/search?q=ner+with+dictionary&oq=ner+with+dic&aqs=chrome.1.69i57j33i160l4.4178j0j7&sourceid=chrome&ie=UTF-8

What is Span ?
https://stackoverflow.com/questions/58876392/what-is-the-difference-between-token-and-span-a-slice-from-a-doc-in-spacy

Other potential packages:
	https://nlp.stanford.edu/software/CRF-NER.html
	https://www.nltk.org/book/ch07.html#consec-use-maxent

For case sensitive spacy matcher:
https://stackoverflow.com/questions/68003864/how-can-i-make-spacy-matches-case-insensitive
'''
import spacy
from spacy.lang.en import English 
from spacy.tokens import Doc
# from spacy.matcher import PhraseMatcher

#add patterns
nlp = English()
# matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
# nlp = spacy.load("en_ner_bc5cdr_md")
ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"})



metabolites_patterns = [
#  {"label": "test", "pattern": "United Kingdom", "id": "loc_test1"},
  {"label": "Metabolites", "pattern": "Uridine 5'-diphosphate", "id": "Uridine 5'-diphosphate_nospace_detection"},
  {"label": "Metabolites", "pattern": "Uridine 5' - diphosphate", "id": "Uridine 5'-diphosphate"},
  {"label": "Metabolites", "pattern": [{"TEXT": {"REGEX": "[Uu](ridine)\s*5'\s*-\s*diphosphate"}}], "id": "Uridine 5'-diphosphate1"}]
ruler.add_patterns(metabolites_patterns)

#build abstracts
abstracts = ["Uridine 5' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides.",
          "In the presence of inorganic phosphate, uridine 5' -diphosphate glucose (UDPG) is specifically hydrolyzed to glucose 1-phosphate and UDP by a unique enzyme, UDPG phosphorylase.",
         "London is the capital of the United Kingdom."]

docs = list(nlp.pipe(abstracts))
c_doc = Doc.from_docs(docs)
doc = nlp(c_doc)

#print NER result
# print([(span.text, span.label_) for span in doc.spans["ruler"]]) # for spans
print([(ent.text, ent.label_, ent.ent_id_) for ent in doc.ents])


# Step 1:
# Uridine 5' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe
# [Uridine 
# 5'
# -
# diphosphate
# ( 
# UDP 
# ) 
# and 
# uridINe 
# 5'
# -
# dipHOSphaTe]

# # s2
# Metlib
# {"label":"Metabolites","pattern":"Uridine 5'-diphosphate","id":"Uridine 5'-diphosphate"}
# After splitting

# [{"label":"Metabolites","pattern":"Uridine", "id":"Uridine 5'-diphosphate"}
# {"label":"Metabolites","pattern":"5", "id":"Uridine 5'-diphosphate"}
# {"label":"Metabolites","pattern":"'", "id":"Uridine 5'-diphosphate"}
# {"label":"Metabolites","pattern":"-", "id":"Uridine 5'-diphosphate"}
# {"label":"Metabolites","pattern":"diphosphate", "id":"Uridine 5'-diphosphate"}]

# # out
# text, label, tag
# 1. Uridine, meta, Uridine 5'-diphosphate




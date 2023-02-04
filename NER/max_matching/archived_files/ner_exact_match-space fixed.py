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
import re

nlp = English()
ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"}) #can only work for non-token pattern

# Build this pattern automatically from metabolite library
met_lib = ["Uridine 5'-diphosphate", "Uridine diphosphate", "Uridine 5'-diphosphoric acid", "5'-UDP",\
 "1-beta-D-Ribofuranosylpyrimidine-2,4(1H,3H)-dione", "Uridine 5\u2019-pyrophosphoric acid'"]
id_name = "Uridine 5'-diphosphate"

metabolites_patterns = []
# For each value in metabolite library, decode it and then add to patterns 
  # While adding to patterns, aplit the full word on all special characters and each word put as {LOWER: that_word} for every full word
for full_word in met_lib:
  # The word as it is
  metabolites_patterns.append({"label": "Metabolites", "pattern": full_word, "id": id_name })

  # Doing encode.decode even on normal strings does not affect anything, but helps with strings having unicode characters
  full_word_decoded = full_word.encode().decode()
  full_word_spaced = ''.join((' {} '.format(el.lower()) if not el.isalnum() and not el.isspace() else el for el in full_word_decoded))
  # Having double spaces also does not affect as .split() removes any word between any number of spaces
  full_word_list = full_word_spaced.split()
  add_split_pattern = []
  for split_word in full_word_list:
    add_split_pattern.append({"LOWER": str(split_word)})
  metabolites_patterns.append({"label": "Metabolites", "pattern": add_split_pattern, "id": id_name })

print(metabolites_patterns)

# Now preprocessing on abstracts (including unicode character removal) - IS THIS STEP NECESSARY BECAUSE IT SEEMS LIKE ABSTRACTS ALREADY HAVE SPACED WORDS (NOT SURE 
# IF THIS APPLIES TO ALL ABSTRACTS )
abstracts = [
			"London is the United Kingdom capital of the United Kingdom.",
      "Uridine 5 ' - diphosphate ( UDP ) - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of \
      plant cell wall polysaccharides .",
      "In the presence of inorganic phosphate, uridine 5'-diphosphate glucose (UDPG) is specifically hydrolyzed to glucose 1-phosphate and UDP by a unique enzyme, UDPG phosphorylase."
         ]

new_abstracts = []
for abstract in abstracts:
  abstract_spaced = "".join((' {} '.format(el.encode().decode()) if (not el.isalnum() and not el.isspace()) else el for el in abstract))
  abstract_preporcessed = " ".join(abstract_spaced.split())
  new_abstracts.append(abstract_preporcessed)

print(new_abstracts)

ruler.add_patterns(metabolites_patterns)
docs = list(nlp.pipe(new_abstracts))
c_doc = Doc.from_docs(docs)
doc = nlp(c_doc)

#print NER result
# print([(span.text, span.label_) for span in doc.spans["ruler"]]) # for spans
print([(ent.text, ent.label_, ent.ent_id_, ent.start_char, ent.end_char) for ent in doc.ents])

# [{'label': 'Metabolites', 'pattern': "uridine 5'-diphosphate", 'id': "Uridine 5'-diphosphate"},
# {'label': 'Metabolites', 'pattern': [{'LOWER': 'uridine'}, {'LOWER': '5'}, {'LOWER': "'"}, {'LOWER': '-'}, {'LOWER': 'diphosphate'}], 'id': "Uridine 5'-diphosphate"},
# {'label': 'Metabolites', 'pattern': 'uridine diphosphate', 'id': "Uridine 5'-diphosphate"},
# {'label': 'Metabolites', 'pattern': [{'LOWER': 'uridine'}, {'LOWER': 'diphosphate'}], 'id': "Uridine 5'-diphosphate"}]

# Test section 
import spacy
from spacy.lang.en import English 
from spacy.tokens import Doc
import re

metabolites_patterns = [{'label': 'Metabolites', 'pattern': "Uridine 5'-diphosphate", 'id': "Uridine 5'-diphosphate"},
{'label': 'Metabolites', 'pattern': [{'LOWER': 'uridine'}, {'LOWER': '5'}, {'LOWER': "'"}, {'LOWER': '-'}, {'LOWER': 'diphosphate'}], 'id': "Uridine 5'-diphosphate"},
{'label': 'Metabolites', 'pattern': 'uridine diphosphate', 'id': "Uridine 5'-diphosphate"},
{'label': 'Metabolites', 'pattern': [{'LOWER': 'uridine'}, {'LOWER': 'diphosphate'}], 'id': "Uridine 5'-diphosphate"}]
nlp = English()
ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"}) #can only work for non-token pattern
ruler.add_patterns(metabolites_patterns)
abstracts = [
			"London is the United Kingdom capital of the United Kingdom.",
            "Uridine 5' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides.",
          	"In the presence of inorganic phosphate, uridine 5'-diphosphate glucose (UDPG) is specifically hydrolyzed to glucose 1-phosphate and UDP by a unique enzyme, UDPG phosphorylase."
         ]

docs = list(nlp.pipe(abstracts))
c_doc = Doc.from_docs(docs)
doc = nlp(c_doc)
print([(ent.text, ent.label_, ent.ent_id_, ent.start_char, ent.end_char) for ent in doc.ents])


''' Original code for patterns
metabolites_patterns = [
  {"label": "test", "pattern": "United Kingdom", "id": "loc_test1"},
  {"label": "Metabolites", "pattern": [{"LOWER": "uridine"}, {"LOWER": "5"}, {"LOWER": "'"}, {"LOWER": "-"}, {"LOWER": "diphosphate"}], "id": "Uridine 5'-diphosphate2"},
  {"label": "Metabolites", "pattern": "just add for test) Uridine 5' - diphosphate", "id": "Uridine 5'-diphosphate"}
]
ruler.add_patterns(metabolites_patterns)
'''

'''
#tokenization:

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("uridine 5'-diphosphate")
for token in doc:
    print(token.text)
doc = nlp("Uridine 5' - diphosphate ")
for token in doc:
    print(token.text)
'''

#build abstracts
'''Original Abstracts - that work with spaced pattern matching
abstracts = [
			"London is the United Kingdom capital of the United Kingdom.",
            "Uridine 5' - diphosphate ( UDP ) and uridINe 5' - dipHOSphaTe - glucose dehydrogenase ( UGD ) produces UDP - glucuronic acid from UDP - glucose as a precursor of plant cell wall polysaccharides.",
          	"In the presence of inorganic phosphate, uridine 5'-diphosphate glucose (UDPG) is specifically hydrolyzed to glucose 1-phosphate and UDP by a unique enzyme, UDPG phosphorylase."
         ]

docs = list(nlp.pipe(abstracts))
c_doc = Doc.from_docs(docs)
doc = nlp(c_doc)

#print NER result
# print([(span.text, span.label_) for span in doc.spans["ruler"]]) # for spans
print([(ent.text, ent.label_, ent.ent_id_, ent.start_char, ent.end_char) for ent in doc.ents])

'''



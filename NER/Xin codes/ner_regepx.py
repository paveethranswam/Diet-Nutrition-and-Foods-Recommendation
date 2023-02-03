'''
Using RegEx for phrase pattern in EntityRuler:
https://stackoverflow.com/questions/57667710/using-regex-for-phrase-pattern-in-entityruler
https://stackoverflow.com/questions/61628562/regex-pattern-for-spacy-entityruler-does-not-work
https://www.google.com/search?q=spacy+entityruler+with+regular+expression&sxsrf=ALiCzsYF0AXiU3HHnRmpRDP3-0uYQYIQvg%3A1671408079967&ei=z6mfY9rQOvKl1QH8uqmoBQ&oq=spacy+EntityRuler+with+regular&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgAMgUIIRCgATIFCCEQoAEyBQghEKABMgUIIRCgAToKCAAQRxDWBBCwAzoICAAQgAQQywE6BggAEAcQHjoGCAAQHhAKOgQIABAeOgYIABAIEB46BQgAEKIEOgcIIRCgARAKSgQIQRgASgQIRhgAUNsFWMiYAWDUpAFoAnABeACAAb4DiAG4DZIBCDE2LjEuNC0xmAEAoAEBoAECyAEKwAEB&sclient=gws-wiz-serp


Please read the following articles to solve intra-hyphen issue when using Spacy:
https://www.google.com/search?q=hypoen+in+token+of+spacy&sxsrf=ALiCzsZ9dLL_l2cW6l_dBrbvxwixxCq8YQ%3A1671412015568&ei=L7mfY8qiIpqu5NoP6qC64AU&ved=0ahUKEwiK9tf7voT8AhUaF1kFHWqQDlwQ4dUDCA8&uact=5&oq=hypoen+in+token+of+spacy&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQogQyBQgAEKIEMgoIABDxBBAeEKIEOgoIABBHENYEELADOgcIIxCwAhAnOg0IABAIEB4Q8QQQDRATOgoIIRDDBBAKEKABSgQIQRgASgQIRhgAUPEVWIVMYK5PaARwAXgAgAGvAYgBzgySAQQxMi41mAEAoAEByAEJwAEB&sclient=gws-wiz-serp
https://stackoverflow.com/questions/55241927/spacy-intra-word-hyphens-how-to-treat-them-one-word
https://support.prodi.gy/t/how-to-tell-spacy-not-to-split-any-intra-hyphen-words/1456
'''

from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import spacy

nlp = English()
# nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")

#These patterns show how Spacy treats hyphens in text
patterns = [{"label": "FRT1", "pattern": [{'LOWER' : {'REGEX': r"^-apple_pie-$"}}]},
            {"label": "FRT2", "pattern": [{'LOWER' : {'REGEX': "ApPle"}}, {'TEXT' : {'REGEX': r"pie"}}]},
            {"label": "FRT-3", "pattern": [{'TEXT' : {'REGEX': r"ApPle"}}, {'TEXT' : {'REGEX': r"pie"}}]},
            {"label": "FRT-4", "pattern": [{'TEXT' : {'REGEX': r"pine"}}, {'TEXT' : {'REGEX': r"ApPle"}}]},
            {"label": "FRT-5", "pattern": [{'TEXT' : {'REGEX': r"ApPle"}}]},
            # {"label": "FRT5", "pattern": [{'TEXT' : {'REGEX': r"^apple( )pie$"}}]},
            {"label": "FRT6", "pattern": [{'LOWER' : {'REGEX': r"^ap\spi$"}}]},
            {"label": "BRN", "pattern": [{"LOWER": "granny"}, {"LOWER": "smith"}]}]

ruler.add_patterns(patterns)

def custom_tokenizer(nlp):
    inf = list(nlp.Defaults.infixes)               # Default infixes
    inf.remove(r"(?<=[0-9])[+\-\*^](?=[0-9-])")    # Remove the generic op between numbers or between a number and a -
    inf = tuple(inf)                               # Convert inf to tuple
    infixes = inf + tuple([r"(?<=[0-9])[+*^](?=[0-9-])", r"(?<=[0-9])-(?=-)"])  # Add the removed rule after subtracting (?<=[0-9])-(?=[0-9]) pattern
    infixes = [x for x in infixes if '-|–|—|--|---|——|~' not in x] # Remove - between letters rule
    infix_re = compile_infix_regex(infixes)

    return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,
                                suffix_search=nlp.tokenizer.suffix_search,
                                infix_finditer=infix_re.finditer,
                                token_match=nlp.tokenizer.token_match,
                                rules=nlp.Defaults.tokenizer_exceptions)

nlp.tokenizer = custom_tokenizer(nlp)
doc = nlp(u"APple pie is red. Granny Smith apples pies are green. -Apple_pie- is Apple- pie is so dif, ApPle , ApPle pie, apPle pie pois pine ApPle and apple-pie, apple - pie la apple--pie which is apple pie apple   pie.")

# print([token.text for token in doc]) 
print([(ent.text, ent.label_) for ent in doc.ents])

# print([(ent.text, ent.label_) for ent in doc.ents]) #[('Granny Smith', 'BRN'), ('-Apple_pie-', 'FRT'), ('ApPle', 'FRT-1'), ('ApPle pie', 'FRT-1'), ('pine ApPle', 'FRT-2')]


# My edition
# patterns = [{"label": "FRT0", "pattern": [{"TEXT": {"REGEX": "Apple- ?pie"}}]},
#             {"label": "FRT1", "pattern": [{'LOWER' : {'REGEX': r"^-apple_pie-$"}}]},
#             {"label": "FRT2", "pattern": [{'TEXT' : {'REGEX': r"^Apple(\-|\s)pie$"}}]},
#             {"label": "FRT3", "pattern": [{'LOWER' : {'REGEX': r"^ap\spi$"}}]},
#             {"label": "BRN", "pattern": [{"LOWER": "granny"}, {"LOWER": "smith"}]}]

# ruler.add_patterns(patterns)
# doc = nlp(u"APple pie is red. Granny Smith apples pies are green. -Apple_pie- is Apple- pie is so dif, ApPle , ApPle pie, pine ApPle.")

# print([(ent.text, ent.label_) for ent in doc.ents])

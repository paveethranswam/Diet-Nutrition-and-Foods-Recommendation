https://pages.github.nceas.ucsb.edu/NCEAS/Computing/local_install_python_on_a_server.html

https://kb.iu.edu/d/bflv
https://kb.iu.edu/d/acey
https://kb.iu.edu/d/aonm

# This code helps to get some package that is not able to import even after installing
# import sys 
# !{sys.executable} -m pip install --user spacy


1. we develop a sequence-tosequence approach, seq2rel, that can learn the
subtasks of DocRE (entity extraction, coreference resolution and relation extraction) end-toend, 
replacing a pipeline of task-specific components

2. Using entity hinting to compare performances

3. Exisiting methods assume entities are already detected and present. This paper detects discontinous mentions, coreferent mentions, and 
intersentence mentions

4. In this paper, we
extend work on seq2seq methods for RE to the document level, with several important contributions:
• We propose a novel linearization schema that
can handle complexities overlooked by previous seq2seq approaches, like coreferent mentions and n-ary relations (§3.1).
• Using this linearization schema, we demonstrate that a seq2seq approach is able to learn
the subtasks of DocRE (entity extraction,
coreference resolution and relation extraction)
jointly, and report the first end-to-end results
on several popular biomedical datasets (§5.1).
• We devise a simple strategy, referred to as “entity hinting” (§3.3), to compare our model to
existing pipeline-based approaches, in some
cases exceeding their performance (§5.1)

5. (E1, ..., En, R) where n is the number of participating entities, or arity, of the relation R.
Ei is represented as the set of its coreferent mentions {e^ij} in the document, which are often expressed as aliases, abbreviations or acronyms

6. The mentions that express a given relation are not necessarily contained within the same sentence

7. Commonly, E is assumed to be known and provided as input to a model. We will refer to these methods as “pipeline-based”. In this
paper, we are primarily concerned with the situation where E is not given and must be predicted by a model, which we will refer to as “end-to-end”


8. Has three issues and some solutions to fix it.







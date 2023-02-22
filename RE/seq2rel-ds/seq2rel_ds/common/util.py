import io
import random
import re
import warnings
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Tuple
from zipfile import ZipFile

import numpy as np
import requests
from more_itertools import chunked
from requests.adapters import HTTPAdapter
from sklearn.model_selection import train_test_split
from urllib3.util.retry import Retry

from seq2rel_ds.common import sorting_utils
from seq2rel_ds.common.schemas import PubtatorAnnotation, PubtatorEntity
import pandas as pd
import spacy

# Seeds
SEED = 13370
NUMPY_SEED = 1337

# API URLs
PUBTATOR_API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator"


# Enums
class TextSegment(str, Enum):
    title = "title"  # type: ignore
    abstract = "abstract"
    both = "both"


class EntityHinting(str, Enum):
    gold = "gold"
    pipeline = "pipeline"


# Here, we create a session globally that can be used in all requests. We add a hook that will
# call raise_for_status() after all our requests. Because API calls can be flaky, we also add
# multiple requests with backoff.
# Details here: https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
# and here: https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
s = requests.Session()
assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()  # noqa
s.hooks["response"] = [assert_status_hook]
retries = Retry(total=5, backoff_factor=0.1)
s.mount("https://", HTTPAdapter(max_retries=retries))


# Private functions #


def _find_first_mention(string: str, text: str, **kwargs: Any) -> Optional[re.Match]:
    """Search for the first occurrence of `string` in `text`, returning an `re.Match` object if
    found and `None` otherwise. To match `string` to `text` more accurately, we use a type of
    "backoff" strategy. First, we look for the whole entity in text. If we cannot find it, we look
    for a lazy match of its first and last tokens. `**kwargs` are passed to `Pattern.search`.
    """
    match = re.compile(rf"\b{re.escape(string)}\b").search(text, **kwargs)

    if not match:
        ent_split = string.split()
        if len(ent_split) > 1:
            first, last = re.escape(ent_split[0]), re.escape(ent_split[-1])
            match = re.compile(rf"\b{first}.*?{last}\b").search(text, **kwargs)
    return match


def _query_pubtator(body: Dict[str, Any], **kwargs: Any) -> Dict[str, PubtatorAnnotation]:
    r = s.post(PUBTATOR_API_URL, json=body)
    pubtator_content = r.text.strip()
    pubtator_annotations = parse_pubtator(pubtator_content, **kwargs)
    return {ann.pmid: ann for ann in pubtator_annotations}


# Public functions #


def set_seeds() -> None:
    """Sets the random seeds of python and numpy for reproducible preprocessing."""
    random.seed(SEED)
    np.random.seed(NUMPY_SEED)


def download_zip(url: str) -> ZipFile:
    # https://stackoverflow.com/a/23419450/6578628
    r = requests.get(url)
    z = ZipFile(io.BytesIO(r.content))
    return z


def train_valid_test_split(
    data: Iterable[Any],
    train_size: float = 0.7,
    valid_size: float = 0.1,
    test_size: float = 0.2,
    **kwargs: Any,
) -> Tuple[List[Any], List[Any], List[Any]]:
    """Given an iterable (`data`), returns train, valid and test partitions of size `train_size`,
    `valid_size` and `test_size`. Optional `**kwargs` are passed to `sklearn.model_selection.train_test_split`.

    See https://datascience.stackexchange.com/a/53161 for details.
    """
    size_sum = train_size + valid_size + test_size
    if size_sum != 1.0:
        raise ValueError(f"train_size, valid_size and test_size must sum to one. Got {size_sum}.")
    # Round to avoid precision errors.
    train, test = train_test_split(data, test_size=round(1 - train_size, 4), **kwargs)
    valid, test = train_test_split(test, test_size=test_size / (test_size + valid_size), **kwargs)
    return train, valid, test


def parse_pubtator(
    pubtator_content: str,
    text_segment: TextSegment = TextSegment.both,
    skip_malformed: bool = False,
) -> List[PubtatorAnnotation]:
    """Parses a PubTator formatted string (`pubtator_content`) and returns a list of
    `PubtatorAnnotation` objects.

    # Parameters

    pubtator_content : `str`
        A string containing one or more articles in the PubTator format.
    text_segment : `TextSegment`, optional (default = `TextSegment.both`)
        Which segment of the text we should consider. Valid values are `TextSegment.title`,
        `TextSegment.abstract` or `TextSegment.both`.
    skip_malformed : bool, optional (default = `False`)
        True if we should ignore malformed annotations that cannot be parsed. This is useful in
        some cases, like when we are generating data using distant supervision.
    """
    # Get a list of PubTator annotations
    articles = pubtator_content.strip().split("\n\n")

    # Parse the annotations, producing a highly structured output
    parsed = []
    for article in articles:
        # Extract the title and abstract (if it exists)
        split_article = article.strip().split("\n")
        title, abstract, annotations = split_article[0], split_article[1], split_article[2:]
        pmid, title = title.split("|t|")
        abstract = abstract.split("|a|")[-1]
        title = title.strip()
        abstract = abstract.strip()
        
        # if(str(pmid) == str(227508)):
        #     print('Before sorting Annotations are: \n\n', annotations)

        # Sort mentions by order of first appearance
        annotations = sorting_utils.sort_entity_annotations(annotations)

        # if(str(pmid) == str(227508)):
        #     print('Annotations are: \n\n', annotations)
        #     print('over')
        # We may want to experiement with different text sources
        if text_segment.value == "both":
            text = f"{title} {abstract}" if abstract else title
        elif text_segment.value == "title":
            text = title
        else:
            # In at least one corpus (GDA), there is a title but no abstract.
            # we handle that by ignoring it when text_segment is "both", and
            # raising an error when it is "abstract"
            if not abstract:
                msg = f"text_segment was {text_segment.value} but no abstract was found"
                raise ValueError(msg)
            text = abstract

        parsed.append(PubtatorAnnotation(pmid=pmid, text=text))

        for ann in annotations:
            split_ann = ann.strip().split("\t")

            # This is a entity mention
            start: int
            end: int
            if sorting_utils.pubtator_ann_is_mention(split_ann):
                if len(split_ann) == 6:
                    _, start, end, mentions, label, uids = split_ann  # type: ignore
                elif len(split_ann) == 7:
                    _, start, end, _, label, uids, mentions = split_ann  # type: ignore
                # For some cases (like distant supervision) it is
                # convenient to skip annotations that are malformed.
                else:
                    if skip_malformed:
                        continue
                    else:
                        err_msg = f"Found an annotation with an unexpected number of columns: {ann}"
                        raise ValueError(err_msg)
                start, end = int(start), int(end)

                # Ignore this annotation if it is not in the chosen text segment
                section = "title" if start < len(title) else "abstract"
                if section != text_segment.value and text_segment.value != "both":
                    continue

                # In at least one corpus (CDR), the annotators include annotations for the
                # individual entities in a compound entity. So we deal with that here.
                # Note that the start & end indicies will no longer be exactly correct, but are
                # be close enough for our purposes of sorting entities by order of appearence.
                mentions, uids = mentions.split("|"), uids.split("|")  # type: ignore
                for mention, uid in zip(mentions, uids):
                    # Ignore this annotation if the entity is not grounded.
                    # à la: https://www.aclweb.org/anthology/D19-1498/
                    if uid == "-1":
                        continue

                    offset = (start, end)

                    # If this is a compound entity update the offsets to be as correct as possible.
                    if len(mentions) > 1:
                        match = _find_first_mention(mention, text, pos=start, endpos=end)
                        if match is not None:
                            offset = match.span()

                    if uid in parsed[-1].entities:
                        parsed[-1].entities[uid].mentions.append(mention)
                        parsed[-1].entities[uid].offsets.append(offset)
                    else:
                        parsed[-1].entities[uid] = PubtatorEntity(
                            mentions=[mention], offsets=[offset], label=label
                        )
            # This is a relation
            else:
                _, label, *uids = split_ann  # type: ignore
                rel = (*uids, label)
                # Check that the relations entities are in the text
                # and that this relation is unique.
                if rel not in parsed[-1].relations and all(
                    uid in parsed[-1].entities for uid in uids
                ):
                    parsed[-1].relations.append(rel)

    return parsed


# def load_from_pmid(pmid):
    




def pubtator_to_seq2rel(
    document_annotations: List[PubtatorAnnotation],
    sort_rels: bool = True,
    entity_hinting: Optional[EntityHinting] = None,
    **kwargs: Any,
) -> List[str]:
    """Converts the highly structured `pubtator_annotations` input to a format that can be used with
    seq2rel. Optional `**kwargs` are passed to `query_pubtator` when `entity_hinting == "pipeline"`.

    # Parameters

    document_annotations : `List[PubtatorAnnotation]`
        A list of`PubtatorAnnotation` objects to convert to the seq2rel format.
    sort_rels : bool, optional (default = `True`)
        Whether relations should be sorted by order of first appearance. This useful for traditional
        seq2seq models that use an order-sensitive loss function, like negative log-likelihood.
    include_ent_hints : bool, optional (default = `False`)
        True if entity markers should be included within the source text. This effectively converts
        the end-to-end relation extraction problem to a pipeline relation extraction approach, where
        entities are given.
    """
    seq2rel_annotations = []

    # If using pipeline-based entity hinting, it is much faster to retrieve the annotations in bulk
    pmids = [ann.pmid for ann in document_annotations] # Relations target e1 e2 CID
    # document_annotations[0].entities = {'s': 'a'}
    
    # print('Input to this function ', type(document_annotations), document_annotations[0].entities, type(document_annotations[0]))


    pubtator_annotations = (
        query_pubtator(pmids, **kwargs) if entity_hinting == EntityHinting.pipeline else {}
    )
    # The pubtator_annotations is different from document_annotations. They both have similar format of storing files, but
    # Document_annotations has different entities from pubtator_annotations. Because pubtator_annotations is from model output 
    # print(pmids[0], '\n')
    # print(pubtator_annotations[pmids[0]], '\n')

    print('Enter into pubtator_to_seqrel and performing inference on my test dataset \n')
    test_abstracts = pd.read_csv('../../NER/max_matching/abstract_writer_31_01.csv')
    print('Abstract file :', test_abstracts.shape)

    print_freq = 0
    abs_index = 0
    test_dataset_type = 'custom' ## Use this if we are using our test dataset
    test_dataset_type = 'cdr' ## Use this if we are using cdr test dataset
    
    nlp = spacy.load('../../NER/max_matching/patterns_02_17')

    for doc_ann in document_annotations[:10]:
        # Apply entity hinting using the requested strategy (if any). In the "pipeline" setting
        # we use the annotations from PubTator to determine the entity hints. Otherwise, we use
        # the ground truth annotations.
        if entity_hinting == EntityHinting.pipeline:
            ## Start of new code

            '''
            If we are using the inbuilt codes, for getting pipeline based methods for entity extraction
            pubtator_ann = pubtator_annotations.get(doc_ann.pmid)
            
            If we are using our existing NER then replace the above part of code with the new line.
            '''
            
            pubtator_ann = pubtator_annotations.get(doc_ann.pmid)
            # print(type(pubtator_ann), '\n')

            # New NER:
            # Load metabolite patterns model and load necessary codes
            
            # Create an entity_strings and use the insert_hints to insert them before text

            # Check acceptance of an entity and save if it is included (save information of which keyword it belongs to and the iloc of abstracts csv)
            accepted_entities = pd.DataFrame(columns=['Entity name', 'Entity label', 'Entity ID', 'Index of abstract in csv', 'Start position in document', 'End position in document'])

            # Get document abstract from DOC_PMID
            # abstract = str(pubtator_ann.text) ## Use this if we are using cdr test dataset
            abstract = test_abstracts.iloc[abs_index]['abstract'] ## Use this if we are using our test dataset 

            abstract_spaced = "".join((' {} '.format(el.encode().decode()) if (not el.isalnum() and not el.isspace()) else el for el in abstract))
            abstract_preprocessed = " ".join(abstract_spaced.split())
            # print('preprocessed', abstract_preprocessed)
            # Then use that patterns model to detect NERs in document
            doc = None
            doc = nlp(abstract_preprocessed)

            # Then store the NER results to file
            entities_dict = {}

            #print NER result
            for ent in doc.ents:
                # Add to a dict
                if(not entities_dict.get(str(ent.ent_id_))):
                    entities_dict[str(ent.ent_id_)] = [(str(ent.text), str(ent.label_), (ent.start_char, ent.end_char))] # Value and its offset  
                else:
                    if(str(ent.text) not in [i[0] for i in entities_dict[str(ent.ent_id_)]]): # Do not add if already there
                        entities_dict[str(ent.ent_id_)].append((str(ent.text), str(ent.label_), (ent.start_char, ent.end_char)))
                # Sort by offset and then Group by the ID name to create a list of values and then insert to text 
            
            # If no entity detected, then ignore this abstract
            if(abs_index == 1):
                print(abstract)
            if(len(entities_dict) == 0):
                print_freq+=1
                abs_index+=1 # To get next abstract
                if(print_freq % 100 == 0):
                    print('Total seq2rel data at ', abs_index, len(seq2rel_annotations))
                    print(doc_ann.to_string(sort=sort_rels))
                continue

            entity_string_list = []
            entities_list = [] # Contains only entities to use for filtering relation target string
            for ent in entities_dict:
                entity_string = ""
                if(len(entities_dict[ent]) > 1):
                    entity_string+= str(entities_dict[ent][0][0]) ## Convert to lower, and convert type to upper
                    for inner_ent in entities_dict[ent][1:]:
                        entity_string+= ' ; ' + str(inner_ent[0]) ## Convert to lower, and convert type to upper
                    entity_string+= ' @CHEMICAL@'
                    # entity_string+=' @' +  str(inner_ent[1]).upper() + '@'
                    
                else:
                    # entity_string+= str(entities_dict[ent][0][0]) + ' @' +  str(entities_dict[ent][0][1]).upper() + '@'
                    entity_string+= str(entities_dict[ent][0][0]) + ' @CHEMICAL@'
                entities_list.append(str(entities_dict[ent][0][0]))
                entity_string_list.append(entity_string)

            # print(accepted_entities.head())

            # Insert in source text
            after_insert_string = ''
            for i in entity_string_list:
                after_insert_string+= i + ' '
            
            # We should add spaces and process the document so use abstract_preprocessed
            after_insert_string+= '[SEP] ' + str(abstract_preprocessed) ## What if there are no entities
            doc_ann.text = after_insert_string
            print_freq+=1
            abs_index+=1 # To get next abstract
            ## End of new code

            if pubtator_ann is None:
                warnings.warn(
                    f"{entity_hinting} entity hinting strategy selected, but no annotations found"
                    f" for PMID: {doc_ann.pmid}. No hints will be inserted for this document."
                )
                continue

            # pubtator_ann.insert_hints() # This code sorts entities, removes duplicate entities but maintain order, and create a 
            # linearized entity hint text and insert at the beginning of the source text. And makes everything lower . 3H-Dio is turned
            # to 3h-dio
            # doc_ann.text = pubtator_ann.text
            # print('\n after insert ', doc_ann.text)
        elif entity_hinting == EntityHinting.gold:
            doc_ann.insert_hints()

        relation_string = '' # To add at end of source text for seq2rel_annotation for datasets without target string

        ## Start of New code
        # Do this only when using cdr dataset or any dataset which has target values
        if(test_dataset_type == 'cdr'):
            # Do not do this during actual inference, but just for current evaluation, we filter out entities from the relation string
            # that are not present in NER entities list

            ## Do not filter out disease from target
            'Lepo @CHEMICAL@ Canc @DISEASE@ @CID@'
            relation_string = doc_ann.to_string(sort=sort_rels)
            relation_string_list = relation_string.split(' ')
            new_relation_string_list = []
            for word in relation_string_list:
                if(word in entities_list):
                    new_relation_string_list.append(word)
            # Lepo @CHEMICAL@ @CID@
            relation_string = ' ' # add space after text
            for i in range(len(new_relation_string_list)):
                relation_string += new_relation_string_list[i] + ' @CHEMICAL@'
                if(i== len(new_relation_string_list) - 1):
                    relation_string+=' @CID@'

        if(print_freq % 100 == 0):
            print('Total seq2rel data at ', abs_index, len(seq2rel_annotations))

        ## End of New code

        seq2rel_annotation = f"{doc_ann.text.strip()}\t{relation_string.strip()}"
        # if(str(doc_ann.pmid) == str(227508)):
        #     print('After seq2rel annotation', seq2rel_annotation)
        seq2rel_annotations.append(seq2rel_annotation)


    return seq2rel_annotations


def query_pubtator(
    pmids: List[str],
    concepts: Optional[List[str]] = None,
    pmids_per_request: int = 1000,
    **kwargs: Any,
) -> Dict[str, PubtatorAnnotation]:
    """Queries PubTator for the given `pmids` and `concepts`, parses the results and
    returns a highly structured dictionary-like object keyed by PMID. Optional `**kwargs` are passed
    to `seq2rel_ds.common.util.parse_pubtator`.
    For details on the PubTator API, see: https://www.ncbi.nlm.nih.gov/research/pubtator/api.html

    # Parameters

    pmids : `List[str]`
        A list of PMIDs to query PubTator with.
    concepts : `List[str]`, optional (default = `None`)
        A list of concepts to include in the PubTator results.

    """
    body: Dict[str, Any] = {"type": "pmids"}
    if concepts is not None:
        body["concepts"] = concepts
    annotations = {}
    for chunk in chunked(pmids, pmids_per_request):
        # Try to post requests in chunks to speed things up...
        try:
            body["pmids"] = chunk
            pubtator_annotations = _query_pubtator(body, **kwargs)
            annotations.update(pubtator_annotations)
        # ...but, if the request fails, recursively half the size of the request.
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            pubtator_annotations = query_pubtator(chunk, concepts, pmids_per_request // 2, **kwargs)
            annotations.update(pubtator_annotations)
    return annotations

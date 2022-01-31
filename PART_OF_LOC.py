##################################################################################
# IMPORTS
##################################################################################
import sys
import os
import json
import nltk
import spacy
import time
import numpy    as np
import networkx as nx
from   nltk.tokenize import sent_tokenize
from   nltk.tokenize import word_tokenize
from   nltk.stem     import WordNetLemmatizer
from   nltk.corpus   import wordnet
from   spacy         import displacy

##################################################################################
# LOADING PACKAGES
##################################################################################
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')

##################################################################################
# PREPROCESSING FUNCTIONS
##################################################################################
def nlpObject(inputFile):
    with open(inputFile, 'r', encoding='utf-8',errors="ignore") as file:
        data = file.read()
    return data

##################################################################################
# EXTRACTING PART_OF(LOC, LOC) RELATIONS
##################################################################################
def extract_part_loc_relation(data, inputFile):
    print('Executing PART_OF_LOC template')
    time.sleep(1)

    sents           = sent_tokenize(data)
    output_template = {"document": inputFile, "extraction":[]}
    for sent in sents:
        part    = []
        inp_doc = nlp(sent)
        edges   = []
        e_list  = {}
        nodes   = []
        tokens  = []
        is_true = "False"
    
        
        for ent in inp_doc.ents:
            if(ent.label_ == "GPE" and e_list.get(ent.text) is None):
                e_list[ent.text] = ent.label_
                nodes            = nodes + [ent.text]

            
        for token in inp_doc:
            for child in token.children:
                if(token.text not in tokens):        
                    tokens = tokens+[token.text]
                edges.append(('{0}'.format(token.lower_),
                      '{0}'.format(child.lower_)))

        graph   = nx.Graph  (edges)
        digraph = nx.DiGraph(edges)

        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                e1 = nodes[i].lower()
                e2 = nodes[j].lower()

                if(('is' in tokens) and (nx.has_path(digraph, source='is', target=e1)) and (nx.has_path(digraph, source='is', target=e2))):
                    s = (e1, e2)
                    if s not in part:
                        part = part + [s]

                if(('are' in tokens) and (nx.has_path(digraph, source='are', target=e1)) and (nx.has_path(digraph, source='are', target=e2))):
                    s = (e1, e2)
                    if s not in part:
                        part = part + [s]

                if(('in' in tokens) and (nx.has_path(digraph, source='in', target=e1)) and (nx.has_path(digraph, source='in', target=e2))):
                    s = (e1, e2)
                    if s not in part:
                        part = part + [s]

                if((nx.has_path(graph, source=e1, target=e2))):
                    inter_node=nx.shortest_path(graph, source=e1, target=e2)

                    if('is' in inter_node and 'in' in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('is' in inter_node and 'of' in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('in' in inter_node and 'of' in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('in' in inter_node and 'of' not in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('in' not in inter_node and 'is' not in inter_node and 'by' not in inter_node and 'of' in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('are' in inter_node):
                        s = (e1, e2)
                        if s not in part:
                            part = part + [s]

                    if('among' in inter_node):
                        s=(e1,e2)
                        if s not in part:
                            part = part + [s] 

        if(len(part)!=0):
            is_true="true"

        if(is_true):
            for i in range(len(part)):
                final_output = {"template": "PART", "sentences": [], "arguments": {"1": "", "2": ""}}
                final_output["sentences"].append(sent)
                final_output["arguments"]["1"] = part[i][0]
                final_output["arguments"]["2"] = part[i][1]
                output_template["extraction"].append(final_output)

    print('Finished')
    time.sleep(1)

    return(output_template)

##################################################################################
# EXECUTING
##################################################################################
if __name__ == '__main__':
    inputFile  = sys.argv[1]
    merge_ents = nlp.create_pipe("merge_entities")
    nlp.add_pipe(merge_ents)

    inp             = nlpObject(inputFile)
    part_data       = extract_part_loc_relation(inp, inputFile)
    json_object     = json.loads(json.dumps(part_data))
    formatting_data = json.dumps(json_object, indent=4)
    file            = open('output/task2/PART_OF/PART_OF_LOC/outLOC.txt', "w")

    file.write(formatting_data)
    file.close()

    print("Please find the output in the 'output' directory.. \n")
    time.sleep(1)

##################################################################################   
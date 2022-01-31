##################################################################################
# IMPORTS
##################################################################################
import spacy
import neuralcoref
import sys
import json
import time

##################################################################################
# LOADING PACKAGES
##################################################################################
nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

##################################################################################
# PREPROCESSING FUNCTIONS
##################################################################################
def getObj(obj, right_):
    if obj.n_rights:
        right_ += list(obj.rights)
        for i in obj.rights:
            getObj(i, right_)
    return right_

def getSubj(sub, left_):
    if sub.n_lefts:
        left_ += list(sub.lefts)
        for i in sub.lefts:
            getSubj(i, left_)
    return left_

def filter_spans(spans):
    key          = lambda i: (i.end - i.start, -i.start)
    spanSorted   = sorted(spans, key=key, reverse=True)
    output       = []
    iterate      = set()
    for i in spanSorted:
        if i.start not in iterate and i.end - 1 not in iterate:  
            output.append(i)
        iterate.update(range(i.start, i.end))
    output = sorted(output, key=lambda j: j.start)
    return output

def nlpObject(inputFile):
    with open(inputFile, 'r', encoding='utf-8',errors="ignore") as file:
        data = file.read()
        out  = nlp(data)
    return out

##################################################################################
# EXTRACTING BORN RELATIONS
##################################################################################
def extract_born_relation(data, inputFile): 
    print('Executing BORN template')
    time.sleep(1)

    sents = list(data.sents)
    born_relations  = []
    output_template = {"document": inputFile, "extraction":[]}
    for sent in sents:
        try:
            spans = list(sent.ents) + list(sent.noun_chunks)
            spans = filter_spans(spans)
            with data.retokenize() as x:
                for span in spans:
                    x.merge(span)

            final_subject  = None
            final_object   = ''
            date           = ''
            is_true        = False
            main_subject   = None
            location       = ''
            final_output   = {"template": "BORN", "sentences": [], "arguments": {"1": "", "2": "", "3": ""}}

            for token in sent:
                if token.ent_type_ == "DATE":
                    date = token.text

                if token.dep_ == "nsubj" or token.dep_ == "nsubjpass" and main_subject is None: 
                    main_subject = token

                if token.lemma_ == 'born' or token.lemma_ == 'found' or token.lemma_ == 'establish': 
                    is_true = True

                    subject = [w for w in token.lefts if w.dep_ == "nsubj" or w.dep_ == "nsubjpass"]

                    if subject:
                        final_subject    = subject[0]
                        r_subtree        = getObj(token, [])

                        for child in r_subtree:
                            if child.ent_type_ == "DATE":
                                date     = child  
                            
                            if child.ent_type_ == "GPE":
                                location = child 
                            
                    if not subject and not obj:
                        obj           = [w for w in token.lefts   if w.dep_ == "nsubjpass"]
                        subject       = [w for w in token.subtree if w.dep_ == "pobj" and w.nbor(-1).text == 'in']
                        final_object  = obj[0]     if obj     else ''
                        final_subject = subject[0] if subject else None   

                    if final_subject is None:
                        getsubject    = getSubj(token.head, [])
                        final_subject = [w for w in getsubject if w.dep_ == 'nsubj']
                        final_subject = final_subject[0] if final_subject else main_subject

            if is_true:
                born_relations.append({(final_subject, location, date) : sent})
                final_output["sentences"].append(sent.text)
                final_output["arguments"]["1"] = final_subject.text if final_subject else ""
                final_output["arguments"]["2"] = date               if date          else ""
                final_output["arguments"]["3"] = location.text      if location.text else ""

                output_template["extraction"].append(final_output)
        except:
            continue

    print('Finished')
    time.sleep(1)

    return output_template
            
##################################################################################
# EXECUTING
##################################################################################
if __name__ == '__main__':
    inputFile = sys.argv[1]

    try:    
        coref = sys.argv[2]
    except IndexError:
        coref = ''
        
    inp = nlpObject(inputFile)
    if(coref == 'c'):
        inp  = nlp(inp._.coref_resolved)
        print('Executing with Corefrence Resolution.')
        time.sleep(1)

    born_data = extract_born_relation(inp, inputFile)

    json_object        = json.loads(json.dumps(born_data))
    formatting_data    = json.dumps(json_object, indent=4)
    file               = open("output/task2/BORN/BORN_output.json", "w")
    
    file.write(formatting_data)
    file.close()

    print("Please find the output in the 'output' directory.. \n")
    time.sleep(1)

##################################################################################
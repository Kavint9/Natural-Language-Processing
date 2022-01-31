##################################################################################
# IMPORTS
##################################################################################
import sys
import spacy
import neuralcoref
import time
import json
from   ACQUIRE     import extract_acquire_relation
from   BORN        import extract_born_relation
from   PART_OF_LOC import extract_part_loc_relation
from   PART_OF_ORG import extract_part_org_relation

##################################################################################
# LOADING PACKAGES
##################################################################################
nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

##################################################################################
# PREPROCESSING FUNCTIONS
##################################################################################
def nlpObject(inputFile):
    with open(inputFile, 'r', encoding='utf-8',errors="ignore") as file:
        data = file.read()
        out  = nlp(data)
    return out

def nlpObject_part(inputFile):
    with open(inputFile, 'r', encoding='utf-8',errors="ignore") as file:
        data = file.read()
    return data

##################################################################################
# EXECUTING
##################################################################################
if __name__ == '__main__':
    inputFile = sys.argv[1]
    inp1      = nlpObject     (inputFile)
    inp2      = nlpObject_part(inputFile)
    time.sleep(1)

    acquire_data     = extract_acquire_relation(inp1, inputFile)
    json_object1     = json.loads(json.dumps(acquire_data))
    formatting_data1 = json.dumps(json_object1, indent=4)
    file1            = open("output/task3/ACQUIRE_output.txt", "w")

    file1.write(formatting_data1)
    file1.close()

    time.sleep(1)

# ------------------------------------------------------------------------------ #

    born_data        = extract_born_relation(inp1, inputFile)
    json_object2     = json.loads(json.dumps(born_data))
    formatting_data2 = json.dumps(json_object2, indent=4)
    file2            = open("output/task3/BORN_output.txt", "w")

    file2.write(formatting_data2)
    file2.close()

    time.sleep(1)

# ------------------------------------------------------------------------------ #

    part_data1       = extract_part_loc_relation(inp2, inputFile)
    json_object3     = json.loads(json.dumps(part_data1))
    formatting_data3 = json.dumps(json_object3, indent=4)
    file3            = open("output/task3/PART_OF_LOC_output.txt", "w")

    file3.write(formatting_data3)
    file3.close()

    part_data2       = extract_part_org_relation(inp2, inputFile)
    json_object4     = json.loads(json.dumps(part_data2))
    formatting_data4 = json.dumps(json_object4, indent=4)
    file4            = open("output/task3/PART_OF_ORG_output.txt", "w")

    file4.write(formatting_data4)
    file4.close()

    print('\n Finished \n')
    time.sleep(1)


    print("Please find the output in the 'output' directory.. \n")
    time.sleep(1)

##################################################################################   
##################################################################################
# IMPORTS
##################################################################################
import sys
import os
import nltk
import spacy
import time

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem     import WordNetLemmatizer
from nltk.corpus   import wordnet

##################################################################################
# DOWNLOADING AND LOADING PACKAGES
##################################################################################
nltk.download('punkt')
nltk.download('wordnet')

spasee = spacy.load('en_core_web_sm')

##################################################################################
# TOKENIZING THE SENTENCES INTO WORDS
##################################################################################
def word_token(sentences):
    print("Extracting Tokens.")
    time.sleep(1)
    print("Extracting Tokens..")
    time.sleep(1)
    print("Extracting Tokens...")
    time.sleep(1)

    token_text_file = open("output/task1/tokens.txt", "w")
    token_text_file.write ("TOKENS \n\n")
    for sent in sentences:
        token_text_file.write(str(word_tokenize(sent)))

    token_text_file.close()
    print("Finished \n")
    time.sleep(1)

##################################################################################
# LEMMATIZING USING NLTK AND SPACY
##################################################################################
def nltk_lemmatize(sentences):
    print("Lemmatizing using Natural Language Tool Kit.")
    time.sleep(1)
    print("Lemmatizing using Natural Language Tool Kit..")
    time.sleep(1)
    print("Lemmatizing using Natural Language Tool Kit...")
    time.sleep(1)

    lemma_nltk = open("output/task1/lemma/nltk/lemma.txt", "w")
    lemma_nltk.write ("NLTK Lemmatization \n\n")
    lemmatizer = WordNetLemmatizer()
    for i in sentences:
        for word in word_tokenize(i):
            lemma_nltk.write(word + "\t---->\t" + lemmatizer.lemmatize(word))
            lemma_nltk.write("\n")

    lemma_nltk.close()
    print("Finished \n")
    time.sleep(1)

# ------------------------------------------------------------------------------ #

def spacy_lemmatize(sentences):
    print("Lemmatizing using Spacy.")
    time.sleep(1)
    print("Lemmatizing using Spacy..")
    time.sleep(1)
    print("Lemmatizing using Spacy...")
    time.sleep(1)

    lemma_spacy        = open("output/task1/lemma/spacy/lemma.txt", "w")
    lemma_spacy.write("Spacy Lemmatization \n\n")
    dict_spacy_lemmas  = {}
    for sent in sentences:
        spacy_sentence = spasee(sent)
        for word in spacy_sentence: 
            dict_spacy_lemmas[word] = word.lemma_

    for i, j in dict_spacy_lemmas.items():
        lemma_spacy.write("Lemma of " + str(i) + " is " + str(j) + "\n")

    lemma_spacy.close()
    print("Finished \n")
    time.sleep(1)

##################################################################################
# PART OF SPEECH TAGGING USING SPACY
##################################################################################
def spacy_pos(sentences):
    print("Part Of Speech tagging using Spacy.")
    time.sleep(1)
    print("Part Of Speech tagging using Spacy..")
    time.sleep(1)
    print("Part Of Speech tagging using Spacy...")
    time.sleep(1)

    pos_spacy      = open("output/task1/pos.txt", "w")
    pos_spacy.write ("Spacy POS tagging \n\n")
    dict_spacy_pos = {}
    for i in sentences:
        sentence_  = spasee(i)
        for word in sentence_:
            dict_spacy_pos[word] = word.pos_

    for i, j in dict_spacy_pos.items():
        pos_spacy.write("POS tag of " + str(i) + " is " + str(j) + "\n")
    
    pos_spacy.close()
    print("Finished \n")
    time.sleep(1)

##################################################################################
# DEPENDENCY PARSING OF FEATURES USING SPACY
##################################################################################
def spacyDependencyParsing(sentences):
    print("Dependency Parsing using Spacy.")
    time.sleep(1)
    print("Dependency Parsing using Spacy..")
    time.sleep(1)
    print("Dependency Parsing using Spacy...")
    time.sleep(1)

    parsing_spacy = open("output/task1/parsing.txt", "w")
    parsing_spacy.write ("Dependency Parsing \n\n")
    for i in sentences:
        sentence_ = spasee(i)
        for token in sentence_:
            parsing_spacy.write(str(token.text)      + "\t\t")
            parsing_spacy.write(str(token.tag_)      + "\t")
            parsing_spacy.write(str(token.head.text) + "\t")
            parsing_spacy.write(str(token.dep_)      + "\t")
            parsing_spacy.write("\n")            
        parsing_spacy.write("\n\n")

    parsing_spacy.write("\n\n\n\n\n\n")
    parsing_spacy.write ("Noun Phrase Chuncking \n\n")
    for i in sentences:
        sentence_ = spasee(i)
        for token in sentence_.noun_chunks:
            parsing_spacy.write(str(token.text)           + "\t\t")
            parsing_spacy.write(str(token.root.text)      + "\t")
            parsing_spacy.write(str(token.root.dep_)      + "\t")
            parsing_spacy.write(str(token.root.head.text) + "\t")
            parsing_spacy.write(str(token.root.head.pos_) + "\t")
            parsing_spacy.write("\n")            
        parsing_spacy.write("\n\n")
            

    parsing_spacy.close()
    print("Finished \n")
    time.sleep(1)

##################################################################################
# CREATING SYNSET RELATIONS
##################################################################################
def extracting_relational_features(sentences):

    hypernymns = open("output/task1/synset/hypernymns.txt", "w")
    hyponyms   = open("output/task1/synset/hyponyms.txt", "w")
    meronyms   = open("output/task1/synset/meronyms.txt", "w")
    holonyms   = open("output/task1/synset/holonyms.txt", "w")
    hypernymns.write ("Extracting Hypernyms \n\n")
    hyponyms.  write ("Extracting Hyponyms \n\n")
    meronyms.  write ("Extracting Meronyms \n\n")
    holonyms.  write ("Extracting Holonyms \n\n")

    # EXTRACTING HYPERNYMS
    def extract_hypernymns(word):
        features = wordnet.synsets(word)
        
        if len(features)   != 0:
            hypernymns_word = features[0].hypernyms()
            if(len(hypernymns_word)!= 0):
                hypernymns.write("Hypernyms of " + str(word) + " is " + str(hypernymns_word[0].name().partition(".")[0]) + "\n\n")
        
    print("Extracting Hypernyms using Spacy.")
    time.sleep(1)
    print("Extracting Hypernyms using Spacy..")
    time.sleep(1)
    print("Extracting Hypernyms using Spacy...")
    time.sleep(1)

    for i in sentences:
        for word in word_tokenize(i):
            extract_hypernymns(word)

    hypernymns.close()
    print("Finished \n")
    time.sleep(1)

    # EXTRACTING HYPONYMS
    def extract_hyponyms(word):
        features = wordnet.synsets(word)
        
        if len(features) != 0:
            hyponyms_word =features[0].hyponyms()
            if(len(hyponyms_word)!= 0):
                hyponyms.write("Hyponyms of " + str(word) + " is " + str(hyponyms_word[0].name().partition(".")[0]) + "\n\n")
    
    print("Extracting Hyponyms using Spacy.")
    time.sleep(1)
    print("Extracting Hyponyms using Spacy..")
    time.sleep(1)
    print("Extracting Hyponyms using Spacy...")
    time.sleep(1)

    for i in sentences:
        for word in word_tokenize(i):
            extract_hyponyms(word)

    hyponyms.close()
    print("Finished \n")
    time.sleep(1)

    # EXTRACTING MERONYMS
    def extract_meronyms(word):
        features = wordnet.synsets(word)
        
        if len(features) != 0:
            meronyms_word =features[0].member_meronyms()
            if(len(meronyms_word)!= 0):
                meronyms.write("Meronyms of " + str(word) + " is " + str(meronyms_word[0].name().partition(".")[0]) + "\n\n")

    print("Extracting Meronyms using Spacy.")
    time.sleep(1)
    print("Extracting Meronyms using Spacy..")
    time.sleep(1)
    print("Extracting Meronyms using Spacy...")
    time.sleep(1)

    for i in sentences:
        for word in word_tokenize(i):
            extract_meronyms(word)

    meronyms.close()
    print("Finished \n")
    time.sleep(1)

    # EXTRACTING HOLONYMS
    def extract_holonyms(word):
        features = wordnet.synsets(word)
        
        if len(features) != 0:
            holonyms_word = features[0].member_holonyms()
            if(len(holonyms_word)!= 0):
                holonyms.write("Holonyms of " + str(word) + " is " + str(holonyms_word[0].name().partition(".")[0]) + "\n\n")

    print("Extracting Holonyms using Spacy.")
    time.sleep(1)
    print("Extracting Holonyms using Spacy..")
    time.sleep(1)
    print("Extracting Holonyms using Spacy...")
    time.sleep(1)

    for i in sentences:
        for word in word_tokenize(i):
            extract_holonyms(word)

    holonyms.close()
    print("Finished \n")
    time.sleep(1)

##################################################################################
# CALLING ALL FUNCTIONS ONE-BY-ONE
##################################################################################
def NLP_features(sentences):
    print("\n")
    
    # Writing Sentences on a file
    print("Extracting Sentences.")
    time.sleep(1)
    print("Extracting Sentences..")
    time.sleep(1)
    print("Extracting Sentences...")
    time.sleep(1)

    sent_file = open("output/task1/sentences.txt", "w")
    sent_file.write ("SENTENCES \n\n")
    for sentence in sentences:
        sent_file.write(str(sentence))

    sent_file.close()
    print("Finished \n")
    time.sleep(1)

    word_token                    (sentences) # Writing Tokens on a file
    nltk_lemmatize                (sentences) # Writing Lemmas on a file (NLTK)
    spacy_lemmatize               (sentences) # Writing Lemmas on a file (Spacy)
    spacy_pos                     (sentences) # Writing POS Tags on a file
    spacyDependencyParsing        (sentences) # Writing Dependency Parsed Tree on a file
    extracting_relational_features(sentences) # Writing Synsets on files

##################################################################################
# MAIN FUNCTION
##################################################################################
if __name__ == '__main__':

    arg_list  = sys.argv
    path      = str(arg_list[1])
    sentences = []
    with open(path,'r',encoding='utf-8-sig') as file:
              data      = file.read()
              sentences = sent_tokenize(data)
    NLP_features(sentences)
    print("Please find the output in the 'output' directory \n")

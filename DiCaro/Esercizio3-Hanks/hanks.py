from nltk.corpus import wordnet as wn
import nltk
import csv
import spacy
from nltk.wsd import lesk
import os.path

nlp = spacy.load("en_core_web_sm")

# 1. Detection of 300 sentences where the verb 'handle' is used

path = f'Esercizio3-Hanks/resource/medium_articles.csv'
path_corpus = f'Esercizio3-Hanks/resource/corpus.txt'

sentences = []
if not os.path.exists(path_corpus): 
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        i = 0
        articles = []
        for article in reader:
            if i == 0: 
                i += 1
            elif i < 10000:
                text = article[1]
                articles.append(text)
                sentences_text = nltk.sent_tokenize(text)
                for sentence in sentences_text:
                    if 'handle' in sentence and len(sentence) < 300 and not sentence.__contains__("\n"):
                        sentences.append(sentence)
                i += 1
            else: 
                break

    print("Length possible sentences: ", len(sentences))

else: 
    with open(path_corpus, 'r', encoding='utf-8') as f:
        sentences = f.readlines()

# 2. Detection of subjects and objects of the verb using dependecy parser (SpaCy) 
# https://www.geeksforgeeks.org/nlp-wupalmer-wordnet-similarity/ 

# possible subj: csubj, csubjpass, nsubj, nsubjpass
# possible obj: dobj, pobj

corpus = []
for sentence in sentences: 
    doc = nlp(sentence)
    subj = ""
    subj_pos = ""
    obj = ""
    obj_pos = ""
    token_sent = []
    for token in doc: 
        token_sent.append(token.text)
        if token.text == "handle" and token.pos_ == "VERB": 
            indirect_obj = False
            active = True
            children = token.children   
            for child in children:
                if child.dep_ == "pobj":
                    indirect_obj = True
                #if subj != "" and obj != "":
                #    break
                if child.dep_.__contains__("subj") and subj == "":
                    active = not child.dep_.__contains__("pass")
                    subj = child.text
                    subj_pos = child.pos_
                elif (child.dep_ == "dobj" or child.dep_ == "dative") and obj == "":
                    obj = child.text
                    obj_pos = child.pos_
            if subj == "" or obj == "" and not indirect_obj:
                if ("VERB" == token.head.pos_ or "AUX" == token.head.pos_) and "comp" in token.dep_: 
                    head_children = token.head.children
                    for head_child in head_children:
                        if head_child.dep_ == "nsubj" and subj == "":
                            subj = head_child.text
                            subj_pos = head_child.pos_
                        elif head_child.dep_ == "dobj" and obj == "":
                            obj = head_child.text
                            obj_pos = head_child.pos_

    if subj != "" and obj != "" and not indirect_obj: # transitive verb -> if subj and obj and indirect_obj : ditransitive verb!
        corpus.append([subj, subj_pos, obj, obj_pos, sentence, token_sent, str(active)])

print("Length corpus: ", len(corpus))

if not os.path.exists(path_corpus): 
    with open (path_corpus, 'w', encoding='utf-8') as f:
        for sentence in corpus:
            f.write('"'+sentence[4]+'"'+"\n")

# 3. Detection of the synset for each object and subject

synsets = []

for subj, subj_pos, obj, obj_pos, sentence, token_sent, _ in corpus:
    synset_subj = None
    synset_obj = None
    if subj_pos == "PRON": 
        if subj.lower() != "it" and subj.lower() != "its" and subj.lower() != "itself":
            synset_subj = wn.synset('person.n.01')
        else: 
            synset_subj = wn.synset('thing.n.6') # thing (a vaguely specified concern) "several matters to attend to"; "it is none of your affair"; "things are going well"
    elif obj_pos == "PRON":
        if obj.lower() != "it" and obj.lower() != "its" and obj.lower() != "itself":
            synset_obj = wn.synset('person.n.01')
        else: 
            synset_obj = wn.synset('thing.n.6')     
    else:     
        pos = ""
        if subj_pos == "NOUN":
            pos = "n"
        elif subj_pos == "VERB":
            pos = "v"
        elif subj_pos == "ADJ":
            pos = "a"
        elif subj_pos == "ADV":
            pos = "r"
        synset_subj = lesk(token_sent, subj, pos)
        pos = ""
        if obj_pos == "NOUN":
            pos = "n"
        elif obj_pos == "VERB":
            pos = "v"
        elif obj_pos == "ADJ":
            pos = "a"
        elif obj_pos == "ADV":
            pos = "r"
        synset_obj = lesk(token_sent, obj, pos)

    if synset_subj is not None and synset_obj is not None:
        synsets.append([synset_subj, synset_obj, token_sent])

# 4. Detection of the supersense for each object and subject -- fare prova anche con csi 
# http://medialab.di.unipi.it/wiki/SuperSense_Tagger oppure lexname in wordnet

supersenses = []
for synset_subj, synset_obj, token_sent in synsets: 
    supersense_subj = synset_subj.lexname()
    supersense_obj = synset_obj.lexname()
    supersenses.append([supersense_subj, supersense_obj, token_sent])

# 5. Combine meaning of verbs - Hanks theory and results aggregation with frequency of semantics of use 

semantic_use= {}

for supersense_subj, supersense_obj, _ in supersenses:
    if (supersense_subj, supersense_obj) not in semantic_use:
        semantic_use[(supersense_subj, supersense_obj)] = 1
    else: 
        semantic_use[(supersense_subj, supersense_obj)] += 1

# 6. BONUS: detection synset of verb in context and mapping with cluster semantics

analysis = {}
for supersense_subj, supersense_obj, token_sent in supersenses: 
    synset_context = lesk(token_sent, "handle", "v")
    if synset_context is not None:
        if synset_context.name() not in analysis:
            analysis[synset_context.name()] = {}
            analysis[synset_context.name()][(supersense_subj, supersense_obj)] = 1
        else: 
            if (supersense_subj, supersense_obj) not in analysis[synset_context.name()]:
                analysis[synset_context.name()][(supersense_subj, supersense_obj)] = 1
            else: 
                analysis[synset_context.name()][(supersense_subj, supersense_obj)] += 1
    else: 
        print("No synset found for 'handle' in sentence: ", sentence)

for synset in analysis: 
    print("\n \n \n \t \tSynset: ", synset)
    print("Definizion synset: ", wn.synset(synset).definition())
    print("Semantic use: ")
    for subj, obj in analysis[synset]: 
        print(subj, obj)
        print("Frequency: ", analysis[synset][(subj, obj)])

print(wn.synsets("handle"))
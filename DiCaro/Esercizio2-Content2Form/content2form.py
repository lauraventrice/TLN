import csv
import json
import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


# 1. read document definitions and create a data structure

with open(f'Esercizio1-DEFS/resource/definitions.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    definitions = []
    for row in reader:
        definitions.append(row)

with open(f'Esercizio1-DEFS/resource/definitions.json', 'w', encoding='utf-8') as f:
    json.dump(definitions, f, indent=4)


with open(f'Esercizio1-DEFS/resource/definitions.json', 'r', encoding='utf-8') as f: 
    definitions = json.load(f)


with open(f'Esercizio1-DEFS/resource/slang.txt', 'r', encoding='utf-8') as f:
    slang = f.read().splitlines()
    slangs = []
    for pair in slang: 
        list_pair = pair.split("=")
        slangs.append((list_pair[0].lower(), list_pair[1].lower()))

def expand_slangs(tokens: list, slangs: list):
    for i, token in enumerate(tokens):
        for slang in slangs:
            if token == slang[0]:
                tokens[i] = slang[1]
    return tokens

def expand_abbr(tokens: list): 
    for i, token in enumerate(tokens): 
        if token == "e.g." or token == "eg":
            tokens[i] = "for example"
        elif token == "i.e." or token == "ie":
            tokens[i] = "that is"
        elif token == "e.i." or token == "ei":
            tokens[i] = "for example that is"
    return tokens


#2.  pre processing - stopwords removal, lemmatization, slang expansion, abbreviation expansion

stopwords = nltk.corpus.stopwords.words('english')

tokens_concepts = {}

for concept in definitions:  
    keys = list(concept.keys()) 
    keys.remove('Concept')
    tokens = set()
    for key in keys: # for all possible definition for the concept  
        definition = concept[key].lower() 
        if definition != '':
            def_tok = nltk.word_tokenize(definition)

            def_tok = expand_slangs(def_tok, slangs) 
            def_tok = expand_abbr(def_tok) 

            def_tok = [token.lower() for token in def_tok if token not in stopwords and token.isalpha()]
            lemmatizer = WordNetLemmatizer() 
            def_lem = [lemmatizer.lemmatize(token) for token in def_tok] 
            tokens.update(def_lem) 
            concept[key] = def_lem  
        else: 
            del concept[key] 
    
    tokens_concepts[concept['Concept']] = list(tokens) 

with open(f'Esercizio2-Content2Form/resource/preprocessing.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for concept in definitions:
        for key, value in concept.items():
            if key == 'Concept':
                writer.writerow([key])
            else: 
                writer.writerow(value)

# 3. filter definition that are too short or too different from other definitions -> create lexial material


for concept in definitions:
    too_short = []
    for key, value in concept.items():
        if key != 'Concept':
            if len(value) < 3:
                too_short.append(key)
    for key in too_short:
        del concept[key]

with open(f'Esercizio2-Content2Form/resource/preprocessing.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for concept in definitions:
        for key, value in concept.items():
            if key == 'Concept':
                writer.writerow([value])
            else: 
                writer.writerow(value)


    
# 4. find the right concept using wordnet


## creare un ranking per ogni concetto in cui sono presenti i synset (top 5)



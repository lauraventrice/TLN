import csv
import json
import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import Counter
from nltk.wsd import lesk

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
            #tokens.update(def_lem) 
            concept[key] = def_lem  
        else: 
            del concept[key] 
    
    tokens_concepts[concept['Concept']] = list(tokens) 

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

# togliere gli outlier di definizioni

    
# 4. find the right concept using wordnet

def get_top_words(definitions: list, n_top: int): 
    concept_counter = Counter()
    
    for definition in definitions:
        concept_counter.update(definition)
    
    most_frequent_words = [word for word, _ in concept_counter.most_common(n_top)]

    print("top words:", most_frequent_words)

    return most_frequent_words

def get_synset(word: str, definitions: list): 

    synset_counter = Counter()
    for definition in definitions: 
        synset = lesk(definition, word)
        if synset:
            synset_counter.update([synset])

    synset = None
    #print("word:", word)
    if len(synset_counter) != 0:
        synset = synset_counter.most_common(1)[0][0]
        #print("synset:", synset, "- tot volte:", synset_counter.most_common(1)[0][1], " su: ", len(definitions))

    return synset

def create_dict_word_dictionary(most_frequent_words: list, definitions: list):
    dict_word_dictionary = {}
    for word in most_frequent_words:
        for definition in definitions: 
            if word in definition:
                if word in dict_word_dictionary:
                    dict_word_dictionary[word].append(definition)
                else:
                    dict_word_dictionary[word] = [definition]

    return dict_word_dictionary

def onomasiologic_search(concept: dict, n_top: int):
    
    results = []
    del concept['Concept']
    definitions = list(concept.values())

    most_frequent_words = get_top_words(definitions, n_top)
    dict_word_dictionary = create_dict_word_dictionary(most_frequent_words, definitions)

    hyponyms = []
    for word in most_frequent_words:
        synset = get_synset(word, dict_word_dictionary[word])
        if synset:
            hyponyms.extend(synset.hyponyms())
    
    res = []
    for hyp in hyponyms:
        hyp_def = hyp.definition() + " " + ', '.join(hyp.examples())
        #print("DEFINIZIONE: ", hyp_def)
        
        match_words = []
        for word in most_frequent_words:
            if word in hyp_def:
                match_words.append(word) 
        
        res.append([hyp, match_words])

     # sort the list using the number of important words found
    sorted_res = sorted(res, key=lambda x: len(x[1]), reverse=True)
    for synset, match_words in sorted_res[:5]:
        results.append((synset.name(), match_words))

    return results


for concept in definitions:
    print(concept['Concept'])
    result = onomasiologic_search(concept, 15)
    print(result, '\n\n\n')
    



import nltk
import csv 
import json
from nltk.stem import WordNetLemmatizer
import numpy as np
from numpy.linalg import norm
from collections import Counter 
import os 

# 1. read document definitions and create a data structure

defs_path = f'Esercizio1-DEFS/resource/definitions.csv'
defs_path_json = f'Esercizio1-DEFS/resource/definitions.json'
slang_path = f'Esercizio1-DEFS/resource/slang.txt'

if not os.path.exists(defs_path_json):
    with open(defs_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        definitions = []
        for row in reader:
            definitions.append(row)

    with open(defs_path_json, 'w', encoding='utf-8') as f:
        json.dump(definitions, f, indent=4)


with open(defs_path_json, 'r', encoding='utf-8') as f: 
    definitions = json.load(f)


with open(slang_path, 'r', encoding='utf-8') as f:
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

with open(f'Esercizio1-DEFS/resource/preprocessing.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for concept in definitions:
        for key, value in concept.items():
            if key == 'Concept':
                writer.writerow([value])
            else: 
                writer.writerow(value)


# creation of a phrase embedding (one-hot) for each definition 

embeddings_concepts = []

for concept in definitions:
    keys = list(concept.keys())
    keys.remove('Concept')
    embedding_concept = []
    for key in keys:
        definition = concept[key]
        embedding = []
        for token in tokens_concepts[concept['Concept']]:
            if token in definition:
                embedding.append(1)
            else:
                embedding.append(0)
        embedding_concept.append(embedding)
    
    embeddings_concepts.append(embedding_concept)

# 3. similarity between definitions

# cosine similarity between vectors u v
def cosine_sim(u, v):
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.dot(u, v) / (norm(u) * norm(v))

similarities = []
for embedding_concept in embeddings_concepts: 
    sim_matrix_conc = []
    for embedding in embedding_concept:
        similarity_row = []
        for embedding2 in embedding_concept:
            if all(elem == 0 for elem in embedding) and all(elem == 0 for elem in embedding2):
                similarity_row.append(1)
            elif all(elem == 0 for elem in embedding) or all(elem == 0 for elem in embedding2):
                similarity_row.append(0)
            else: 
                cosine_similarity = cosine_sim(embedding, embedding2)
                similarity_row.append(cosine_similarity)
        sim_matrix_conc.append(similarity_row)

    similarities.append(sim_matrix_conc)

with open(f'Esercizio1-DEFS/resource/similarities.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for similarity in similarities:
        for row in similarity:
            writer.writerow(row)
        writer.writerow([])

mean_concepts = []

for similarity_conc in similarities:
    mean_concept = []
    for similarity in similarity_conc:
        mean_def = np.mean(similarity)
        mean_concept.append(mean_def)
    
    mean_conc = np.mean(mean_concept)
    mean_concepts.append(mean_conc)


sim_perc = [sim*100 for sim in mean_concepts]
print("\nSimilarity for each concept: ")
print("\t\t --------------------------")
print("\t\t |  ", round(sim_perc[0], 3), "  |  ", round(sim_perc[1], 3), " |")
print("\t\t |  ", round(sim_perc[2], 3), "  |  ", round(sim_perc[3], 3), " |")
print("\t\t --------------------------")


# 4. statistics about words 

def get_top_words(definitions: list, n_top: int): 
    concept_counter = Counter()
    
    for definition in definitions:
        concept_counter.update(definition)
    
    most_frequent_words = [entry for entry in concept_counter.most_common(n_top)]
    return most_frequent_words

print("\nTop 5 words per concept: ")
for concept in definitions: 
    keys = list(concept.keys())
    print(concept['Concept'])
    keys.remove('Concept')
    top_words = get_top_words(concept.values(), 5)
    print(top_words) 

print("\n-----------------------------\n")
# mean length of definitions for concept
for concept in definitions:
    keys = list(concept.keys())
    keys.remove('Concept')
    length = []
    for key in keys:
        definition = concept[key]
        length.append(len(definition))
    mean_length = np.mean(length)
    print("Mean length for ", concept['Concept'], ": ", round(mean_length, 2))

print("\n-----------------------------\n")
#5. mean similarity values between the two dimensions of concepts

concrete_concept_mean = np.mean([mean_concepts[1], mean_concepts[3]])
abstract_concept_mean = np.mean([mean_concepts[0], mean_concepts[2]])
generic_concept_mean = np.mean([mean_concepts[0], mean_concepts[1]])
specific_concept_mean = np.mean([mean_concepts[2], mean_concepts[3]])

print("Mean similarity for concept type dimension ")
print("Concrete: ", round(concrete_concept_mean, 3))
print("Abstract: ", round(abstract_concept_mean, 3))
print("Generic:  ", round(generic_concept_mean, 3))
print("Specific: ", round(specific_concept_mean, 3))


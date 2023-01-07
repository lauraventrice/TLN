import wikipediaapi
import pandas as pd
import numpy as np
from numpy.linalg import norm
import os
from collections import Counter
import spacy
import nltk 

wiki_wiki = wikipediaapi.Wikipedia('en')
nlp = spacy.load("en_core_web_sm")
stopwords = nltk.corpus.stopwords.words('english')
# 1. Load corpus - Paragraphs from different topics 

file_corpus = f"Esercizio4-Segmentation/resource/corpus.txt"

pages = ["New York City", "Machine Learning", "Vincent van Gogh", "Cubism"]

text = ""
sentences_enumerate = []

if not os.path.exists(file_corpus):
    text_sentences = []
    for page in pages: 
        text_topic_sentences = []
        page_wiki = wiki_wiki.page(page)
        print("Page - Title: %s" % page_wiki.title)
        text_topic = page_wiki.summary
        sections = page_wiki.sections
        for i in range(5): 
            text_topic += sections[i].text.replace("\n", " ")
        #print("Page - Summary: %s" % summary)
        if text == "":  
            text = text_topic
        else:
            text = text + "\n" + text_topic

        text_topic_sentences = [sent.text.strip() for sent in nlp(text_topic).sents if sent.text.strip() != ""]

        text_sentences.extend([' '.join(text_topic_sentences[i:i+4]) for i in range(0, len(text_topic_sentences), 4)])

    sentences_enumerate = list(enumerate(text_sentences))

    with open(file_corpus, "w", encoding='utf-8') as f:
        for index, sentence in sentences_enumerate:
            f.write(str(index) + ": " + sentence + "\n")

else: 
    with open(file_corpus, "r", encoding='utf-8') as f:
        sentences = f.readlines()
        sentences_enumerate = []
        for sentence in sentences: 
            index = sentence.split(":")[0]
            sentence = sentence.split(":")[1]
            sentences_enumerate.append((int(index), sentence))

# cuts: [19, 35, 58]

# 2. Sentences, pre processing and word count

words_sentences = {}
words_text = set()
for index, sentence in sentences_enumerate:
    words_sentence = Counter()
    words = nlp(sentence)
    words_clean = [word.lemma_.lower() for word in words if word.is_alpha and word.text not in stopwords and word.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]]
    
    words_text.update(words_clean)
    words_sentence.update(words_clean)

    words_sentences[index] = words_sentence

words_text = list(words_text) 

# complete encoding of the words in the sentences with 0s
for sentence in words_sentences:    
    words_count = list(words_sentences[sentence].keys())
    for word in words_text: 
        if not word in words_count: 
            words_sentences[sentence][word] = 0

# 3. Detection of words with distribution of frequency not uniform

df = pd.DataFrame(words_sentences)

rows_to_drop = []
for index, row in df.iterrows():
    row_valued = row[row != 0]
    sparsity = len(row_valued) / len(row)
    if sparsity < 0.10 or sparsity > 0.90: # are not meaningful words (too used or too rare)
        rows_to_drop.append(index)

for row_to_drop in rows_to_drop: 
    df.drop(row_to_drop, inplace=True)


# 4. Visualization of the frequency of the words
#with pd.option_context('display.max_rows', None,
#                   'display.max_columns', None,
#                   'display.precision', 3,
#                   ):
#    print(df)


# 5. text segmentation in a casual way 

n_segments = 3
segments = []
width = len(df.columns) // (n_segments + 1)
possible_cuts = list(df.columns[1:-2])

import random

for i in range(n_segments): 
    segment = (width * (i+1)) + 5
    segments.append(segment)
    possible_cuts.remove(segment)
    if segment+1 in possible_cuts: 
        possible_cuts.remove(segment+1)
    if segment-1 in possible_cuts:
        possible_cuts.remove(segment-1)

segments.sort()

print("segments", segments)

def cohesion(centroid, sentence) -> float: 
    return np.linalg.norm(centroid - sentence)

def intra_group_cohesion(df_segment: pd.DataFrame): 
    cohesion_value = 0
    centroid_segment = df_segment.mean(axis=1).to_numpy()
    for index in df_segment.columns: 
        sentence = df_segment[[index]].astype(float).to_numpy() 
        cohesion_sentence = cohesion(centroid_segment, sentence)
        cohesion_value += cohesion_sentence 
    return cohesion_value/len(df_segment.columns)

def segmentation(df: pd.DataFrame, segments_df: list): 
    df_segmented = []
    for segment_df in segments_df: # for each segment chosen
        columns_to_drop = []
        find = False
        for col in df.columns:
            if col == segment_df and not find:
                find = True
            if find:
                columns_to_drop.append(col)
        
        df_new = df.drop(columns_to_drop, axis=1)
        df = df.drop(df_new.columns, axis=1) 
        df_segmented.append(df_new)
   
    df_segmented.append(df)
    return df_segmented

def change_segmentation(segment1: pd.DataFrame, segment2: pd.DataFrame, reverse = False):
    segment1_new = segment1.copy()
    segment2_new = segment2.copy()
    if len(segment1) > 1 and len(segment2) > 1: 
        if reverse:
            first_column = segment2.columns[0]
            segment1_new.insert(len(segment1.columns), first_column, segment2[first_column])
            segment2_new.drop(first_column, axis=1, inplace=True)
        else: 
            last_column = segment1.columns[-1]
            segment1_new.drop(last_column, axis=1, inplace=True)
            segment2_new.insert(0, last_column, segment1[[last_column]])
    
    return segment1_new, segment2_new

def text_segmentation(df: pd.DataFrame, segments: list): # main algorithm
    to_continue = True
    segments.sort()
    while to_continue:    
        new_segments = []
        df_segmented = segmentation(df, segments)
        #print("SEGMENTED:", df_segmented)
        pairs_segments = zip(df_segmented, df_segmented[1:], segments)
        for segment1, segment2, value_segment in pairs_segments: # per tutte le porzioni di testo
            # 6. intra-group cohesion in segments
            cohesion1 = intra_group_cohesion(segment1)
            cohesion2 = intra_group_cohesion(segment2)
            print("COHESION:", cohesion1, cohesion2)

            # 7. search of points with low cohesion -> break point
            # 8. change of the segmentation 
            segment_new1, segment_new2 = change_segmentation(segment1, segment2)
            cohesion1_new = intra_group_cohesion(segment_new1)
            cohesion2_new = intra_group_cohesion(segment_new2)
            print("COHESION NEW REVERSE FALSE: ", cohesion1_new, cohesion2_new)
            if cohesion1_new < cohesion1 and cohesion2_new < cohesion2:
                new_segments.append(value_segment+1)
            else: 
                segment_new1, segment_new2 = change_segmentation(segment1, segment2, True)
                cohesion1_new = intra_group_cohesion(segment_new1)
                cohesion2_new = intra_group_cohesion(segment_new2)
                print("COHESION NEW REVERSE TRUE: ", cohesion1_new, cohesion2_new)
                if cohesion1_new < cohesion1 and cohesion2_new < cohesion2:
                    new_segments.append(value_segment-1)
                else: 
                    new_segments.append(value_segment)
        
        no_change = True
        for value in segments: 
            no_change = no_change and value in new_segments

        if no_change:
            to_continue = False
        else: 
            segments = new_segments
            print("NEW SEGMENTS: ", segments)

    return segments


splits_def = text_segmentation(df, segments)
print("RISULTATI: ", splits_def)
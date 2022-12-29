import nltk 
import wikipediaapi
import pandas as pd
import random
import numpy as np
from numpy.linalg import norm

wiki_wiki = wikipediaapi.Wikipedia('en')
stopwords = nltk.corpus.stopwords.words('english')
# 1. Paragraphs from different topics 

pages = ["New York City", "Artificial Intelligence", "Vincent van Gogh", "Cubism"]

text = ""
for page in pages: 
    page_wiki = wiki_wiki.page(page)
    print("Page - Title: %s" % page_wiki.title)
    summary = page_wiki.summary
    #print("Page - Summary: %s" % summary)
    if text == "": 
        text = summary
    else: 
        text = text + "\n" + summary

# 2. Sentences, pre processing and word count

text_sentences = nltk.sent_tokenize(text)

words_sentences = {}
words_text = []
file_corpus = f"Esercizio4-Segmentation/resource/corpus.txt"
sentences_enumerate = enumerate(text_sentences)

with open(file_corpus, "w", encoding='utf-8') as f:
    for index, sentence in sentences_enumerate:
        words_sentence = {}
        f.write(str(index) + ": " + sentence + "\n")
        words = nltk.word_tokenize(sentence)
        words_clean = [word.lower() for word in words if word.isalpha() and not word.lower() in stopwords]
        lemmatizer = nltk.stem.WordNetLemmatizer()
        words_lemm = [lemmatizer.lemmatize(word) for word in words_clean]
        words_missing = [lemma for lemma in words_lemm if lemma not in words_text]
        words_text.extend(words_missing)
        for lemma in words_lemm: 
            if lemma in words_sentence: 
                words_sentence[lemma] += 1 
            else: 
                words_sentence[lemma] = 1 
        
        words_sentences[index] = words_sentence

# TODO: INSERIRE GLI 0 CON CRITERIO!
for sentence in words_sentences:    
    words_count = list(words_sentences[sentence].keys())
    for word in words_text: 
        if not word in words_count: 
            words_sentences[sentence][word] = 0

# 3. Detection of words with distribution of frequency not uniform

df = pd.DataFrame(words_sentences)

rows_to_drop = []
for index, row in df.iterrows(): # eliminare le parole che hanno una distribuzione uniforme
    #print("ROW:", row)
    row_sparse = row[row != 0]
    #print("ROW SPARSE:", row_sparse)
    sparsity = len(row_sparse) / len(row)
    if sparsity < 0.05 or sparsity > 0.90: 
        rows_to_drop.append(index)

for row_to_drop in rows_to_drop: 
    df.drop(row_to_drop, inplace=True)


# 4. Visualization of the frequency of the words
with pd.option_context('display.max_rows', None,
                   'display.max_columns', None,
                   'display.precision', 3,
                   ):
    print(df)


# 5. text segmentation in a casual way 

n_segments = 3
segments = []
len_columns = len(df.columns)
df_columns = df.columns[2:len_columns-2] 

for i in range(n_segments): 
    segment = random.choice(df_columns) 
    print("SEGMENTO!: ", segment, type(segment))
    segments.append(segment)
    df_columns = df_columns.drop([segment, segment+1])

def cohesion(centroid, sentence) -> float: 
    return np.linalg.norm(centroid - sentence)

def intra_group_cohesion(df_segment: pd.DataFrame): 
    cohesion_value = 0
    centroid_segment = df_segment.mean(axis=1).to_numpy()
    for index in df_segment.columns: 
        sentence = df_segment[[index]].astype(float).to_numpy() 
        cohesion_sentence = cohesion(centroid_segment, sentence)
        cohesion_value += cohesion_sentence # trovare altro modo
    return cohesion_value/len(df_segment.columns)

# 5.1 BEGIN ALGORITHM 

def segmentation(df: pd.DataFrame, segments_df: list): 
    df_segmented = []
    for segment_df in segments_df: 
        columns_to_drop = []
        find = False
        for column in df.columns: 
            find = find or column == segment_df
            if find: 
                columns_to_drop.append(column)
        df_new = df.drop(columns_to_drop, axis=1) # lo segmento con segment_df
        df = df.drop(df_new.columns, axis=1) # il resto
        df_segmented.append(df_new)
   
    df_segmented.append(df) # aggiungo il resto
    return df_segmented

def change_segmentation(segment1: pd.DataFrame, segment2: pd.DataFrame, reverse = False):
    segment1_new = segment1.copy()
    segment2_new = segment2.copy()
    if len(segment1) > 2: 
        if reverse:
            first_column = segment2.columns[0]
            segment1_new.insert(len(segment1.columns), first_column, segment2[first_column])
            segment2_new = segment2.drop(first_column, axis=1)
        else: 
            last_column = segment1.columns[-1]
            segment1_new = segment1.drop(last_column, axis=1)
            segment2_new.insert(0, last_column, segment1[[last_column]])
    
    return segment1_new, segment2_new

def text_segmentation(df: pd.DataFrame, segments: np.array):
    to_continue = True
    segments = np.sort(segments) # parto da quelli casuali
    while to_continue:    
        new_segments = []
        df_segmented = segmentation(df, segments)
        print("SEGMENTED:", df_segmented)
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

        print("NO CHANGE: ", no_change)
        if no_change:
            to_continue = False
        else: 
            segments = new_segments

    print("SPLIT DEFINITIVI:", segments)
    return segments


splits_def = text_segmentation(df, segments)
print("RISULTATI: ", splits_def)
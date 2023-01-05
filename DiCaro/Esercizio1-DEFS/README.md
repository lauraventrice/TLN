## EXERCISE TEXT 

### TITLE: “Defs”: 

- Calculate similarity, seen as lexical overlap, between definitions in the `definitions.csv` document. (intersection cardinality normalized to minimum length between the two, or variants)
- Aggregation on the two dimensions (concreteness/specificity), and results analysis

### Hints:
Experiment using filters, preprocessing, and overlay metrics of your choice 
(e.g., using stemming and stopword removal as preprocessing, calculating top-k frequencies in the
definitions, etc.).

## Resources

slangs file: https://github.com/rishabhverma17/sms_slang_translator

libraries: 

- nltk

## Results

Similarity for each concept:
                 --------------------------
                 |   14.515   |   44.085  |
                 |   13.418   |   37.106  |
                 --------------------------

Top 5 words per concept:
Emotion
[('feeling', 12), ('human', 8), ('feel', 8), ('something', 7), ('state', 4)]
Person
[('human', 29), ('person', 6), ('living', 4), ('individual', 3), ('certain', 3)]
Revenge
[('someone', 14), ('anger', 8), ('feeling', 7), ('action', 6), ('emotion', 6)]
Brick
[('used', 24), ('object', 16), ('material', 16), ('construction', 16), ('build', 13)]

-----------------------------

Mean length for  Emotion :  4.1
Mean length for  Person :  3.48
Mean length for  Revenge :  5.53
Mean length for  Brick :  5.19

-----------------------------

Mean similarity for concept type dimension
Concrete:  0.406
Abstract:  0.14
Generic:   0.293
Specific:  0.253

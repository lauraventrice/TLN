# Semantic resources - Part 2

The exercises that have been chosen to be carried out are as follows: 

- SemEval 
- Automatic Summarization with NASARI
- Conceptual Similarity with WordNet 

***
### SemEval 
##### Semantic Similarity

The task to implement is on Semantic Word Similarity. 
Given a dataset on **Multilingual and Cross-lingual Semantic Word Similarity**, we focus on Semantic Similarity on the Italian language. 
The original dataset is available **[HERE](http://alt.qcri.org/semeval2017/task2/)**

The first operation is to annotate with a semantic similarity score, 50
pairs of terms. The criterion to be used can be found **[HERE](https://alt.qcri.org/semeval2017/task2/index.php?id=data-and-tools)**. 

The file *it.test.data.txt* contains the pairs to be extracted using the function defined in the *semeval_mapper.ipynb* notebook using the developer's last name. 

The result of this step is the file *it.test.data_annotated.txt*. 

Evaluation of the annotated scores is carried out in relation to the similarity obtained using the NASARI vectors in version
embedded (*mini_NASARI.tsv* file), maximizing **cosine similarity**. 

Then **Pearsons and Spearman coefficients** are calculated between (the average of) the hand-annotated scores and those calculated using the NASARI resource. 


##### Sense Identification

The second task is to identify the **senses selected** in the similarity judgment.

The question we ask is this: *which senses did we actually used when we assigned a value of similarity to a pair of terms (e.g., society and culture)?*

To solve this task, we start with the assumption that the two terms function as a disambiguation context for each other.

The output of this part of the exercise, in the *it-test.data_ids_**ANNOTATOR*** files consists of 2 Babel synset IDs and the synset terms. 
The output format then consists of 6 fields (separator between fields the tab, while we use the comma ',' as a separator within the
same field):
`
#Term1 Term2 BS1 BS2 Terms_in_BS1 Terms_in_BS2
car bicycle bn:00007309n bn:00010248n
car,car bicycle,bicycle,bike
`

We again calculate the level of agreement in group annotations, this time using **Cohen's kappa score** (*cohen_kappa_score* from the *sklearn.metrics* library). 

We evaluate the result obtained (i.e., the pair of senses identified, and the relative appropriateness) against the output of a simple system made again using the NASARI vectors, calculating the pair of senses that maximize the similarity score. 

Finally, accuracy is measured here on both individual elements and pairs.

***
### Automatic Summarization

The task is to implement an extractive text summarization algorithm, in which sentences that have higher value or informative words are selected. 
The algorithm consists of the following steps: 
1. identification of the topic to be summarized, identified as a set of lexical NASARI vectors;
2. creation of the context with the terms within the topic
3. extraction of the paragraphs containing the most important terms, using Weighted Overlap. 

The relevance criteria implemented are as follows: 
- cue phrase method: consists of identifying sentences that contain words that indicate that something important is about to be said
- title method: consists of using the title for context creation, with the idea that it is informative about the content of the document. 
- hybrid version with cue phrase and title

NASARI lexical vectors found in the file *dd-small-nasari-15.txt* were used, and the summarized documents are: 
- *Andy-Warhol.txt*
- *Ebola-virus-disease.txt*
- *Life-indoors.txt*
- *Napoleon-wiki.txt*
- *Trump-wall.txt*

Finally, the experiments were performed with different degrees of compression (20%, 30%, 40%). 

Evaluation is performed on the basis of two complimentary metrics: 
- **BLEU** (bilingual evaluation understudy) regarding precision; and
- **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) as regards as recall.


***
### Conceptual Similarity

Given two terms as input, the conceptual similarity task consists of providing a numerical similarity score indicating their
semantic closeness. For example, the similarity between the concepts car and bus might be 0.8 on a scale [0,1], where 0 means that the senses are completely dissimilar, while 1 means identity.
To solve the concept similarity task, it is possible to take advantage of the **WordNet** tree structure.

The input for this exercise is pairs of terms contained in the *WordSim353.csv* file. Each pair is assigned a numerical value [0,10], which represents the similarity between the elements of the pair.

The first part of this exercise is to implement three WordNet-based similarity measures: 
- Wu & Palmer
- Shortest Path
- Leakcock & Chodorow 
For each of these similarity measures, calculate
- Spearman's correlation indices and
- Pearson's correlation indices between the results obtained and the 'target' results in the annotated file.

In the second part, however, it is required to implement **Lesk's algorithm** (!= use existing implementation, e.g., in nltk...).
1. Extract 50 sentences from the *[SemCor corpus](http://web.eecs.umich.edu/~mihalcea/downloads.html)* which is annotated with the synsets of WN, and disambiguate (at least) one noun per sentence. Calculate the accuracy of the implemented system based on the senses annotated in SemCor.
2. Randomize the selection of the 50 sentences and the selection of the term to be
disambiguate, and return the average accuracy over (for example) 10 executions of the program.
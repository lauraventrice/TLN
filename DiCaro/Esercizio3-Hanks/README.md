## Exercise text

### Title: "Hanks"

Choose a transitive verb (at least 2 arguments)
- retrieve from a corpus n (> 200) instances (sentences) in which it is used
- perform parsing and disambiguation (palmer, nltk)
- obtaining senses 
- use WordNet (or CSI) super senses on the arguments (subj and obj in the case of 2 arguments) of the chosen verb
- combine meanings from verbs, automatically following hanks theory
- aggregate the results, calculate the frequencies, print the obtained semantic clusters (semantic types)


## Resources

- corpus: https://www.kaggle.com/datasets/fabiochiusano/medium-articles?resource=download
- SpaCy: for parsing and identification of subjects and objects of the verb
- Wordnet: to identify senses and supersenses (lexname)

## Results 

### List of pairs with supersense and count of occurrence

('noun.artifact', 'noun.communication') 12
('noun.communication', 'noun.communication') 10
('noun.act', 'noun.communication') 10
('noun.person', 'noun.communication') 9
('noun.communication', 'noun.cognition') 8
('noun.artifact', 'noun.act') 7
('noun.group', 'noun.attribute') 7
('noun.person', 'noun.artifact') 7
('noun.act', 'noun.cognition') 6
('noun.person', 'noun.location') 6
('noun.cognition', 'noun.artifact') 6
('noun.act', 'noun.act') 6
('noun.group', 'noun.cognition') 5
('noun.person', 'noun.act') 5
('noun.cognition', 'noun.cognition') 5
('noun.group', 'noun.act') 5
('noun.body', 'noun.event') 4
('noun.group', 'noun.communication') 4
('noun.artifact', 'noun.state') 4
('noun.person', 'noun.attribute') 4
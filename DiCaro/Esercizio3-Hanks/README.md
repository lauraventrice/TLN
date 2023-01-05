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

Synset:  wield.v.02   
Definizion synset:  handle effectively
Semantic use:
noun.body noun.event
Frequency:  2
noun.communication noun.communication 
Frequency:  1
verb.competition noun.communication   
Frequency:  1
noun.communication noun.cognition     
Frequency:  4
noun.person noun.communication        
Frequency:  2
noun.artifact noun.process
Frequency:  1
verb.contact noun.artifact
Frequency:  1
noun.group noun.communication
Frequency:  2
noun.object noun.object
Frequency:  1
noun.communication adj.all
Frequency:  1
noun.communication noun.location
Frequency:  1
noun.artifact noun.act
Frequency:  2
noun.act noun.group
Frequency:  2
noun.cognition noun.artifact
Frequency:  1
noun.group noun.artifact
Frequency:  1
noun.animal noun.communication
Frequency:  1
noun.artifact noun.cognition
Frequency:  1
noun.group noun.attribute
Frequency:  3
noun.person noun.artifact
Frequency:  3
noun.artifact noun.artifact
Frequency:  1
noun.person noun.act
Frequency:  1
noun.body noun.group
Frequency:  1
noun.cognition noun.substance
Frequency:  1
noun.artifact noun.communication
Frequency:  4
adj.all noun.communication
Frequency:  1
noun.body noun.cognition
Frequency:  1
noun.event noun.event
Frequency:  1
verb.stative noun.location
Frequency:  1
noun.body noun.artifact
Frequency:  1
noun.artifact noun.event
Frequency:  1
adj.pert noun.artifact
Frequency:  1
noun.act noun.state
Frequency:  1
noun.act noun.communication
Frequency:  1
noun.person adj.all
Frequency:  1
noun.person noun.location
Frequency:  1
noun.food noun.artifact
Frequency:  1
noun.group noun.cognition
Frequency:  1
noun.cognition noun.attribute
Frequency:  1
noun.act noun.cognition
Frequency:  1



                Synset:  handle.v.04
Definizion synset:  touch, lift, or hold with the hands
Semantic use:
noun.body noun.process
Frequency:  1
noun.communication noun.artifact
Frequency:  1
noun.act noun.location
Frequency:  1
noun.act noun.cognition
Frequency:  1
noun.substance noun.act
Frequency:  1



                Synset:  cover.v.05
Definizion synset:  act on verbally or in some form of artistic expression
Semantic use:
noun.substance noun.attribute
Frequency:  1
noun.animal noun.attribute
Frequency:  1



                Synset:  treat.v.01
Definizion synset:  interact in a certain way
Semantic use:
noun.artifact noun.Tops
Frequency:  1
noun.Tops noun.event
Frequency:  1
noun.location noun.object
Frequency:  1
verb.stative noun.group
Frequency:  1
noun.cognition noun.cognition
Frequency:  1
noun.person noun.artifact
Frequency:  1



                Synset:  manage.v.02
Definizion synset:  be in charge of, act on, or dispose of
Semantic use:
noun.artifact noun.group
Frequency:  2
noun.act noun.cognition
Frequency:  1
noun.act noun.group
Frequency:  1
noun.plant noun.cognition
Frequency:  1
noun.attribute noun.event
Frequency:  1
[Synset('handle.n.01'), Synset('manage.v.02'), Synset('treat.v.01'), Synset('cover.v.05'), Synset('handle.v.04'), Synset('wield.v.02'), Synset('handle.v.06')]
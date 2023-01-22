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

('noun.artifact', 'noun.communication') 9
('noun.communication', 'noun.communication') 8
('noun.person', 'noun.communication') 7
('noun.group', 'noun.cognition') 7
('noun.act', 'noun.cognition') 6
('noun.group', 'noun.attribute') 6
('noun.person', 'noun.artifact') 6
('noun.communication', 'noun.cognition') 5
('noun.artifact', 'noun.act') 5
('noun.cognition', 'noun.cognition') 5
('noun.act', 'noun.communication') 5
('noun.group', 'noun.act') 5
('noun.cognition', 'noun.artifact') 4
('noun.artifact', 'noun.artifact') 4
('noun.person', 'noun.act') 4
('noun.person', 'noun.location') 4
('noun.person', 'noun.attribute') 4
('noun.act', 'noun.act') 4
('noun.body', 'noun.event') 3
('noun.artifact', 'noun.process') 3
('noun.group', 'noun.communication') 3
('noun.body', 'noun.cognition') 3
('noun.person', 'noun.cognition') 3
('noun.cognition', 'noun.communication') 3
('noun.cognition', 'noun.act') 3
('noun.artifact', 'noun.state') 3
('noun.attribute', 'noun.state') 2
('noun.artifact', 'noun.group') 2
('noun.artifact', 'noun.event') 2
('noun.person', 'adj.all') 2
('noun.plant', 'noun.cognition') 2
('noun.cognition', 'noun.attribute') 2
('noun.artifact', 'noun.relation') 2
('noun.cognition', 'noun.event') 2
('noun.attribute', 'noun.communication') 2
('noun.person', 'noun.process') 2
('noun.artifact', 'noun.quantity') 2
('noun.artifact', 'noun.Tops') 2
('noun.relation', 'noun.phenomenon') 2
('verb.competition', 'noun.communication') 1
('verb.contact', 'noun.artifact') 1
('noun.object', 'noun.object') 1
('noun.body', 'noun.process') 1
('noun.communication', 'adj.all') 1
('noun.substance', 'noun.attribute') 1
('noun.communication', 'noun.location') 1
('noun.artifact', 'noun.attribute') 1
('noun.Tops', 'noun.event') 1
('noun.group', 'noun.artifact') 1
('noun.animal', 'noun.communication') 1
('noun.location', 'noun.object') 1
('noun.cognition', 'noun.substance') 1
('adj.all', 'noun.communication') 1
('noun.communication', 'noun.artifact') 1
('noun.event', 'noun.event') 1
('verb.stative', 'noun.location') 1
('noun.body', 'noun.artifact') 1
('noun.animal', 'noun.attribute') 1
('verb.stative', 'noun.cognition') 1
('noun.cognition', 'noun.location') 1
('adj.pert', 'noun.artifact') 1
('noun.act', 'noun.state') 1
('noun.act', 'noun.group') 1
('noun.communication', 'noun.possession') 1
('noun.food', 'noun.artifact') 1
('noun.substance', 'noun.act') 1
('noun.attribute', 'noun.event') 1
('noun.event', 'noun.attribute') 1
('noun.artifact', 'noun.cognition') 1
('verb.motion', 'noun.cognition') 1
('noun.person', 'noun.state') 1
('noun.relation', 'noun.artifact') 1
('verb.change', 'noun.cognition') 1
('noun.act', 'noun.artifact') 1
('noun.animal', 'noun.cognition') 1
('noun.quantity', 'noun.attribute') 1
('noun.attribute', 'noun.possession') 1
('verb.change', 'noun.possession') 1
('noun.artifact', 'noun.person') 1
('noun.state', 'noun.group') 1
('noun.act', 'noun.person') 1
('noun.body', 'noun.communication') 1
('noun.person', 'noun.phenomenon') 1
('adj.all', 'noun.phenomenon') 1
('noun.process', 'noun.communication') 1
('noun.artifact', 'adj.all') 1
('noun.person', 'noun.group') 1
('noun.communication', 'noun.act') 1
('noun.group', 'noun.state') 1
('noun.state', 'noun.act') 1
('noun.group', 'noun.group') 1
('noun.communication', 'noun.person') 1
('noun.attribute', 'noun.act') 1
('noun.body', 'noun.act') 1
('noun.communication', 'noun.state') 1
('noun.quantity', 'noun.person') 1
('noun.group', 'noun.body') 1
('adj.all', 'noun.artifact') 1
('noun.cognition', 'noun.time') 1
('noun.plant', 'noun.artifact') 1
('noun.artifact', 'noun.substance') 1
('noun.body', 'noun.possession') 1
('noun.Tops', 'noun.person') 1
('noun.shape', 'noun.phenomenon') 1
('noun.Tops', 'noun.attribute') 1
('noun.communication', 'noun.relation') 1
('noun.communication', 'noun.phenomenon') 1
('noun.animal', 'noun.feeling') 1
('noun.group', 'noun.Tops') 1
('verb.possession', 'noun.cognition') 1
('noun.person', 'noun.person') 1
('noun.act', 'adj.all') 1
('verb.cognition', 'noun.act') 1
('noun.plant', 'noun.act') 1



                Synset:  wield.v.02
Definizion synset:  handle effectively
Semantic use:
noun.body noun.event
Frequency:  2
noun.communication noun.communication
Frequency:  3
verb.competition noun.communication
Frequency:  1
noun.communication noun.cognition
Frequency:  5
noun.artifact noun.process
Frequency:  2
verb.contact noun.artifact
Frequency:  1
noun.group noun.communication
Frequency:  3
noun.object noun.object
Frequency:  1
noun.communication adj.all
Frequency:  1
noun.communication noun.location
Frequency:  1
noun.attribute noun.state
Frequency:  2
noun.act noun.cognition
Frequency:  3
noun.animal noun.communication
Frequency:  1
noun.group noun.cognition
Frequency:  6
noun.group noun.attribute
Frequency:  5
noun.person noun.artifact
Frequency:  4
noun.artifact noun.artifact
Frequency:  3
noun.person noun.act
Frequency:  4
noun.body noun.cognition
Frequency:  3
noun.artifact noun.communication
Frequency:  6
adj.all noun.communication
Frequency:  1
verb.stative noun.location
Frequency:  1
noun.cognition noun.cognition
Frequency:  2
noun.body noun.artifact
Frequency:  1
noun.artifact noun.act
Frequency:  4
noun.artifact noun.event
Frequency:  2
adj.pert noun.artifact
Frequency:  1
noun.act noun.state
Frequency:  1
noun.act noun.communication
Frequency:  4
noun.person adj.all
Frequency:  2
noun.communication noun.possession
Frequency:  1
noun.person noun.location
Frequency:  4
noun.food noun.artifact
Frequency:  1
noun.cognition noun.attribute
Frequency:  1
noun.person noun.communication
Frequency:  4
noun.cognition noun.artifact
Frequency:  2
noun.event noun.attribute
Frequency:  1
noun.artifact noun.cognition
Frequency:  1
verb.motion noun.cognition
Frequency:  1
noun.person noun.state
Frequency:  1
noun.person noun.attribute
Frequency:  3
noun.artifact noun.relation
Frequency:  2
noun.cognition noun.event
Frequency:  2
verb.change noun.cognition
Frequency:  1
noun.act noun.artifact
Frequency:  1
noun.plant noun.cognition
Frequency:  1
noun.person noun.cognition
Frequency:  3
noun.act noun.act
Frequency:  2
noun.attribute noun.possession
Frequency:  1
noun.artifact noun.person
Frequency:  1
noun.act noun.person
Frequency:  1
noun.attribute noun.communication
Frequency:  1
noun.body noun.communication
Frequency:  1
noun.process noun.communication
Frequency:  1
noun.person noun.process
Frequency:  1
noun.artifact adj.all
Frequency:  1
noun.artifact noun.quantity
Frequency:  1
noun.group noun.act
Frequency:  4
noun.artifact noun.Tops
Frequency:  2
noun.person noun.group
Frequency:  1
noun.group noun.group
Frequency:  1
noun.artifact noun.state
Frequency:  1
noun.communication noun.person
Frequency:  1
noun.attribute noun.act
Frequency:  1
noun.body noun.act
Frequency:  1
noun.communication noun.state
Frequency:  1
noun.group noun.body
Frequency:  1
adj.all noun.artifact
Frequency:  1
noun.cognition noun.time
Frequency:  1
noun.plant noun.artifact
Frequency:  1
noun.artifact noun.substance
Frequency:  1
noun.relation noun.phenomenon
Frequency:  1
noun.body noun.possession
Frequency:  1
noun.Tops noun.person
Frequency:  1
noun.shape noun.phenomenon
Frequency:  1
noun.communication noun.relation
Frequency:  1
noun.cognition noun.communication
Frequency:  2
noun.animal noun.feeling
Frequency:  1
noun.group noun.Tops
Frequency:  1
noun.act adj.all
Frequency:  1
noun.cognition noun.act
Frequency:  1


Summary:

SUPERSENSES SUBJECT
noun.body : 9
noun.communication : 14
verb.competition : 1
noun.artifact : 27
verb.contact : 1
noun.group : 21
noun.object : 1
noun.attribute : 5
noun.act : 13
noun.animal : 2
noun.person : 27
adj.all : 2
verb.stative : 1
noun.cognition : 11
adj.pert : 1
noun.food : 1
noun.event : 1
verb.motion : 1
verb.change : 1
noun.plant : 2
noun.process : 1
noun.relation : 1
noun.Tops : 1
noun.shape : 1


SUPERSENSES OBJECT
noun.event : 6
noun.communication : 28
noun.cognition : 26
noun.process : 3
noun.artifact : 16
noun.object : 1
adj.all : 5
noun.location : 6
noun.state : 6
noun.attribute : 10
noun.act : 17
noun.possession : 3
noun.relation : 3
noun.person : 4
noun.quantity : 1
noun.Tops : 3
noun.group : 2
noun.body : 1
noun.time : 1
noun.substance : 1
noun.phenomenon : 2
noun.feeling : 1



                Synset:  manage.v.02
Definizion synset:  be in charge of, act on, or dispose of
Semantic use:
noun.person noun.communication
Frequency:  1
noun.body noun.process 
Frequency:  1
noun.artifact noun.act
Frequency:  1
noun.cognition noun.artifact
Frequency:  2
noun.artifact noun.group
Frequency:  2
noun.group noun.artifact
Frequency:  1
noun.location noun.object
Frequency:  1
noun.cognition noun.substance
Frequency:  1
noun.act noun.cognition
Frequency:  3
noun.event noun.event
Frequency:  1
noun.animal noun.attribute
Frequency:  1
noun.group noun.cognition
Frequency:  1
noun.act noun.group
Frequency:  1
noun.cognition noun.cognition
Frequency:  2
noun.plant noun.cognition
Frequency:  1
noun.substance noun.act
Frequency:  1
noun.attribute noun.event
Frequency:  1
noun.relation noun.artifact
Frequency:  1
noun.animal noun.cognition
Frequency:  1
noun.act noun.act
Frequency:  1
noun.body noun.event
Frequency:  1
noun.person noun.phenomenon
Frequency:  1
noun.cognition noun.communication
Frequency:  1
adj.all noun.phenomenon
Frequency:  1
noun.group noun.attribute
Frequency:  1
noun.artifact noun.communication
Frequency:  1
noun.group noun.state
Frequency:  1
noun.cognition noun.act
Frequency:  1
noun.state noun.act
Frequency:  1
noun.communication noun.communication
Frequency:  2
noun.quantity noun.person
Frequency:  1
noun.artifact noun.state
Frequency:  2
noun.artifact noun.artifact
Frequency:  1
noun.artifact noun.quantity
Frequency:  1
noun.person noun.person
Frequency:  1
noun.act noun.communication
Frequency:  1
noun.attribute noun.communication
Frequency:  1


Summary:

SUPERSENSES SUBJECT
noun.person : 3
noun.body : 2
noun.artifact : 8
noun.cognition : 7
noun.group : 4
noun.location : 1
noun.act : 6
noun.event : 1
noun.animal : 2
noun.plant : 1
noun.substance : 1
noun.attribute : 2
noun.relation : 1
adj.all : 1
noun.state : 1
noun.communication : 2
noun.quantity : 1


SUPERSENSES OBJECT
noun.communication : 7
noun.process : 1
noun.act : 5
noun.artifact : 5
noun.group : 3
noun.object : 1
noun.substance : 1
noun.cognition : 8
noun.event : 3
noun.attribute : 2
noun.phenomenon : 2
noun.state : 3
noun.person : 2
noun.quantity : 1



                Synset:  cover.v.05
Definizion synset:  act on verbally or in some form of artistic expressionSemantic use:
noun.substance noun.attribute
Frequency:  1
noun.cognition noun.attribute
Frequency:  1
noun.state noun.group
Frequency:  1
noun.Tops noun.attribute
Frequency:  1
noun.act noun.act
Frequency:  1
verb.possession noun.cognition
Frequency:  1
noun.artifact noun.communication
Frequency:  1


Summary:

SUPERSENSES SUBJECT
noun.substance : 1
noun.cognition : 1
noun.state : 1
noun.Tops : 1
noun.act : 1
verb.possession : 1
noun.artifact : 1


SUPERSENSES OBJECT
noun.attribute : 3
noun.group : 1
noun.act : 1
noun.cognition : 1
noun.communication : 1



                Synset:  treat.v.01
Definizion synset:  interact in a certain way
Semantic use:
noun.artifact noun.attribute
Frequency:  1
noun.Tops noun.event
Frequency:  1
verb.stative noun.cognition
Frequency:  1
noun.cognition noun.cognition
Frequency:  1
noun.person noun.artifact
Frequency:  1
noun.person noun.communication
Frequency:  2
noun.artifact noun.process
Frequency:  1
noun.quantity noun.attribute
Frequency:  1
noun.communication noun.communication
Frequency:  3
noun.person noun.process
Frequency:  1
noun.relation noun.phenomenon
Frequency:  1
noun.cognition noun.act
Frequency:  1
noun.person noun.attribute
Frequency:  1
noun.plant noun.act
Frequency:  1


Summary:

SUPERSENSES SUBJECT
noun.artifact : 2
noun.Tops : 1
verb.stative : 1
noun.cognition : 2
noun.person : 5
noun.quantity : 1
noun.communication : 3
noun.relation : 1
noun.plant : 1


SUPERSENSES OBJECT
noun.attribute : 3
noun.event : 1
noun.cognition : 2
noun.artifact : 1
noun.communication : 5
noun.process : 2
noun.phenomenon : 1
noun.act : 2



                Synset:  handle.v.04
Definizion synset:  touch, lift, or hold with the hands
Semantic use: 
noun.communication noun.artifact
Frequency:  1
noun.cognition noun.location
Frequency:  1
verb.change noun.possession
Frequency:  1
noun.person noun.artifact
Frequency:  1
noun.group noun.act
Frequency:  1
noun.communication noun.act
Frequency:  1
noun.communication noun.phenomenon
Frequency:  1
noun.artifact noun.communication
Frequency:  1
verb.cognition noun.act
Frequency:  1


Summary:

SUPERSENSES SUBJECT
noun.communication : 3
noun.cognition : 1
verb.change : 1
noun.person : 1
noun.group : 1
noun.artifact : 1
verb.cognition : 1


SUPERSENSES OBJECT
noun.artifact : 2
noun.location : 1
noun.possession : 1
noun.act : 3
noun.phenomenon : 1
noun.communication : 1
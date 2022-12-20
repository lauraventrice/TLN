# Dialog System - Piton

## Text Project: Dialogue System for trainee Witches or Sorcerers 
Specifications:
1. The DS (ITA or ENG) must impersonate the Severus Piton character. 
The DS is task-based: must interrogate the user on the composition of 3 magical potions to be chosen from [here](https://www.potterpedia.it/?speciale=elenco&categoria=Pozioni).
2. Algorithm: ANALYSIS-DM-GENERATION.

### Analysis: 
2 possible approaches:
- Like Eliza Chatbot: regular expressions on strings.
- With dependencies: use a dependency parser (e.g. Spacy, Stanza, Tint) you look for regularities in the tree. 
Ex: "An ingredient is moon water". 
    - ingredient -nsubj-> water
    - is -cop-> water
    - water -nmod-> moon

### Dialogue Management
The initiative lies with the system to query
- Frame-Based: each potion is represented as a frame to be fill whose slots are the ingredien5 -> Common-ground
- The DM must query about the ingredien5 still missing, possibly proposing true or false answers
- He/she should give a grade and a (sagacious) comment at the end of the interaction
- Backup-strategy
- Memory

### Generation
Define a structure for the Text-Plan and one for the Sentence-Plan. 
Using Simple-NLG. 


### Evaluation 
Analyze at least 3 dialogues (-> report)
- What are the most common errors?
- What linguistic phenomena can you handle?
- Trindi Tick List

## Setup and utils 
### SpaCy setup and utils

**API:** 
https://spacy.io/api

**Token attributes:** 
https://spacy.io/api/token#attributes

`pip install -U spacy`

`python -m spacy download en_core_web_sm`

### GingerIt setup and utils

https://gingerit.readthedocs.io/en/latest/

`pip install gingerit`

### Pandas setup and utils

https://pandas.pydata.org

`pip install pandas`

### SimpleNLG setup and utils

https://github.com/bjascob/pySimpleNLG

`pip install simplenlg`

### Speech recognition setup and utils

https://pypi.org/project/SpeechRecognition/

`pip install SpeechRecognition`
`pip install pyttsx3`

### Random library

`pip install random`

### PyAudio

Install PyAudio on Windows:

`pip install pyaudio`

Install PyAudio on M1 Chip using [this guide](https://stackoverflow.com/questions/68251169/unable-to-install-pyaudio-on-m1-mac-portaudio-already-installed)

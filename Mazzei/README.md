# Dialog System - Piton

## Text Project: Dialogue System for trainee Witches or Sorcerers 
Specifications:
1. The DS (ITA or ENG) must impersonate the Severus Piton character. 
The DS is task-based: must interrogate the user on the composition of 3 magical potions to be chosen from:
https://www.po#erpedia.it/?speciale=elenco&categoria=Pozioni
2. Algorithm: ANALYSIS-DM-GENERATION.

### Analysis: 
2 possible approaches:
- Like Eliza Chatbot: regular expressions on strings.
- With dependencies: use a dependency parser (e.g. Spacy, Stanza, Tint) you look for regularities in the tree. 
Ex: "An ingredient is moon water". 
* ingredient -nsubj-> water
* is -cop-> water
* water -nmod-> moon

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

`pip install -U spacy`

`python -m spacy download en_core_web_sm`

https://spacy.io/api

https://spacy.io/usage/linguistic-features

**Token attributes:**
https://spacy.io/api/token#attributes

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
`pip install pyaudio`


### Random library

`pip install random`

### PyAudio

Install PyAudio on Windows:

`pip install pyaudio`

Install PyAudio on M1 Chip:

1.  Install  `portaudio`

```
brew install portaudio
```

2.  Link  `portaudio`

```
brew link portaudio
```

3.  Copy the path where  `portaudio`  was installed (use it in the next step)

```
brew --prefix portaudio
```

4.  Create  `.pydistutils.cfg`  in your home directory

```
sudo nano $HOME/.pydistutils.cfg
```
then paste the following
```
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
```

5.  Install pyaudio

```
pip install pyaudio
or
pip3 install pyaudio
```

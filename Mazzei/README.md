# Dialog System - Piton

## SpaCy setup

`pip install -U spacy`

`python -m spacy download en_core_web_sm`

# SpaCy utils

https://spacy.io/api

https://spacy.io/usage/linguistic-features

**Token attributes:**
https://spacy.io/api/token#attributes

## GingerIt setup and utils

https://gingerit.readthedocs.io/en/latest/

`pip install gingerit`

## Pandas setup and utils

https://pandas.pydata.org

`pip install pandas`

## SimpleNLG setup and utils

https://github.com/bjascob/pySimpleNLG

`pip install simplenlg`


## Speech recognition setup and utils

https://pypi.org/project/SpeechRecognition/

`pip install SpeechRecognition`
`pip install pyttsx3`
`pip install pyaudio`


## Random library

`pip install random`

## PyAudio

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

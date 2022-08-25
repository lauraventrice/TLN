# correttezza sintattica uso di NLTK???????????
# uso di stanza per il parser a dipendenze
# funzione is_claim per individuare claim negazioni o frasi neutre --cercare lista di parole con accezione pos e ng

#import language_tool_python as lt

class LanguageUnderstanding: 

    def check_sentence(self, sentence: str):
        #uso di language tool per la correttezza sintattica
        # se lo score è minore di 0.5 allora non è comprensibile, altrimenti si corregge per poi essere interpretata dalla parsificazione
        pass
    
    def score_sentence(selft, sentence: str): 
        #calcolo score 1-errori/totale parole PRENDERE DAL SITO
        # usare spacy per splittare in sentence, oppure mi basta la funzione del sito?    
        pass

    def parsing_sentence(self, sentence: str, ingredients: list):
        #uso di stanza per il parser a dipendenze     
        #analizziamo l'albero per individuare i sotto alberi con noun chunks e dove viene detto un ingrediente

        pass
    
    def is_claim(self, sentence: str):
        #dobbiamo capire che fare..
        pass
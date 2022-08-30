import language_tool_python as lt
import spacy
import re

nlp = spacy.load("en_core_web_sm")

class LanguageUnderstanding: 

    def __init__(self, ingredients_available: list):
        self.ingredients_available = ingredients_available 
        

    def interpret_response(self, response: str):
        """ Interprets the response.

        Args:
            response (str): The response to interpret.

        Returns:
            in_potion (list) : The ingredients mentioned as in the potion.
            out_potion (list): The ingredients mentioned as out of the potion.
            y_n (str): The answer to the question if was yes or no. 
            unclear_answer (bool): Whether the sentence is unclear.
        """
        in_potion = []
        not_in_potion = []
        y_n = ""
        unclear_answer = False
        if not str.__contains__(response.lower(), "good morning"):
            
            unclear_answer, correct_sentence = self.check_sentence(response)
            if not unclear_answer: 
                in_potion, not_in_potion, y_n = self.parsing_sentence(correct_sentence)
            
        return in_potion, not_in_potion, y_n, unclear_answer

    def check_sentence(self, sentence: str):
        """ Checks if the sentence is unclear using score_sentence.

        Args:
            sentence (str): The sentence to check.
        
        Returns:
            bool: Whether the sentence is unclear.
            str: The correct sentence.
        """
        score, correct_sentence = self.score_sentence(sentence)
        print("SCORE: ", score)
        unclear = True
        if score > 0.5:
            unclear = False

        return unclear, correct_sentence
    
    def score_sentence(self, sentence: str): 
        """ Scores the sentence using the language tool.

        Args:
            sentence (str): The sentence to score.
        
        Returns:
            float: The score of the sentence.
            str: The correct sentence.
        """
        tool = lt.LanguageTool('en-US')
        errors = tool.check(sentence)
        count_errors = len(errors)

        count_words = len(sentence.split(" "))
        print("")

        # non effettuare correzioni se sono da corregere ingredienti 
        correct_sentence = tool.correct(sentence)

        return 1 - count_errors/count_words, correct_sentence
        

    def parsing_sentence(self, sentence: str):
        """ Parses the sentence.

        Args:
            sentence (str): The sentence to parse.
        
        Returns:
            in_potion (list): The ingredients mentioned as in the potion.
            out_potion (list): The ingredients mentioned as out of the potion.
            y_n (str): The answer to the question if was yes or no.
        """

        #TODO: gestire risposta si/no

        in_potion = []
        out_potion = []
        y_n = ""

        doc = nlp(sentence)

        #TODO cambiare il codice con quello del notebook 
        # avere la lista di ingredienti presenti nella frase
        ingredients_mentioned = []
        sentence = sentence.lower()
        for ingredient in self.ingredients_available:
            if ingredient.lower() in sentence:
                ingredients_mentioned.append(ingredient)
                sentence = sentence.replace(ingredient.lower(), ingredient)
                
        sentence = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), sentence, 1)
        
        # avere la lista di noun chunks data da spacy 
        noun_chunks = doc.noun_chunks
        
        #analizziamo l'albero per individuare i sotto alberi con noun chunks e dove viene detto un ingrediente
        dep_tree = []
        verbs = []
        for token in doc: 
            dep_tree.append((str(token.text), str(token.dep_), str(token.head.text), str(token.tag_),  [child for child in token.children]))

        for node in dep_tree: 
            if node[3] == "VBP": # token.tag_
                verb_context = self.check_verb_context(node)
                verbs.append((str(token.text), verb_context, [child for child in token.children])) 
        
        for verb in verbs: 
            for child in verb[2]: #visita in profondità
                if child[0] in ingredients_mentioned: # che facciamo con i maiuscoli/minuscoli??
                    if verb[1] == "pos":
                        in_potion.append(child[0])
                    else: # negazione
                        out_potion.append(child[0])
                else: 
                    # compound
                    for nephew in child[4]:
                        if nephew[1] == "compound" or nephew[1] == "amod": 
                            ingredients_compound = nephew[0] + " " + child[0] 
                            if ingredients_compound in ingredients_mentioned: 
                                if verb[1] == "pos": 
                                    in_potion.append(ingredients_compound)
                                else: # negazione
                                    out_potion.append(ingredients_compound)
                                # controllo i fratelli per prendere il resto degli ingredienti



    def check_verb_context(self, node: tuple):
        """ Checks the verb context.

        Args:
            node (tuple): The node to check.
        
        Returns:
            context (str) : The context of the verb.
        """

        #usiamo parser a dipendenze per inviduare negazioni o claim
        # ricorda, le negazioni sono avverbi!
        context = "pos" 
        for child in node[4]:
            if str(child.dep_) == "neg":
                context = "neg" 
            
        return context
        
        
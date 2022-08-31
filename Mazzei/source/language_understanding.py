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
                in_potion, not_in_potion, y_n = self.parsing_sentence(response)
            
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
        ingredients_mentioned = []
        sentence = sentence.lower()
        for ingredient in self.ingredients_available:
            if ingredient.lower() in sentence:
                ingredients_mentioned.append(ingredient)
                sentence = sentence.replace(ingredient.lower(), ingredient)
                
        sentence = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), sentence, 1)
        doc = nlp(sentence)
        
        verbs = []
        for token in doc: 
            print(token.text, token.tag_)
            if str(token.tag_) == "VBP" or str(token.tag_) == "VBZ": # token.tag_
                verb_context = self.check_verb_context(token)
                verbs.append((token, verb_context)) 
        
        print("verbs: \n")
        for verb in verbs: 
            print ("{:<15} | {:<15} |".format(str(verb[0]), verb[1]))

        for verb in verbs: 
            print("Children ", verb[0].children)
            ingredients_mentioned_verb = self.deep_search(verb[0], [])
            if verb[1] == "pos":
                in_potion = ingredients_mentioned_verb
            else: # negazione
                out_potion = ingredients_mentioned_verb

        print("in_potion", in_potion)
        print("out_potion", out_potion) 
        return in_potion, out_potion, []


    def deep_search(self, node, ingredients_mentioned: list, is_compound = False): 
        print("NOME NODO", node.text, " TAG ", str(node.tag_))
        if str(node.tag_) == "VBP" or str(node.tag_) == "VBZ": # siamo in root 
            for child in node.children:
                if child.dep_ == "nsubj" or child.dep_ == "attr" or child.dep_ == "ccomp":
                    ingredients_mentioned = self.deep_search(child, ingredients_mentioned)
                    print("ingredients_mentioned", ingredients_mentioned)
            return ingredients_mentioned
        elif any(node.text in ingredient for ingredient in self.ingredients_available) or is_compound:    
            if node.text in self.ingredients_available:
                print("SONO NELL'IF")
                ingredients_mentioned.append(node.text)
                for child in node.children:
                    if child.dep_ == "conj" or child.dep_ == "appos" or child.dep_ == "npadvmod":
                        ingredients_mentioned = self.deep_search(child, ingredients_mentioned)
                return ingredients_mentioned
            else: # controlliamo se c'è possibilità di comporre il nome dell'ingrediente
                print("siamo nell'else")
                is_present = False
                for child in node.children: 
                    is_present = is_present or child.dep_ == "compound" or child.dep_ == "amod" or child.dep_ == "nsubj"
                if not is_present and is_compound:
                    return node.text
                else: 
                    for child in node.children:
                        print("child: ", child.text)
                        if child.dep_ == "compound" or child.dep_ == "amod" or child.dep_ == "nsubj":
                            ingredient_name = self.deep_search(child, ingredients_mentioned, True)
                            ingredient_name = ingredient_name + " " + node.text
                            print("Ingredient name", ingredient_name)
                            if ingredient_name in self.ingredients_available:
                                print("l'ingrediente è presente")
                                ingredients_mentioned.append(ingredient_name)
                            elif is_compound: 
                                return ingredient_name
                        if child.dep_ == "conj" or child.dep_ == "appos" or child.dep_ == "npadvmod" :
                            ingredients_mentioned = self.deep_search(child, ingredients_mentioned) 
                    return ingredients_mentioned
        else: 
            return ingredients_mentioned


    def check_verb_context(self, token):
        """ Checks the verb context.

        Args:
            node (tuple): The node to check.
        
        Returns:
            context (str) : The context of the verb.
        """

        context = "pos" 
        for child in token.children:
            if str(child.dep_) == "neg":
                context = "neg" 
            
        return context
        
        
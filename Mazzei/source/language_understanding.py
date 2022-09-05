import spacy
import re
from gingerit.gingerit import GingerIt

nlp = spacy.load("en_core_web_sm")

class LanguageUnderstanding: 

    def __init__(self, ingredients_available: list):
        self.ingredients_available = ingredients_available 
        

    def interpret_response(self, response: str, intent: str):
        """ Interprets the response.

        Args:
            response (str): The response to interpret.
            intent (str): The intent of the response of the question.
        Returns:
            in_potion (list) : The ingredients mentioned as in the potion.
            out_potion (list): The ingredients mentioned as out of the potion.
            y_n (str): The answer to the question if was yes or no. 
            unclear_answer (bool): Whether the sentence is unclear.
        """
        in_potion = []
        out_potion = []
        y_n = ""
        unclear_answer = False
        if intent != "handshake":
            
            response = self.preprocessing(response)

            unclear_answer = self.check_sentence(response)

            if not unclear_answer: 
                if intent == "ingredients_yes_no" or intent == "question_tricky": # parsing sentence with answer yes or no
                    negative_lemmas = ["no", "not", "'nt"]
                    is_negative = bool([neg_lemma for neg_lemma in negative_lemmas if(neg_lemma in response.lower())])

                    if is_negative:
                        y_n = "no"
                    else: 
                        y_n = "yes"
                else:
                    unclear_answer = len(self.contains_ingredients(response)) == 0
                    if not unclear_answer:
                        in_potion, out_potion = self.parsing_sentence(response)
                        if in_potion == [] and out_potion == []:
                            unclear_answer = True
        
        print("IN POTION in language understanding: \n \n \n ", in_potion, "\n \n \n")
        print("YES NO ANSWER, ", y_n)
        return in_potion, out_potion, y_n, unclear_answer

    def contains_ingredients(self, sentence: str):
        """ Checks if the sentence contains ingredients.

        Args:
            sentence (str): The sentence to check.
        
        Returns:
            list: The ingredients mentioned in the sentence.
        """

        ingredients_mentioned = []
        for ingredient in self.ingredients_available:
            if ingredient.lower() in sentence.lower():
                ingredients_mentioned.append(ingredient)
        
        return ingredients_mentioned

    def check_sentence(self, sentence: str):
        """ Checks if the sentence is unclear using score_sentence.

        Args:
            sentence (str): The sentence to check.
        
        Returns:
            bool: Whether the sentence is unclear.
            str: The correct sentence.
        """
        score = self.score_sentence(sentence)
        print("SCORE: ", score)
        unclear = True
        if score > 0.5:
            unclear = False

        return unclear
    
    def score_sentence(self, sentence: str): 
        """ Scores the sentence using the language tool.

        Args:
            sentence (str): The sentence to score.
        
        Returns:
            float: The score of the sentence.
        """

        """"
        tool = lt.LanguageTool('en-US')
        errors = tool.check(sentence)
        """

        parser = GingerIt()
        errors = parser.parse(sentence)
        count_errors = len(errors["corrections"])

        count_words = len(sentence.split(" "))

        
        return 1 - count_errors/count_words
    
    def preprocessing(self, sentence: str): 
        ingredients_mentioned = []
        # preprocessing
        sentence = sentence.lower()
        for ingredient in self.ingredients_available:
            if ingredient.lower() in sentence:
                ingredients_mentioned.append(ingredient)
                sentence = sentence.replace(ingredient.lower(), ingredient)
                
        sentence = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), sentence, 1)

        sentence = " ".join(sentence.split()) # delete double spaces

        sentence = re.sub(r'(?<=[.,])(?=[^\s])', r' ', sentence) # add space after comma and dot if there is no space

        print("AFTER PRE PROCESSING: ", sentence)
        return sentence

    def parsing_sentence(self, sentence: str):
        """ Parses the sentence.

        Args:
            sentence (str): The sentence to parse.
        
        Returns:
            in_potion (list): The ingredients mentioned as in the potion.
            out_potion (list): The ingredients mentioned as out of the potion.
        """

        in_potion = []
        out_potion = []
        doc = nlp(sentence)

        ingredients_mentioned = self.contains_ingredients(sentence)
        
        verbs = []
        for token in doc: 
            print(token.text, token.tag_)
            if str(token.tag_) == "VBP" or str(token.tag_) == "VBZ" or str(token.tag_) == "VB": 
                verb_context = self.check_verb_context(token)
                verbs.append((token, verb_context)) 
        
        print("verbs: \n")
        for verb in verbs: 
            print ("{:<15} | {:<15} |".format(str(verb[0]), verb[1]))

        if verbs: 
            for verb in verbs:
                ingredients_mentioned_verb = self.deep_search(verb[0], [])
                print("\n \n VERB: ", verb[0].text, " ingredients_mentioned_verb: ", ingredients_mentioned_verb, "\n \n")
                if verb[1] == "pos":
                    in_potion = list(set(in_potion + ingredients_mentioned_verb))
                else: # negazione
                    out_potion = list(set(out_potion + ingredients_mentioned_verb))

            # if an ingredient is in both list in_potion and out_potion, it has to be only in out_potion
            in_potion = list(set(in_potion).difference(set(out_potion)))

            print("in_potion", in_potion)
            print("out_potion", out_potion) 

            check_parsing = self.check_parsing_ingredients(ingredients_mentioned, in_potion, out_potion)

            if not check_parsing:
                in_potion = []
                out_potion = []
        else: 
            print("NON HO UN VERBO!")
            in_potion = ingredients_mentioned

       

        return in_potion, out_potion

    def check_parsing_ingredients(self, ingredients_mentioned: list, in_potion: list, out_potion: list):
        """ Checks if the all ingredients mentioned are correct parsed in the sentence.

        Args:
            ingredients_mentioned (list): The ingredients mentioned in the sentence.
            in_potion (list): The ingredients mentioned as in the potion.
            out_potion (list): The ingredients mentioned as out of the potion.
        
        Returns:
            bool: Whether the parsing is correct.
        """
        are_recognized = True
        for ingredient in ingredients_mentioned:
            are_recognized = are_recognized and (ingredient in in_potion or ingredient in out_potion)
        
        return are_recognized

    def deep_search(self, node, ingredients_mentioned: list, is_compound = False): 
        print("NOME NODO", node.text, " TAG ", str(node.tag_))
        if str(node.tag_) == "VBP" or str(node.tag_) == "VBZ" or str(node.tag_) == "VB":  
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
            else: # check if there is the chance to compund the name of the ingredient
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
        
        
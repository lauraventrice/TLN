import language_tool_python as lt
import spacy

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
        if not response.__contains__("Good Morning Professor.") and \
            not response.__contains__("Good Morning"):
            
            unclear_answer, correct_sentence = self.check_sentence(response)
            if not unclear_answer: 
                in_potion, not_in_potion, y_n = self.parsing_sentence(correct_sentence, self.ingredients_available)
            
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
        unclear = True
        if score < 0.5:
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

        correct_sentence = tool.correct(sentence)

        return 1 - count_errors/count_words, correct_sentence
        

    def parsing_sentence(self, sentence: str, ingredients: list):
        """ 
        """

        #analizziamo l'albero per individuare i sotto alberi con noun chunks e dove viene detto un ingrediente

        pass
    
    def is_claim(self, sentence: str):
        #usiamo parser a dipendenze per inviduare negazioni o claim
        # ricorda, le negazioni sono avverbi!
        pass
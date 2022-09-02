# sfrutta la memoria per diversi output possibili: 
# - saluti
# - inizio esame
# - risposta giusta e continuo
# - risposta sbagliata e continuo
# - input incomprensibile e chiede di ripetere
# - fine esame e valutazione

# Uso di simpleNLG per generare risposte

# Usiamo pyttsx3 per generare audio????? o alternative!!!!!!!!!!

from unicodedata import name
from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *
import numpy as np
import pandas 
import random 

class ResponseGenerator: 

    CONTEXT_ANSWERS = ["greetings", "init_exam", "feedback_continue", "unclear_input", "end_exam_eval", "restart"]

    @classmethod
    def generate_answer(cls, current_intent: str, to_ask = "generic", memory = None, unclear_answer = False, name_potion = ""): 
        """Generates an answer for the current intent based on memory.
        
        Args:
            memory (pandas.DataFrame): The memory of the system.
            current_intent (str): The current intent of the system.
            unclear_answer (bool, optional): Whether the answer is unclear. Defaults to False. Based on language_understanding module.
        """
        print("\n CURRENT INTENT response_generation: \n", current_intent, "\n")
        print("\n TO ASK: \n", to_ask, "\n")

        if unclear_answer: 
            return cls.generate_unclear_answer()
        elif current_intent == "handshake":
            return cls.generate_greetings()
        elif current_intent == "ingredients_generic":
            return cls.generate_ingredient_generic(name_potion)
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky":
            return cls.generate_feedback_continue(to_ask, name_potion)
        elif current_intent == "evaluation":
            return cls.generate_end_exam_eval()
        elif current_intent == "restart":
            return cls.generate_restart(to_ask)
        else:
            return "I don't know what to say."

    @classmethod
    def generate_greetings(cls): #rispondiamo a partire da una lista di possibili risposte
        
        possible_sentences = ["Good morning Mr Potter.", "Welcome to the potions examination Mr Potter."]
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
   
        return possible_sentences[choose_sentence[0]]

    @classmethod
    def generate_ingredient_generic(cls, name_potion : str): #rispondiamo a partire da una lista di possibili risposte
        
        if str.__contains__(name_potion.lower(), "potion"):
            possible_sentences = ["Mr. Potter tell me the ingredients of the " + name_potion + ".", \
                "Mr. Potter can you tell me the ingredients of the " + name_potion + " ?",   \
                    "Mr. Potter could you tell me the ingredients of the " + name_potion + " ?"]
        else:    
            possible_sentences = ["Mr. Potter tell me the ingredients of the " + name_potion + " potion.", \
                "Mr. Potter can you tell me the ingredients of the " + name_potion + " potion?",   \
                    "Mr. Potter could you tell me the ingredients of the " + name_potion + " potion?"]
        
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
   
        return possible_sentences[choose_sentence[0]]
    
    @classmethod
    def generate_feedback_continue(cls, intent: str, to_ask = "", name_potion = ""): #usiamo simpleNLG per generare risposte 
        if intent == "ingredients_yes_no":
            cls.generate_question_yes_no(to_ask, name_potion)
        else:
            cls.generate_tricky_question(to_ask)
        pass
    
    @classmethod
    def generate_end_exam_eval(cls): #rispondiamo a partire da una lista di possibili risposte
        pass
    
    @classmethod
    def generate_restart(cls, to_ask: str): #rispondiamo a partire da una lista di possibili risposte
        pass    

    @classmethod
    def generate_unclear_answer(cls): #rispondiamo a partire da una lista di possibili risposte
        print("\n UNCLEAR ANSWER response_generation: \n")
        pass

    # forse alla fine di questa fase ci conviene restituire sia la domanda da stampare che la domanda attesa??

    @classmethod
    def generate_question_yes_no(cls, to_ask: str, name_potion: str): #generiamo la domanda che prevede si/no come risposta
        lexicon = Lexicon.getDefaultLexicon()
        realiser = Realiser(lexicon)
        nlgFactory = NLGFactory(lexicon)

        random_indexes = list(random.sample(range(0, 5), 1))

        if random_indexes[0] == 0:
            ## Do you think that INGNAME is present in POTNAME? - YES/NO
            p = nlgFactory.createClause("you", "think")
            p0 = nlgFactory.createClause(to_ask, "be present", "in " + name_potion + " potion")
            p.addComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 1:
            ## Is INGNAME present in the POTNAME potion? - YES/NO
            p = nlgFactory.createClause("INGNAME", "be present", "in the POTNAME potion")
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 2:
            ## Do you think INGNAME is an ingredient of this potion? - YES/NO
            p = nlgFactory.createClause("you", "think")
            p0 = nlgFactory.createClause("INGNAME", "be", "this potion")
            p0.setIndirectObject("an ingredient of")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 3:
            #Is INGNAME in the ingredient list of the POTNAME potion? - YES/NO
            p = nlgFactory.createClause("INGNAME", "be", "of the POTNAME potion")
            p.setIndirectObject("in the ingredient list")
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 4:
            ## Would you be able to tell me if INGNAME is an ingredient in the potion? - YES/NO
            p = nlgFactory.createClause("you")
            verb = nlgFactory.createVerbPhrase("be able to tell me")
            verb.setFeature(Feature.MODAL, "would")
            p.setVerbPhrase(verb)
            p0 = nlgFactory.createClause("INGNAME", "be", "this potion")
            p0.setIndirectObject("an ingredient in")
            p0.setFeature(Feature.COMPLEMENTISER, "if")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)

        phrase = realiser.realiseSentence(p)

        return phrase

    @classmethod
    def generate_tricky_question(cls, to_ask: str): #generiamo la domanda trabocchetto
        lexicon = Lexicon.getDefaultLexicon()
        realiser = Realiser(lexicon)
        nlgFactory = NLGFactory(lexicon)

        if to_ask == "question_tricky": # qua non bisogna usare l'ingrediente
            random_indexes = list(random.sample(range(0, 2), 1))

            if random_indexes[0] == 0:
                # Are you sure that all the ingredients have been listed? - tricky
                p = nlgFactory.createClause("you", "be sure")
                p0 = nlgFactory.createClause("all the ingredients", "have been listed")
                p.setComplement(p0)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            else:
                # Are you sure you have mentioned all the ingredients? - tricky
                p = nlgFactory.createClause("you", "be sure")
                p0 = nlgFactory.createClause("you", "have mentioned", "all the ingredients") # o al posto di mentioned anche reported
                p.setComplement(p0)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        else: # qua bisogna usare l'ingrediente
            ## Are you sure that INGNAME is an ingredient of this potion? - tricky
            p = nlgFactory.createClause("you", "be sure")
            p0 = nlgFactory.createClause(to_ask, "be", "this potion")
            p0.setIndirectObject("an ingredient of")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        
        phrase = realiser.realiseSentence(p)   
        
        return phrase
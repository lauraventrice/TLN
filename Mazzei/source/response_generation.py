from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *
import pandas as pd
import random 

class ResponseGenerator: 

    CONTEXT_ANSWERS = ["greetings", "init_exam", "feedback_continue", "unclear_input", "end_exam_eval", "restart"]

    @classmethod
    def generate_answer(cls, current_intent: str, to_ask = "", memory = None, unclear_answer = False, name_potion = ""): 
        """Generates an answer for the current intent based on memory.
        
        Args:
            memory (pandas.DataFrame): The memory of the system.
            current_intent (str): The current intent of the system.
            unclear_answer (bool, optional): Whether the answer is unclear. Defaults to False. Based on language_understanding module.

        Returns:
            str: The answer to the current intent.
        """

        if unclear_answer: 
            return cls.generate_unclear_answer()
        elif current_intent == "handshake":
            return cls.generate_greetings()
        elif current_intent == "ingredients_generic":
            return cls.generate_ingredient_generic(to_ask, name_potion, memory)
        elif current_intent == "ingredients_yes_no" or current_intent == "question_tricky":
            return cls.generate_feedback_continue(current_intent, to_ask, name_potion)
        elif current_intent == "evaluation_end":
            return cls.generate_end_exam_eval(to_ask)
        elif current_intent == "restart":
            return cls.generate_restart(name_potion)
        else:
            return "I don't know what to say."

    @classmethod
    def generate_greetings(cls): 
        
        possible_sentences = ["Good morning Mr Potter.", "Welcome to the potions examination Mr Potter.", \
            "Good morning Mr Potter, I hope that you have studied this time.", "Good morning Potter, I hope you are better prepared than last time. "]
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
   
        return possible_sentences[choose_sentence[0]]

    @classmethod
    def generate_ingredient_generic(cls, to_ask: str, name_potion: str, memory: pd.DataFrame): 
        if to_ask == "start_ingredients_generic":
            begin_sentence = "Mr. Potter, "
            phrase = cls.choose_phrase(name_potion)

            return begin_sentence + phrase
        else: # to_ask == "remaining_ingredients"       
            lexicon = Lexicon.getDefaultLexicon()
            realiser = Realiser(lexicon)
            nlgFactory = NLGFactory(lexicon)

            random_indexes = list(random.sample(range(0, 4), 1))

            index_last_value = len(memory.index) - 1
            last_value = memory.loc[index_last_value] 
            
            print("\n \n LAST_VALUE: ", last_value, "\n \n")
            count_correct = 0
            count_incorrect = 0
            count_indiff = 0
        
            
            correct_ingredients = [ingredient for ingredient in last_value["Correct ingredients"].split(",") if ingredient != ""]
            count_correct += len(correct_ingredients)

            incorrect_ingredients = [ingredient for ingredient in last_value["Incorrect ingredients"].split(",") if ingredient != ""]
            count_incorrect += len(incorrect_ingredients)

            indifferent_ingredients = [ingredient for ingredient in last_value["Indifferent ingredients"].split(",") if ingredient != ""]
            count_indiff += len(indifferent_ingredients)
            
            print("SCELTA COMMMENTO count_correct: ", count_correct)
            print("SCELTA COMMMENTO count_incorrect: ", count_incorrect)
            print("SCELTA COMMMENTO count_indiff: ", count_indiff)

            comment = ""

            # scelta commento alla risposta precedente
            good_answer = ["You are right Potter, but ", "Good Job Potter! ", "Well done Potter, but ", "That's right Potter! ", "That's correct Potter! "]
            bad_answer = ["You are wrong as usual! ", "Nice try but of course you are wrong. ", "That's not correct Potter! "]
            indifferent_answer = ["Answer me in a meaningful way Potter! "]
            neutral_answer = ["I see you confused Potter! "]

            if count_indiff >= 1:
                random_indexes = list(random.sample(range(0, len(indifferent_answer)), 1))
                comment = indifferent_answer[random_indexes[0]]
            elif count_correct >= 1 and count_incorrect == 0:
                random_indexes = list(random.sample(range(0, len(good_answer)), 1))
                comment = good_answer[random_indexes[0]]
            elif count_incorrect >= 1 and count_correct == 0:
                random_indexes = list(random.sample(range(0, len(bad_answer)), 1))
                comment = bad_answer[random_indexes[0]]
            else:
                random_indexes = list(random.sample(range(0, len(neutral_answer)), 1))
                comment = neutral_answer[random_indexes[0]]
            
            # generazione prossima domanda
            if random_indexes[0] == 0:
                # You should tell me some more ingredients.
                p = nlgFactory.createClause("you")
                verb = nlgFactory.createVerbPhrase("tell")
                p.setObject("some more ingredients")
                p.setVerb(verb)
                verb.setFeature(Feature.MODAL, "should")
                verb.setPostModifier("me")
                phrase = realiser.realiseSentence(p)
            elif random_indexes[0] == 1:
                ## What are the remaining ingredients? 
                p = nlgFactory.createClause("the remaining ingredients")
                verb = nlgFactory.createVerbPhrase("be")
                verb.setPlural(True)
                p.setVerbPhrase(verb)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
                phrase = realiser.realiseSentence(p)
            elif random_indexes[0] == 2:
                ## What are the other ingredients? 
                p = nlgFactory.createClause("the other ingredients")
                verb = nlgFactory.createVerbPhrase("be")
                verb.setPlural(True)
                p.setVerbPhrase(verb)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
                phrase = realiser.realiseSentence(p)
            elif random_indexes[0] == 3:
                ## What ingredients are left? 
                p = nlgFactory.createClause("the ingredients")
                p.setPlural(True)
                verb = nlgFactory.createVerbPhrase("be left")
                p.setVerbPhrase(verb)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
                phrase = realiser.realiseSentence(p)
                
            if str.__contains__(comment, "but"):
                phrase = cls.decapitalize(phrase)

            return comment + phrase


    @classmethod

    def decapitalize(s):
        if not s:  # check that s is not empty string
            return s
        return s[0].lower() + s[1:]


    @classmethod
    def choose_phrase(cls, name_potion: str):
        """ Choose a phrase to ask ingredients of the potion, in a random way.

        Args:
            name_potion (str): The name of the potion.
        
        Returns:
            str: The phrase to ask ingredients of the potion.
        """
        if str.__contains__(name_potion.lower(), "potion"):
                possible_sentences = ["tell me the ingredients of the " + name_potion + ".", \
                    "can you tell me the ingredients of the " + name_potion + " ?",   \
                        "could you tell me the ingredients of the " + name_potion + " ?"]
        else:    
            possible_sentences = ["tell me the ingredients of the " + name_potion + " potion.", \
                "can you tell me the ingredients of the " + name_potion + " potion?",   \
                    "could you tell me the ingredients of the " + name_potion + " potion?"]
        
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))

        return possible_sentences[choose_sentence[0]]

    @classmethod
    def generate_feedback_continue(cls, intent: str, to_ask: str, name_potion: str): #use of simpleNLG to generate answer 
        if intent == "ingredients_yes_no":
            phrase = cls.generate_question_yes_no(to_ask, name_potion)
        else:
            phrase = cls.generate_tricky_question(to_ask)
        
        return phrase
    
    @classmethod
    def generate_end_exam_eval(cls, evaluation: str): 
        """ Generates the end of the exam with evaluation in to_ask.

        Args:
            evaluation (str): The evaluation of the exam.

        Returns:
            str: The end of the exam with evaluation.
        """

        phrases_end = ["This exam is over. ", "This exam has ended. ", "This examination is now over. ", "This is the end of this exam. "]
        choose_end = list(random.sample(range(0, len(phrases_end)), 1))
        phrase_end = phrases_end[choose_end[0]]

        if evaluation == "insufficient" or evaluation == "failure": 
            possible_comments = ["You failed the exam, Potter. ", "You didn't pass the exam, Potter. "]
        elif evaluation == "mediocre": 
            possible_comments = ["You should study more Potter! You haven't studied enough, you've passed the exam with the minimum mark. ",
                    "You have studied as little as your usual Potter. "]
        else: 
            possible_comments = ["You passed the exam, but there is still a long way to go. ", "At the limit of decency Potter, you saved yourself this time. "\
                "You got away with it in the end, Potter. "]

        choose_comment = list(random.sample(range(0, len(possible_comments)), 1))
        phrase_comment = possible_comments[choose_comment[0]]

        phrase_evaluation = "Your final grade for this exam is " + evaluation.upper() + "."
        
        return phrase_end + phrase_comment + phrase_evaluation
    
    @classmethod
    def generate_restart(cls, name_potion: str): 
        possible_start = ["Next question, ", "Perhaps we should change potions, ", "Let's try another question, ", "Let's try another potion, "]
        
        choose_start = list(random.sample(range(0, len(possible_start)), 1))
        phrase_start = possible_start[choose_start[0]]

        phrase = cls.choose_phrase(name_potion)

        return phrase_start + phrase

    @classmethod
    def generate_unclear_answer(cls): 
        """ Generates an answer if the answer of the user is unclear. 
        The answer has to ask to repeat the answer of the user.

        Returns:
            str: The answer.
        """
        possible_sentences = ["Your answer was unclear, please try again.", "I didn't understand, could you repeat?", \
            "I didn't understand, could you say it again?", "I didn't get it, could you repeat?"]
        
        choose_sentence = list(random.sample(range(0, len(possible_sentences)), 1))
   
        return possible_sentences[choose_sentence[0]]

    @classmethod
    def generate_question_yes_no(cls, to_ask: str, name_potion: str): 
        """ Generate a yes/no question about a particular ingredient in a potion.

        Args:
            to_ask (str): The ingredient to ask about.
            name_potion (str): The name of the potion.
        
        Returns:
            str: The generated question.
        """
        lexicon = Lexicon.getDefaultLexicon()
        realiser = Realiser(lexicon)
        nlgFactory = NLGFactory(lexicon)

        random_indexes = list(random.sample(range(0, 5), 1))

        if random_indexes[0] == 0:
            ## Do you think that INGNAME is present in POTNAME? 
            p = nlgFactory.createClause("you", "think")
            p0 = nlgFactory.createClause(to_ask, "be present", "in " + name_potion + " potion")
            p.addComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 1:
            ## Is INGNAME present in the POTNAME potion? 
            p = nlgFactory.createClause(to_ask, "be present", "in the "  + name_potion + " potion")
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 2:
            ## Do you think INGNAME is an ingredient of this potion? 
            p = nlgFactory.createClause("you", "think")
            p0 = nlgFactory.createClause(to_ask, "be", "this potion")
            p0.setIndirectObject("an ingredient of")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 3:
            ## Is INGNAME in the ingredient list of the POTNAME potion? 
            p = nlgFactory.createClause(to_ask, "be", "of the " + name_potion + " potion")
            p.setIndirectObject("in the ingredient list")
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        elif random_indexes[0] == 4:
            ## Would you be able to tell me if INGNAME is an ingredient in the potion? 
            p = nlgFactory.createClause("you")
            verb = nlgFactory.createVerbPhrase("be able to tell me")
            verb.setFeature(Feature.MODAL, "would")
            p.setVerbPhrase(verb)
            p0 = nlgFactory.createClause(to_ask, "be", "this potion")
            p0.setIndirectObject("an ingredient in")
            p0.setFeature(Feature.COMPLEMENTISER, "if")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)

        phrase = realiser.realiseSentence(p)

        return phrase

    @classmethod
    def generate_tricky_question(cls, to_ask: str):
        """ Generate a tricky question with specified ingredient or not. 

        Args:
            to_ask (str): ingredient to ask
        
        Returns:
            str: generated question
        """
        lexicon = Lexicon.getDefaultLexicon()
        realiser = Realiser(lexicon)
        nlgFactory = NLGFactory(lexicon)

        if to_ask == "question_tricky": # question without specified ingredient
            random_indexes = list(random.sample(range(0, 2), 1))

            if random_indexes[0] == 0:
                ## Are you sure that all the ingredients have been listed?
                p = nlgFactory.createClause("you", "be sure")
                p0 = nlgFactory.createClause("all the ingredients", "have been listed")
                p.setComplement(p0)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            else:
                ## Are you sure you have mentioned all the ingredients?
                p = nlgFactory.createClause("you", "be sure")
                p0 = nlgFactory.createClause("you", "have mentioned", "all the ingredients")
                p.setComplement(p0)
                p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        else: # question with specified ingredient
            ## Are you sure that INGNAME is an ingredient of this potion?
            p = nlgFactory.createClause("you", "be sure")
            p0 = nlgFactory.createClause(to_ask, "be", "this potion")
            p0.setIndirectObject("an ingredient of")
            p.setComplement(p0)
            p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        
        phrase = realiser.realiseSentence(p)   
        
        return phrase
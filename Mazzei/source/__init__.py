import csv

from dialogue_manager import DialogueManager
from dialogue_system import DialogueSystem
from language_understanding import LanguageUnderstanding
import warnings

warnings.filterwarnings('ignore')

POTIONS_DIR = f"Mazzei/data/potions.csv"
INGREDIENTS_DIR = f"Mazzei/data/ingredients.csv"

def load_config():
    """Loads the configuration of the system (potions and ingredients).
    """
    potions = load_potions()
    ingredients = load_ingredients()
    return potions, ingredients

def load_potions():
    """Loads the potions from the csv file.
    """
    potions_dict = {}

    with open(POTIONS_DIR) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            potions_dict[row[0]] = row[1:len(row)]

    return potions_dict

def load_ingredients():
    """Loads the ingredients from the csv file.
    """
    ingredients = []
    with open(INGREDIENTS_DIR) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            ingredients.append(row[0])

    return ingredients

def main():
    dialogue_manager = DialogueManager()
    potions, ingredients = load_config()
    language_understanding = LanguageUnderstanding(ingredients)
    dialogue_manager.set_ingredients(ingredients)
    dialogue_manager.choose_potions(potions)
    dialogue_system = DialogueSystem(dialogue_manager, language_understanding)
    dialogue_system.start_dialogue()


main()
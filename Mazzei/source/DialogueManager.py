#Dialog control: definisce l'Intent sulla base della memoria

#Dialog context: mantiene lo storico della conversazione, la common ground, 
#con una memoria dell'interazione, frame delle pozioni e intent per il tipo di domanda

# si sceglie la pozione su cui interrogare, processa l'input e aggiorna la memoria

# Parte 1:
# - funzione che carica un file con tutte le pozioni
# - crea dizionario con chiave nome della pozione e valore lista ingredienti
# - crea lista di ingredienti completa

# Parte 2:
# - scelta di 3 pozioni random dal dizionario
# - creazione dei frame relativi alle pozioni solo con nome e campi vuoti (forse sarà un oggetto??)

# Parte 3:
# - gestione degli intent tipo automa, come se fosse lo stato della conversazione, dataflow: 
#   1. handshake
#   2. chiedi ingredienti ("Quali sono gli ingredienti di questa pozione?" oppure "Quali sono il resto degli ingredienti?" oppure "Quindi quali sono gli ingredienti?") 
#   2. chiedi se un particolare ingrediente è presente negli ingredienti della pozione (PIù DI UNA VOLTA)
#   3. chiede se è sicuro della presenza di un ingrediente citato precedentemente o se sono stati citati tutti (SI DEVE POI RITORNARE A 2 o 4)
#   4. evaluation con voto e mini commento 


# Parte 4:
# - gestione della memoria con intent-domanda-risposta DECIDERE

import pandas as pd
import csv
import os
import random

def create_data_frame(columnName, rowNum):
    df = pd.DataFrame(index=range(rowNum),columns=[columnName])
    return df

# Parte 1

def read_potions():
    dictionary = {} 

    #cur_path = os.path.dirname(__file__)
    #cur_path = cur_path.replace('/source', '')
    #filename = os.path.join(cur_path, 'data', 'potions.csv')

    postions_numbers = 0

    filename = f"Mazzei/data/potions.csv"

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            dictionary[row[0]] = row[1:len(row)]
            postions_numbers += 1

    return dictionary, postions_numbers

def read_ingredients():
    ingredients = []

    #cur_path = os.path.dirname(__file__)
    #cur_path = cur_path.replace('/source', '')
    #filename = os.path.join(cur_path, 'data', 'ingredients.csv')

    filename = f"Mazzei/data/ingredients.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            ingredients.append(row[0])

    return ingredients


def create_list_of_data_frame():
    potions_dictionary, postions_numbers = read_potions()
    ingredients_list =  read_ingredients()  #TODO: questo serve da un'altra parte mi sa

    # Parte 2
    random_indexes = list(random.sample(range(1, postions_numbers), 3))

    data_frame_list = []

    # Prendi la pozione a indice index1
    for i in range(len(random_indexes)):
        potion_name = list(potions_dictionary.keys())[random_indexes[i]]
        potion_ingredients = list(potions_dictionary.values())[random_indexes[i]]
        df = create_data_frame(potion_name, len(potion_ingredients))
        data_frame_list.append(df)
    
    return data_frame_list

data_frame_list = create_list_of_data_frame()

print("STAMPO LA LISTA DI DATA FRAME")
print(data_frame_list)

# Tentativo di inserimento di un valore in un dataframe
# print(data_frame_list[0].columns[0])
# data_frame_list[0].at[0, data_frame_list[0].columns[0]] = "CIAO"
# print(data_frame_list)

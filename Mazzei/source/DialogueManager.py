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

df = pd.DataFrame(index=range(4),columns=['a'])

print(df)
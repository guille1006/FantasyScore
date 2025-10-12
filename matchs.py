import json
import pandas as pd
from collections import defaultdict

from Sofascore import Sofascore
from utils.get_fields import get_fields

#------------------------------------------------------------------------------------------------------------
# Llamamos a la clase Sofascore para poder extraer los datos de Sofascore
sofascore = Sofascore()

# Usamos la funcion get_match_dicts para tener todos los datos de la liga deseada y su correspondiente temporada
matchs = sofascore.get_match_dicts("24/25", "Spain La Liga")

#------------------------------------------------------------------------------------------------------------
# Hay muchos datos irrelevantes por ello vamos a filtrar, usaremos solo los campos especificados abajo
important_fields = [{"tournament":["name"]},
                    {"season":["year"]},
                    "roundInfo",
                    {"homeTeam":["id", "name"]},
                    {"awayTeam":["id", "name"]},
                    {"homeScore": ["period1", "period2", "normaltime"]},
                    {"awayScore": ["period1", "period2", "normaltime"]},
                    "id",
                    {"status":["description"]}]

# Convertimos nuestros datos y contamos para tener claro cuales queremos y cuales no
# Es importante saber que solo deberiamos querer aquellos que tienen un status de "finished"
matchs_cleans = list()
count = defaultdict(int)
for match in matchs:
    new_match = get_fields(match, important_fields)
    matchs_cleans.append(new_match)
    count[new_match["roundInfo"]["round"]] += 1 


#------------------------------------------------------------------------------------------------------------
# Guardado de los datos en un JSON
with open("data/matchs_cleans.json", "w", encoding="utf-8") as f:
    json.dump(matchs_cleans, f, ensure_ascii=False, indent=4)

# Guardado de los datos en un csv
matchs_cleans_df = pd.json_normalize(matchs_cleans)
matchs_cleans_df.to_csv("data/matchs_cleans.csv", index=False, encoding="utf-8")
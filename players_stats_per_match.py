import json
import pandas as pd

from Sofascore import Sofascore
from utils.get_fields import get_fields

# Creo el objeto de Sofascore para poder recolectar los datos
sofascore = Sofascore()

# Abro el archivo con todos los csv y solo uso aquellos que tienen en su descripción Ended
df_matchs = pd.read_csv("data/matchs_cleans.csv")
matchs = df_matchs[df_matchs["status.description"]=="Ended"]["id"]
#------------------------------------------------------------------------------------------------------------
# Los campos que creo que son importantes son:
important_fields = [{"player": ["name", "id"]},  
                "position",
                "substitute",
                "statistics"]

# Genero una lista que será donde guarde todos los datos
players_stats_per_match = []

# Además genero un contador para ver si algun match ha dado error
contador = 0

# Realizo el bucle para todos los match id
for match_id in matchs:
    # Leo los datos
    data = sofascore.scrape_player_match_stats(match_id)
    # Me aseguro que tiene todos los apartados
    ## Al final he comentado esto porque me puede dar error en mitad de la ejecución y perderia todo lo no guardado
    ## if not data["confirmed"]:
        ## contador += 1
        ## print(match_id)
        ## continue

    
    data = data["home"]["players"] + data["away"]["players"]

    for player in data:
        info = get_fields(player, important_fields)
        info["match_id"] = match_id
        if len(info["statistics"]) > 1:
            players_stats_per_match.append(info)


#------------------------------------------------------------------------------------------------------------
# Guardado de los datos en un JSON
with open("data/players_stats_per_match.json", "w", encoding="utf-8") as f:
    json.dump(players_stats_per_match, f, ensure_ascii=False, indent=4)

# Guardado de los datos en un csv
matchs_cleans_df = pd.json_normalize(players_stats_per_match)
matchs_cleans_df.to_csv("data/players_stats_per_match.csv", index=False, encoding="utf-8")
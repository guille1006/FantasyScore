import pandas as pd
import numpy as np
import json
from typing import Union, Sequence
import warnings


from utils.botasaurus_getters import botasaurus_browser_get_json
from utils.load_comps import get_module_comps

API_PREFIX = 'https://api.sofascore.com/api/v1'
comps = get_module_comps("SOFASCORE")

class Sofascore:

    # =======================================================================================
    def __init__(self) -> None:
        pass 

    # =======================================================================================
    def get_valid_seasons(self, league:str) -> dict:
        """
        Devuelve las temporadas validas para la liga especificada con su respectivo ID
        Param
        -----
        league (str): Liga que vamos a buscar, el str debe estar guardado en el comps.yaml
        
        Return
        ------
        dict: Diccionario
            key: Nombre de la temporada
            value: ID de la temporada
        """
        if not isinstance(league, str):
            raise TypeError("'league' must be a string")
        if league not in comps.keys():
            raise ValueError(f"{league} is not valid")
        
        url = f"{API_PREFIX}/unique-tournament/{comps[league]["SOFASCORE"]}/seasons/"
        response = botasaurus_browser_get_json(url)
        seasons = dict([(x['year'], x['id']) for x in response['seasons']])
        return seasons
    
    # =======================================================================================
    def get_match_dicts(self, year: str, league:str) -> Sequence[dict]:
        """ Devuelve los partidos de la API de Sofascore para una liga y año dado

        Params
        ------
        year (str): Año elegido
        league (str): Liga elegida

        Returns
        -------
        Lista 
            Diccionarios con cada partido

        """
        if not isinstance(year, str):
            raise TypeError('`year` must be a string.')
        valid_seasons = self.get_valid_seasons(league)
        if year not in valid_seasons.keys():
            raise ValueError(f"{year} is not valid")

        matches = list()
        i = 0
        while 1:
            response = botasaurus_browser_get_json(
                f'{API_PREFIX}/unique-tournament/{comps[league]["SOFASCORE"]}/' +
                f'season/{valid_seasons[year]}/events/last/{i}'
            )
            if 'events' not in response:
                break
            matches += response['events']
            i += 1

        return matches
    
    # =======================================================================================
    def get_elem_from_json(self, key_to_find: str, value_to_find) -> dict:
        """
        Usado para sacar el JSON con los datos desde el archivo guardado"""

        with open("data/matchs_cleans.json", "r", encoding="utf-8") as f:
            data_json = json.load(f)

        for item in data_json:
            if key_to_find in item and item[key_to_find] == value_to_find:
                return item

        
    # =======================================================================================
    def get_player_ids(self, match_id:int) -> dict:
        """ Get the player IDs for a match

        :param str or int match: Sofascore match URL or match ID

        :returns: All players who played in the match. Names are keys, IDs are values.
        :rtype: dict
        """
        url = f"{API_PREFIX}/event/{match_id}/lineups"
        response = botasaurus_browser_get_json(url)

        if 'error' not in response:
            teams = ['home', 'away']
            player_ids = dict()
            for team in teams:
                data = response[team]['players']
                for item in data:
                    player_data = item['player']
                    player_ids[player_data['name']] = player_data['id']
        else:
            warnings.warn(
                f"Encountered {response['error']['code']}: {response['error']['message']} from"
                f" {url}. Returning empty dict."
            )
            player_ids = dict()

        return player_ids
    
    # =======================================================================================
    def scrape_player_match_stats(self, match_id: int) -> pd.DataFrame:
        """ Scrape player stats for a match

        :param str or int match: Sofascore match URL or match ID

        :rtype: pandas.DataFrame
        """
        match_dict = self.get_elem_from_json(key_to_find="id", value_to_find=match_id)  # used to get home and away team names and IDs
        url = f'{API_PREFIX}/event/{match_id}/lineups'
        response = botasaurus_browser_get_json(url)

        return response
        if "error" not in response:
            home_players = response['home']['players']
            away_players = response['away']['players']
            for p in home_players:
                p["teamId"] = match_dict["homeTeam"]["id"]
                p["teamName"] = match_dict["homeTeam"]["name"]
            for p in away_players:
                p["teamId"] = match_dict["awayTeam"]["id"]
                p["teamName"] = match_dict["awayTeam"]["name"]
                players = home_players + away_players

            temp = pd.DataFrame(players)
            columns = list()
            for c in temp.columns:
                if isinstance(temp.loc[0, c], dict):
                    # Break dicts into series
                    columns.append(temp[c].apply(pd.Series, dtype=object))
                else:
                    # Else they're already series
                    columns.append(temp[c])  # type: ignore
            df = pd.concat(columns, axis=1)
        else:
            warnings.warn(
                f"Encountered {response['error']['code']}: {response['error']['message']} from"
                f" {url}. Returning empty dataframe."
            )
            df = pd.DataFrame()

        return df

    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================
    # =======================================================================================

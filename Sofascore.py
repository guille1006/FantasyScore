import pandas as pd
import numpy as np
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
    # =======================================================================================

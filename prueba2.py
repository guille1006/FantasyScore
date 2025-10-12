from utils.botasaurus_getters import botasaurus_browser_get_json, botasaurus_request_get_json
from utils.load_comps import get_module_comps

API_PREFIX = 'https://api.sofascore.com/api/v1'
comps = get_module_comps("SOFASCORE")
league = "Spain La Liga"


url = f'{API_PREFIX}/unique-tournament/{comps[league]["SOFASCORE"]}/seasons/'
response = botasaurus_browser_get_json(url)
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
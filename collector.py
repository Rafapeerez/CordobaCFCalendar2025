import requests
from dotenv import load_dotenv
import os 

load_dotenv()

api_key = os.getenv('API_KEY')
team = os.getenv('TEAM')
with open("matches.txt", "w") as file:
    file.truncate(0)  

for iterator in range(1, 43):
    url = f'https://apiclient.besoccerapps.com/scripts/api/api.php?key={api_key}&format=json&req=matchs&league=2&tz=Europe/Madrid&round={iterator}'
    response = requests.get(url)

    info = response.json()

    matches = info.get('match', [])

    with open('matches.txt', 'a') as file:
        for match in matches:
            if ( match.get('local') == team or match.get('visitor') == team) :
                team1 = match.get('local')
                team2 = match.get('visitor')
                schedule = match.get('schedule')
                team_match = f"{team1} vs {team2}, Date: {schedule} \n"
        
                file.write(team_match)
    file.close()
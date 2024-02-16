import requests
import pandas as pd
import concurrent.futures
from datetime import datetime, timedelta
import os
import re
from django.core.management.base import BaseCommand
from webpage.models import Game, Player, Championship
from django.conf import settings

api_key = settings.API_KEY
api_host = settings.API_HOST
base_url = settings.BASE_URL

# Create a session object for persistent connections
session = requests.Session()
session.headers.update({
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": api_host
})

def fetch_game_details(season):
    """Fetches game details for a given season."""
    games_url = f'{base_url}games'
    response = session.get(games_url, params={"season": season})
    return response.json()['response']

def get_game_details_date(date):
    """Processes game details for a given season."""
    games = fetch_game_details(season)
    given_season_games_details = []
    for game in games:
        game_details = {
            'game_id': game['id'],
            'game_start': game.get('date',{}).get('start',None),
            # 'game_end': game.get('date',{}).get('end',None),
            # 'game_duration': game.get('date',{}).get('duration',None),
            'status': game.get('status',{}).get('long',None),
            'team_visitors_id' : game.get('teams',{}).get('visitors',{}).get('id',None),
            'team_visitors_name' : game.get('teams',{}).get('visitors',{}).get('name',None),
            'team_home_id' : game.get('teams',{}).get('home',{}).get('id',None),
            'team_home_name' : game.get('teams',{}).get('home',{}).get('name',None),
            'team_visitors_score' : None,
            'team_home_score' : None,
        }

        # Determine winners and losers
        if game.get('scores',{}).get('visitors',{}).get('win') == '1':
            game_details['team_visitors_score'] = 'W'
            game_details['team_home_score'] = 'L'
        else:
            game_details['team_visitors_score'] = 'L'
            game_details['team_home_score'] = 'W'           
        
        given_season_games_details.append(game_details)
    
    return(given_season_games_details)
        
def get_teams_ids():
    """Fetches team IDs."""
    teams_url = f'{base_url}teams'
    response = session.get(teams_url)
    teams = response.json()['response']
    return [team['id'] for team in teams]

def get_player_per_season(season, team_id, games_per_season):
    """Fetches and processes player details per season."""
    player_details_list = []
    for team in team_id:
        player_url = f'{base_url}players'
        response = session.get(player_url, params={"season": season, "team": team})
        players = response.json()['response']
        for player in players:

            # Get initial details
            player_id = player['id']
            player_details = {
                'season': season,
                'player_id': player['id'],
                'first_name': player['firstname'],
                'last_name': player['lastname'],
                'height': player.get('height', {}).get('meters', None),
                'weight': player.get('weight', {}).get('kilograms', None)
            }
            # Fetch match details only if the basic details are present
            if all(player_details.values()): 
                stats_query = {"id": player['id'], "season": season}
                match_response = session.get(f'{base_url}players/statistics', params=stats_query)
                matches = match_response.json()['response']
            
                for match in matches:
                    if match['player']['id'] == player_id:
                        player_details = player_details.copy()
                        player_details.update({
                        "game_id":match['game']['id'],
                        "player_team":match['team']['name'],
                        "player_team_id":match['team']['id'],
                        "player_team_nickname":match['team']['nickname'],
                        "player_team_code":match['team']['code'],
                        "player_points":match['points'],
                        "player_pos":match['pos'],
                        "player_min":match['min'],
                        "player_fgm":match['fgm'],
                        "player_fga":match['fga'],
                        "player_fgp":match['fgp'],
                        "player_ftm":match['ftm'],
                        "player_fta":match['fta'],
                        "player_ftp":match['ftp'],
                        "player_tpm":match['tpm'],
                        "player_tpa":match['tpa'],
                        "player_tpp":match['tpp'],
                        "player_offReb":match['offReb'],
                        "player_defReb":match['defReb'],
                        "player_totReb":match['totReb'],
                        "player_assists":match['assists'],
                        "player_pFouls":match['pFouls'],
                        "player_steals":match['steals'],
                        "player_turnovers":match['turnovers'],
                        "player_blocks":match['blocks'],
                        "player_plusMinus":match['plusMinus'],
                        })

                    for game_id in games_per_season:
                        if match['game']['id'] == game_id['game_id'] and game_id['status'] == 'Finished':
                                # Convert and format game_start and game_end
                                game_start_date = datetime.strptime(game_id['game_start'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                player_details = player_details.copy()
                                player_details.update({
                                "game_start":game_start_date,
                                "game_status":game_id['status'],
                                "home_team_id":game_id['team_home_id'],
                                "home_team_name":game_id['team_home_name'],
                                "visitors_team_id":game_id['team_visitors_id'],
                                "visitors_team_name":game_id['team_visitors_name'],
                                "visitors_team_score":game_id['team_visitors_score'],
                                "home_team_score":game_id['team_home_score'],
                                })
                                player_details_list.append(player_details)

    return player_details_list

last_recorded_game_date = Game.objects.latest('game_start').game_start.date() if Game.objects.exists() else datetime(year=2022, month=1, day=1).date()
current_date = datetime.now().date()

date_range = [last_recorded_game_date + timedelta(days=x) for x in range((current_date - last_recorded_game_date).days + 1)]

team_ids = get_teams_ids()

main_players_info_list = []

for date in date_range:
    if date.year == current_date.year and date.month >= 10:
        season = date.year
    else:
        season = date.year - 1
        

class Command(BaseCommand):
    help = 'Fetches games and player details from the NBA API for each day in the specified date range.'

    def handle(self, *args, **options):
        # Now you can use args.data_file and args.model_name in your script

        games_per_date = get_game_details_date(date)
        date_updates = get_player_per_season(season, team_ids, games_per_date)
        main_players_info_list.extend(date_updates)
        
        # Convert to Pandas DataFrame
        df = pd.DataFrame(main_players_info_list)

        # Replace null values
        cleaned_df = df.dropna()

        # Get the filename of the current script
        filename = os.path.basename(__file__)
        
        # Regex pattern to match the word until the first underscore
        pattern = r"^(.*?)_(.*?)_"

        match = re.match(pattern, filename)
        
        if match:
            sport = match.group(1)
            championship = match.group(2)
            print("Sport:", sport)
            print("Championship:", championship)
        else:
            print("No match found.")

        for index, row in cleaned_df.iterrows():

            championship = Championship.objects.get(name=championship)

            Player.objects.update_or_create(
                player_id=row['player_id'],
                defaults={
                    'player_id': row['player_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'height': row['height'],
                    'weight': row['weight'],
                    'championship': championship.championship_name,
                }
            )

            Game.objects.update_or_create(
                player_id=row['player_id'],
                defaults={
                    'game_id': row['game_id'],
                    'player_points': row['player_points'],
                    'player_team': row['player_team'],
                    'player_team_nickname': row['player_team_nickname'],
                    'player_team_code': row['player_team_code'],
                    'player_pos': row['player_pos'],
                    'player_min': row['player_min'],
                    'player_fgm': row['player_fgm'],
                    'player_fga': row['player_fga'],
                    'player_fgp': row['player_fgp'],
                    'player_ftm': row['player_ftm'],
                    'player_fta': row['player_fta'],
                    'player_ftp': row['player_ftp'],
                    'player_tpm': row['player_tpm'],
                    'player_tpa': row['player_tpa'],
                    'player_tpp': row['player_tpp'],
                    'player_offReb': row['player_offReb'],
                    'player_defReb': row['player_defReb'],
                    'player_totReb': row['player_totReb'],
                    'player_assists': row['player_assists'],
                    'player_pFouls': row['player_pFouls'],
                    'player_steals': row['player_steals'],
                    'player_turnovers': row['player_turnovers'],
                    'player_blocks': row['player_blocks'],
                    'player_plusMinus': row['player_plusMinus'],
                    'game_start': row['game_start'],
                    'game_status': row['game_status'],
                    'home_team_id': row['home_team_id'],
                    'home_team_name': row['home_team_name'],
                    'visitors_team_id': row['visitors_team_id'],
                    'visitors_team_name': row['visitors_team_name'],
                    'visitors_team_score': row['visitors_team_score'],
                    'home_team_score': row['home_team_score'],
                }
            )

        print("Done updatind Game and Player DBs!")
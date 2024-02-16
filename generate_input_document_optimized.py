import requests
import pandas as pd
import concurrent.futures
from datetime import datetime
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Player Games Statistics Agregator")
parser.add_argument('api_key', type=str, help='Key used by Rapid API')
parser.add_argument('api_host', type=str, help='Rapid API hostname')
parser.add_argument('base_url', type=str, help='Base URL')
parser.add_argument('output_file', type=str, help='Output Filepath')

# Parse arguments
args = parser.parse_args()

# Now you can use args.data_file and args.model_name in your script
api_key = args.api_key
api_host = args.api_host
base_url = args.base_url
output_file = args.output_file

# Create a session object for persistent connections
session = requests.Session()
session.headers.update({
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": api_host
})

# Get the season ids between specified range years
def get_seasons_ids():
    """Fetches season IDs within a given range."""
    seasons_url = f'{base_url}seasons'
    response = session.get(seasons_url)
    seasons = response.json()['response']
    # return [season for season in seasons if 2015 <= int(season) <= 2021]
    return [season for season in seasons if 2022 <= int(season) <= 2023]

def fetch_game_details(season):
    """Fetches game details for a given season."""
    games_url = f'{base_url}games'
    response = session.get(games_url, params={"season": season})
    return response.json()['response']

def get_game_details_season(season):
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

# Main execution
seasons_ids = get_seasons_ids()
team_ids = get_teams_ids()

main_players_info_list = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Fetch game details for each season in parallel
    future_to_season = {executor.submit(get_game_details_season, season): season for season in seasons_ids}
    for future in concurrent.futures.as_completed(future_to_season):
        season = future_to_season[future]
        games_per_season = future.result()
        # Fetch player details per season
        season_updates = get_player_per_season(season, team_ids, games_per_season)
        main_players_info_list.extend(season_updates)

# Convert to Pandas DataFrame and export
df = pd.DataFrame(main_players_info_list)
df.dropna(inplace=True)
# df.to_csv('report_players_2015_2021.csv', index=False)
df.to_csv(output_file, index=False)
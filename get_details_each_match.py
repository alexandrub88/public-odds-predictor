import requests
import pandas as pd
from datetime import datetime

api_key = '4b19277cadmsh1dce4652d666edep1b9001jsn9c1bb52fca9a'
base_url = 'https://api-nba-v1.p.rapidapi.com/'
headers = {
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

def get_seasons_ids():
    seasons_url = f'{base_url}seasons'
    response = requests.get(seasons_url, headers = headers)
    seasons= response.json()['response']
    season_list = []
    for season in seasons:
        if 2015<=int(season)<=2018:
            season_list.append(season)
    return(season_list)

def get_game_details_season(season):
    given_season_games_details = []
    games_url = f'{base_url}games'
    querystring = {"season":season}
    response = requests.get(games_url, headers = headers, params = querystring)
    games = response.json()['response']
    for game in games:
        game_details = {
            'game_id': game['id'],
            'game_start': game.get('date',{}).get('start',None),
            'game_end': game.get('date',{}).get('end',None),
            'game_duration': game.get('date',{}).get('duration',None),
            'status': game.get('status',{}).get('long',None),
            'team_visitors_id' : game.get('teams',{}).get('visitors',{}).get('id',None),
            'team_visitors_name' : game.get('teams',{}).get('visitors',{}).get('name',None),
            'team_home_id' : game.get('teams',{}).get('home',{}).get('id',None),
            'team_home_name' : game.get('teams',{}).get('home',{}).get('name',None),
            'team_visitors_score' : None,
            'team_home_score' : None,
        }
        
        if game.get('scores',{}).get('visitors',{}).get('win') == '1':
            game_details['team_visitors_score'] = 'W'
            game_details['team_home_score'] = 'L'
        else:
            game_details['team_visitors_score'] = 'L'
            game_details['team_home_score'] = 'W'           
        
        given_season_games_details.append(game_details)
    
    return(given_season_games_details)
        
def get_teams_ids():
    teams_url = f'{base_url}teams'
    response = requests.get(teams_url, headers = headers)
    teams = response.json()['response']
    team_id = []
    for team in teams:
        team_id.append(team['id'])
    return(team_id)

def get_player_per_season(season, teams_id, games_per_season):
    players_info_per_season = []
    for team in teams_id:
        player_url = f'{base_url}players'
        querystring = {"season":season, "team":team}
        player_response = requests.get(player_url, headers = headers, params = querystring )
        try:
            players = player_response.json()['response']
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
                    match_response = requests.get(f'{base_url}players/statistics', headers=headers, params=stats_query)
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
                            if match['game']['id'] == game_id['game_id']:
                                
                                # Convert and format game_start and game_end
                                game_start_date = datetime.strptime(game_id['game_start'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                game_end_date = datetime.strptime(game_id['game_end'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                
                                player_details = player_details.copy()
                                player_details.update({
                                    "game_start":game_start_date,
                                    "game_end":game_end_date,
                                    "game_duration":game_id['game_duration'],
                                    "game_status":game_id['status'],
                                    "home_team_id":game_id['team_home_id'],
                                    "home_team_name":game_id['team_home_name'],
                                    "visitors_team_id":game_id['team_visitors_id'],
                                    "visitors_team_name":game_id['team_visitors_name'],
                                    "visitors_team_score":game_id['team_visitors_score'],
                                    "home_team_score":game_id['team_home_score'],
                                })
                                players_info_per_season.append(player_details)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        # break
    return(players_info_per_season)

seasons_ids = get_seasons_ids()
team_id = get_teams_ids()

main_players_info_list = []

for season in seasons_ids:
    
    games_per_season = get_game_details_season(season)
    season_updates = get_player_per_season(season, team_id, games_per_season)
    main_players_info_list.extend(season_updates)
    
# Convert to Pandas DataFrame
df = pd.DataFrame(main_players_info_list)

# Replace null values
cleaned_df = df.dropna()

# Write to CSV
cleaned_df.to_csv('report_players.csv', index=False)
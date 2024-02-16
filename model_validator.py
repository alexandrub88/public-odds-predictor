import pandas as pd
from joblib import load
import numpy as np
import requests
from datetime import datetime
import concurrent.futures
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Function to preprocess new data (ensure this matches the training data preprocessing)
def preprocess_data(new_data, encoder, numerical_features, categorical_features):
    # Apply same preprocessing as done for the training data
    new_data[numerical_features] = new_data[numerical_features].astype(float).values.reshape(1, -1)
    new_data_categorical_encoded = encoder.transform(new_data[categorical_features]).values.reshape(1, -1)
    categorical_data_encoded = encoder.transform(categorical_data).toarray()
    # Combine numerical and categorical features
    new_data_processed = np.concatenate([new_data[numerical_features], new_data_categorical_encoded], axis=1)
    return new_data_processed


def get_seasons_ids():
    """Fetches season IDs within a given range."""
    seasons_url = f'{base_url}seasons'
    response = session.get(seasons_url)
    seasons = response.json()['response']
    return [season for season in seasons if 2022 <= int(season) <= 2022]

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
                match = match_response.json()['response']

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


# Create a session object for persistent connections
session = requests.Session()
api_key = '4b19277cadmsh1dce4652d666edep1b9001jsn9c1bb52fca9a'
session.headers.update({
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
})

base_url = 'https://api-nba-v1.p.rapidapi.com/'

first_match_path = './report_players_2022_all_known_games.csv'

if not os.path.exists(first_match_path):
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
    df.to_csv('report_players_2022_first_match.csv', index=False)


# Load the trained model
model = load('./OU_trained_model.joblib')

# Load data
data = pd.read_csv('./report_players_2022_first_match.csv')

data.dropna(inplace=True)

data = data.sort_values(by=['player_id', 'game_id'])
data = data.reset_index(drop=True)

categorical_features = ['player_pos', 'visitors_team_score', 'home_team_score']
# List of columns to drop
drop_columns = ['season', 'first_name', 'last_name', 'game_id', 'player_team', 'player_team_nickname',
                'player_team_id', 'player_team_code', 'player_min', 'game_duration', 'game_status',
                'home_team_name', 'visitors_team_name', 'game_start', 'game_end', 'game_duration', 'player_points']
numerical_features = [col for col in data.columns if col not in drop_columns + categorical_features]
encoder = OneHotEncoder()
encoder.fit(data[categorical_features])

# numerical_features and categorical_features lists should be the same as used during training.
# List of categorical and numerical features
# categorical_features = ['player_pos', 'visitors_team_score', 'home_team_score']
# encoder = OneHotEncoder()
# encoder.fit(data[categorical_features])
# Load new dataset for prediction
# new_data = pd.read_csv('/path/to/your/new_data.csv')

# Loop through each row in the new dataset
for index, row in data.iterrows():

    # Preprocess the row (excluding 'player_points' from the prediction input)
    preprocessed_row = preprocess_data(row, encoder, numerical_features, categorical_features)

    # Make prediction
    predicted_score = model.predict(preprocessed_row)[0]

    # Print results along with actual points for comparison
    player_id = row['player_id']
    game_id = row['game_id']
    actual_points = row['player_points']  # Actual points scored
    print(f"Player ID {player_id}, Game ID {game_id} -> Predicted Score: {predicted_score}, Actual Score: {actual_points}")
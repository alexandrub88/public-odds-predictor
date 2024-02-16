import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os

print('Started script')

# Prediction scripts variables
preprocessor_path_player_points = os.getenv('PREPROCESSOR_POINTS')
model_path_player_points = os.getenv('MODEL_POINTS')
preprocessor_path_player_turnovers = os.getenv('PREPROCESSOR_TURNOVERS')
model_path_player_turnovers = os.getenv('MODEL_TURNOVERS')
preprocessor_path_player_steals = os.getenv('PREPROCESSOR_STEALS')
model_path_player_steals = os.getenv('MODEL_STEALS')
preprocessor_path_player_assists = os.getenv('PREPROCESSOR_ASSISTS')
model_path_player_assists = os.getenv('MODEL_ASSISTS')
preprocessor_path_player_blocks = os.getenv('PREPROCESSOR_BLOCKS')
model_path_player_blocks = os.getenv('MODEL_BLOCKS')
preprocessor_path_player_tpm = os.getenv('PREPROCESSOR_TPM')
model_path_player_tpm = os.getenv('MODEL_TPM')
preprocessor_path_player_rebounds = os.getenv('PREPROCESSOR_REBOUNDS')
model_path_player_rebounds = os.getenv('MODEL_REBOUNDS')
preprocessor_path_player_fga = os.getenv('PREPROCESSOR_FGA')
model_path_player_fga = os.getenv('MODEL_FGA')
preprocessor_path_player_ftm = os.getenv('PREPROCESSOR_FTM')
model_path_player_ftm = os.getenv('MODEL_FTM')
predictions_output_file = os.getenv('PREDICTIONS_OUTPUT_FILE')
historical_data_path = os.getenv('HISTORICAL_DATAPATH')

# Monte Carlo Dropout prediction function
def predict_with_uncertainty(model, X, n_iter=100):
    predictions = [model.predict(X) for _ in range(n_iter)]
    return np.array(predictions).squeeze()

# Function to generate predictions and uncertainties for each player
def generate_player_points_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player points')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_score = []
    under_probabilities_predicted_score = []
    for idx, mean_score in enumerate(mean_predictions):
        over_probabilities_predicted_score.append(np.mean(probabilistic_predictions > mean_score)*100)
        under_probabilities_predicted_score.append(np.mean(probabilistic_predictions <= mean_score)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_score': mean_predictions,
        'over_probabilities_predicted_score': over_probabilities_predicted_score,
        'under_probabilities_predicted_score': under_probabilities_predicted_score
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_assists_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player assists')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_assists = []
    under_probabilities_predicted_assists = []
    for idx, mean_score in enumerate(mean_predictions):
        over_probabilities_predicted_assists.append(np.mean(probabilistic_predictions > mean_score)*100)
        under_probabilities_predicted_assists.append(np.mean(probabilistic_predictions <= mean_score)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_assists': mean_predictions,
        'over_probabilities_predicted_assists': over_probabilities_predicted_assists,
        'under_probabilities_predicted_assists': under_probabilities_predicted_assists
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_blocks_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player blocks')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_blocks = []
    under_probabilities_predicted_blocks = []
    for idx, mean_blocks in enumerate(mean_predictions):
        over_probabilities_predicted_blocks.append(np.mean(probabilistic_predictions > mean_blocks)*100)
        under_probabilities_predicted_blocks.append(np.mean(probabilistic_predictions <= mean_blocks)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_blocks': mean_predictions,
        'over_probabilities_predicted_blocks': over_probabilities_predicted_blocks,
        'under_probabilities_predicted_blocks': under_probabilities_predicted_blocks
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_turnovers_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player turnovers')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_turnovers = []
    under_probabilities_predicted_turnovers = []
    for idx, mean_turnovers in enumerate(mean_predictions):
        over_probabilities_predicted_turnovers.append(np.mean(probabilistic_predictions > mean_turnovers)*100)
        under_probabilities_predicted_turnovers.append(np.mean(probabilistic_predictions <= mean_turnovers)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_turnovers': mean_predictions,
        'over_probabilities_predicted_turnovers': over_probabilities_predicted_turnovers,
        'under_probabilities_predicted_turnovers': under_probabilities_predicted_turnovers
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_fga_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player fga')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_fga = []
    under_probabilities_predicted_fga = []
    for idx, mean_fga in enumerate(mean_predictions):
        over_probabilities_predicted_fga.append(np.mean(probabilistic_predictions > mean_fga)*100)
        under_probabilities_predicted_fga.append(np.mean(probabilistic_predictions <= mean_fga)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_fga': mean_predictions,
        'over_probabilities_predicted_fga': over_probabilities_predicted_fga,
        'under_probabilities_predicted_fga': under_probabilities_predicted_fga
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_tpm_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player tpm')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_tpm = []
    under_probabilities_predicted_tpm = []
    for idx, mean_tpm in enumerate(mean_predictions):
        over_probabilities_predicted_tpm.append(np.mean(probabilistic_predictions > mean_tpm)*100)
        under_probabilities_predicted_tpm.append(np.mean(probabilistic_predictions <= mean_tpm)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_tpm': mean_predictions,
        'over_probabilities_predicted_tpm': over_probabilities_predicted_tpm,
        'under_probabilities_predicted_tpm': under_probabilities_predicted_tpm
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_rebounds_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player rebounds')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_rebounds = []
    under_probabilities_predicted_rebounds = []
    for idx, mean_rebounds in enumerate(mean_predictions):
        over_probabilities_predicted_rebounds.append(np.mean(probabilistic_predictions > mean_rebounds)*100)
        under_probabilities_predicted_rebounds.append(np.mean(probabilistic_predictions <= mean_rebounds)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_rebounds': mean_predictions,
        'over_probabilities_predicted_rebounds': over_probabilities_predicted_rebounds,
        'under_probabilities_predicted_rebounds': under_probabilities_predicted_rebounds
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_steals_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player steals')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_steals = []
    under_probabilities_predicted_steals = []
    for idx, mean_steals in enumerate(mean_predictions):
        over_probabilities_predicted_steals.append(np.mean(probabilistic_predictions > mean_steals)*100)
        under_probabilities_predicted_steals.append(np.mean(probabilistic_predictions <= mean_steals)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_steals': mean_predictions,
        'over_probabilities_predicted_steals': over_probabilities_predicted_steals,
        'under_probabilities_predicted_steals': under_probabilities_predicted_steals
    })

    return player_predictions

# Function to generate predictions and uncertainties for each player
def generate_player_ftm_predictions(historical_data, preprocessor, model, features, n_iter=100):
    print('Started generate player ftm')
    # Aggregate the latest data for each player
    latest_data = historical_data.groupby('player_id').last().reset_index()
    # Ensure the data contains all necessary features
    if not all(feature in latest_data.columns for feature in features):
        raise ValueError("Missing features in the data")
    # Preprocess the data
    latest_data_processed = preprocessor.transform(latest_data[features])
    # Predict scores with uncertainty
    probabilistic_predictions = predict_with_uncertainty(model, latest_data_processed, n_iter)
    # Calculate mean predictions
    mean_predictions = np.mean(probabilistic_predictions, axis=0)

    # Calculate mean, over, and under probabilities
    over_probabilities_predicted_ftm = []
    under_probabilities_predicted_ftm = []
    for idx, mean_ftm in enumerate(mean_predictions):
        over_probabilities_predicted_ftm.append(np.mean(probabilistic_predictions > mean_ftm)*100)
        under_probabilities_predicted_ftm.append(np.mean(probabilistic_predictions <= mean_ftm)*100)

    # Compile results
    player_predictions = pd.DataFrame({
        'player_id': latest_data['player_id'],
        'predicted_ftm': mean_predictions,
        'over_probabilities_predicted_ftm': over_probabilities_predicted_ftm,
        'under_probabilities_predicted_ftm': under_probabilities_predicted_ftm
    })

    return player_predictions

# Load the historical data
historical_data = pd.read_csv(historical_data_path, sep=',')
print('Loaded historical datapath')
# Load the bet score data
# bet_score_data_path = '/content/drive/MyDrive/Colab Notebooks/bet_score.csv'
# bet_score_data = pd.read_csv(bet_score_data_path, sep=';')

categorical_features = ['player_pos', 'visitors_team_score', 'home_team_score']

# Function to convert time strings to total seconds
def convert_to_seconds(time_str):
    if time_str in ['-', '--']:
        return 0
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:  # HH:MM:SS format
        return 3600 * parts[0] + 60 * parts[1] + parts[2]
    elif len(parts) == 2:  # MM:SS format
        return 60 * parts[0] + parts[1]
    else:
        return 0  # Default case, should not happen if all data is correct

# Apply the conversion to seconds
historical_data['player_min_in_seconds'] = historical_data['player_min'].apply(convert_to_seconds)

# Optionally, convert to minutes
historical_data['player_min_in_minutes'] = historical_data['player_min_in_seconds'] / 60

numerical_features_preproc = ['height', 
                              'weight', 'player_fgm', 'player_fga',
                              'player_ftm', 'player_fta', 'player_tpm', 'player_tpa',
                              'player_offReb', 'player_defReb', 'player_totReb',
                              'player_assists', 'player_pFouls', 'player_steals',
                              'player_turnovers', 'player_blocks', 'player_plusMinus',
                              'player_id', 'game_id', 'player_team_id', 'player_fgp',
                              'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id',
                              'player_points']

# Preprocess data
historical_data['game_id'] = pd.to_numeric(historical_data['game_id'], errors='coerce')
for col in numerical_features_preproc:
    historical_data[col] = pd.to_numeric(historical_data[col], errors='coerce')
print(historical_data)

historical_data.dropna(subset=['game_id'] + numerical_features_preproc + categorical_features, inplace=True)
historical_data.sort_values('game_id', inplace=True)
historical_data.reset_index(drop=True, inplace=True)
print(historical_data)

print('Preprocessed historical_data')


# Define the features used in the model
numerical_features_player_points = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_player_points = numerical_features_player_points + categorical_features

# Define the features used in the model
numerical_features_assists = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_points', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']

features_assists = numerical_features_assists + categorical_features

# Define the features used in the model
numerical_features_blocks = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_points', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_blocks = numerical_features_blocks + categorical_features

# Define the features used in the model
numerical_features_turnovers = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_points', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_turnovers = numerical_features_turnovers + categorical_features

# Define the features used in the model
numerical_features_steals = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_points',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_steals = numerical_features_steals + categorical_features

# Define the features used in the model
numerical_features_tpm = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_points', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_tpm = numerical_features_tpm + categorical_features

# Define the features used in the model
numerical_features_rebounds = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_points',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_rebounds = numerical_features_rebounds + categorical_features

# Define the features used in the model
numerical_features_fga = ['height', 'weight', 'player_fgm', 'player_points',
                      'player_ftm', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_fga = numerical_features_fga + categorical_features

numerical_features_ftm = ['height', 'weight', 'player_fgm', 'player_points',
                      'player_fga', 
                      'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
features_ftm = numerical_features_ftm + categorical_features

# Load the preprocessor and the model
preprocessor_player_points = joblib.load(preprocessor_path_player_points)
model_player_points = tf.keras.models.load_model(model_path_player_points)

print('Loaded player points models')

# Load the preprocessor and the model
preprocessor_player_turnovers = joblib.load(preprocessor_path_player_turnovers)
model_player_turnovers = joblib.load(model_path_player_turnovers)

print('Loaded player points turnovers')

# Load the preprocessor and the model
preprocessor_player_steals = joblib.load(preprocessor_path_player_steals)
model_player_steals = joblib.load(model_path_player_steals)

print('Loaded player points steals')

# Load the preprocessor and the model
preprocessor_player_assists = joblib.load(preprocessor_path_player_assists)
model_player_assists = joblib.load(model_path_player_assists)

print('Loaded player points assists')

# Load the preprocessor and the model
preprocessor_player_blocks = joblib.load(preprocessor_path_player_blocks)
model_player_blocks = joblib.load(model_path_player_blocks)

print('Loaded player points blocks')

# Load the preprocessor and the model
preprocessor_player_tpm = joblib.load(preprocessor_path_player_tpm)
model_player_tpm = joblib.load(model_path_player_tpm)

print('Loaded player points tpm')

# Load the preprocessor and the model
preprocessor_player_rebounds = joblib.load(preprocessor_path_player_rebounds)
model_player_rebounds = tf.keras.models.load_model(model_path_player_rebounds)

print('Loaded player points rebounds')

# Load the preprocessor and the model
preprocessor_player_fga = joblib.load(preprocessor_path_player_fga)
model_player_fga = tf.keras.models.load_model(model_path_player_fga)

print('Loaded player points fga')

# Load the preprocessor and the model
preprocessor_player_ftm = joblib.load(preprocessor_path_player_ftm)
model_player_ftm = joblib.load(model_path_player_ftm)

print('Loaded player points ftm')

# Generate predictions for each player
player_points_predictions = generate_player_points_predictions(historical_data, preprocessor_player_points, model_player_points, features_player_points)
player_assists_predictions = generate_player_assists_predictions(historical_data, preprocessor_player_assists, model_player_assists, features_assists)
player_blocks_predictions = generate_player_blocks_predictions(historical_data, preprocessor_player_blocks, model_player_blocks, features_blocks)
player_turnovers_predictions = generate_player_turnovers_predictions(historical_data, preprocessor_player_turnovers, model_player_turnovers, features_turnovers)
player_steals_predictions = generate_player_steals_predictions(historical_data, preprocessor_player_steals, model_player_steals, features_steals)
player_tpm_predictions = generate_player_tpm_predictions(historical_data, preprocessor_player_tpm, model_player_tpm, features_tpm)
player_fga_predictions = generate_player_fga_predictions(historical_data, preprocessor_player_fga, model_player_fga, features_fga)
player_rebounds_predictions = generate_player_rebounds_predictions(historical_data, preprocessor_player_rebounds, model_player_rebounds, features_rebounds)
player_ftm_predictions = generate_player_ftm_predictions(historical_data, preprocessor_player_ftm, model_player_ftm, features_ftm)

# Calculate probabilities for future games' bet scores
# bet_score_probabilities = calculate_bet_score_probabilities(bet_score_data, historical_data, preprocessor, model, features)

# Combine the predictions and bet score probabilities
###### Uncomment when a final design is done ########
# combined_results = pd.merge(player_predictions, bet_score_probabilities, on='player_id')

# Combine all prediction dataframes
final_predictions = player_points_predictions.merge(player_assists_predictions, on='player_id').merge(player_blocks_predictions, on='player_id').merge(player_turnovers_predictions, on='player_id').merge(player_steals_predictions, on='player_id').merge(player_tpm_predictions, on='player_id').merge(player_fga_predictions, on='player_id').merge(player_rebounds_predictions, on='player_id').merge(player_ftm_predictions, on='player_id')

# Display or save the combined results
print(final_predictions)

# Optionally, save to a CSV file
final_predictions.to_csv(predictions_output_file, index=False)
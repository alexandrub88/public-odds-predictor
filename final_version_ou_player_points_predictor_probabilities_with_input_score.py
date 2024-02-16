import pandas as pd
import numpy as np
import tensorflow as tf
import joblib

# Monte Carlo Dropout prediction function
def predict_with_uncertainty(model, X, n_iter=100):
    predictions = [model.predict(X) for _ in range(n_iter)]
    return np.array(predictions).squeeze()

# Function to generate predictions and uncertainties for each player
def generate_player_predictions(historical_data, preprocessor, model, features, n_iter=100):
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

# Function to calculate probabilities for future games' bet scores
def calculate_bet_score_probabilities(bet_score_data, historical_data, preprocessor, model, features, n_iter=100):
    bet_score_results = []
    for _, bet_row in bet_score_data.iterrows():
        player_id = bet_row['player_id']
        bet_score = bet_row['bet_score']

        # Get the latest historical data for the specific player
        player_historical_data = historical_data[historical_data['player_id'] == player_id]
        # Preprocess the player's historical data
        player_data_processed = preprocessor.transform(player_historical_data[features])

        # Predict scores with uncertainty for this player
        probabilistic_predictions_bet_score = predict_with_uncertainty(model, player_data_processed, n_iter)

        # Calculate mean predictions
        mean_predictions_bet_score = np.mean(probabilistic_predictions_bet_score, axis=0)

        # Calculate over and under probabilities for the bet score
        over_probabilities_bet_score = np.mean(probabilistic_predictions_bet_score > bet_score) * 100
        under_probabilities_bet_score = np.mean(probabilistic_predictions_bet_score <= bet_score) * 100

        bet_score_results.append({
            'player_id': player_id,
            'bet_score': bet_score,
            'over_probability_bet_score': over_probabilities_bet_score,
            'under_probability_bet_score': under_probabilities_bet_score
        })

    return pd.DataFrame(bet_score_results)

# Load the historical data
historical_data_path = '/content/drive/MyDrive/Colab Notebooks/1st_half_season_without_last_game.csv'
historical_data = pd.read_csv(historical_data_path, sep=';')

# Load the bet score data
bet_score_data_path = '/content/drive/MyDrive/Colab Notebooks/bet_score.csv'
bet_score_data = pd.read_csv(bet_score_data_path, sep=';')
print(bet_score_data.columns)

# Define the features used in the model
numerical_features = ['height', 'weight', 'player_fgm', 'player_fga',
                      'player_ftm', 'player_fta', 'player_tpm', 'player_tpa',
                      'player_offReb', 'player_defReb', 'player_totReb',
                      'player_assists', 'player_pFouls', 'player_steals',
                      'player_turnovers', 'player_blocks', 'player_plusMinus',
                      'player_id', 'game_id', 'player_team_id', 'player_fgp',
                      'player_ftp', 'player_tpp', 'home_team_id', 'visitors_team_id']
categorical_features = ['player_pos', 'visitors_team_score', 'home_team_score']
features = numerical_features + categorical_features

# Preprocess data
historical_data['game_id'] = pd.to_numeric(historical_data['game_id'], errors='coerce')
for col in numerical_features:
    historical_data[col] = pd.to_numeric(historical_data[col], errors='coerce')
historical_data.dropna(subset=['game_id'] + numerical_features + categorical_features, inplace=True)
historical_data.sort_values('game_id', inplace=True)
historical_data.reset_index(drop=True, inplace=True)

# Load the preprocessor and the model
preprocessor_path = '/content/drive/MyDrive/Colab Notebooks/preprocessor_ou_dropout_probabilistic.joblib'
model_path = '/content/drive/MyDrive/Colab Notebooks/NN_player_points_predictor_best_v3_probabilistic.h5'
preprocessor = joblib.load(preprocessor_path)
model = tf.keras.models.load_model(model_path)

# Generate predictions for each player
player_predictions = generate_player_predictions(historical_data, preprocessor, model, features)

# Calculate probabilities for future games' bet scores
bet_score_probabilities = calculate_bet_score_probabilities(bet_score_data, historical_data, preprocessor, model, features)

# Combine the predictions and bet score probabilities
combined_results = pd.merge(player_predictions, bet_score_probabilities, on='player_id')

# Display or save the combined results
print(combined_results)

# Optionally, save to a CSV file
# output_file_path = '/content/drive/MyDrive/Colab Notebooks/combined_predictions_and_bet_scores.csv'
combined_results.to_csv(output_file_path, index=False)

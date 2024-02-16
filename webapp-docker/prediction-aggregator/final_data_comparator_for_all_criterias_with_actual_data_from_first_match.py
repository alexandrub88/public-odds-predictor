import pandas as pd
import os


combined_predictions_and_bet_scores = os.getenv('COMBINED_PREDICTIONS_AND_BET_SCORES_FILEPATH')
players_report_future_match = os.getenv('PLAYERS_REPORT_FUTURE_MATCH')
combined_predictions_output_path = os.getenv('COMBINED_PREDICTIONS_OUTPUT_PATH')

# Load both CSV files
df1 = pd.read_csv(combined_predictions_and_bet_scores, sep=',' )
df2 = pd.read_csv(players_report_future_match, sep = ',')

# Sort the second dataframe by player_id and then by game_id to ensure we get the first game_id for each player
df2_sorted = df2.sort_values(by=['player_id', 'game_id'])

# Drop duplicates to keep only the first game_id for each player_id
df2_first_game = df2_sorted.drop_duplicates(subset=['player_id'])

# Merge the first dataframe with the df2_first_game on player_id to match the game_id
merged_df = df1.merge(df2_first_game[['player_id', 'game_id', 'player_points', 'player_tpm', 'player_assists', 'player_turnovers', 'player_totReb', 'player_blocks',
                                      'player_fga', 'player_steals', 'player_ftm']], on='player_id', how='left')

# Rename columns for clarity
merged_df.rename(columns={
    'player_points': 'actual_player_points',
    'predicted_score': 'predicted_player_points',
    'over_probabilities_predicted_score': 'over_probabilities_player_points',
    'under_probabilities_predicted_score': 'under_probabilities_player_points',
    'player_assists': 'actual_player_assists',
    'predicted_assists': 'predicted_player_assists',
    'over_probabilities_predicted_assists': 'over_probabilities_player_assists',
    'under_probabilities_predicted_assists': 'under_probabilities_player_assists',
    'player_tpm': 'actual_player_tpm',
    'predicted_tpm': 'predicted_player_tpm',
    'over_probabilities_predicted_tpm': 'over_probabilities_player_tpm',
    'under_probabilities_predicted_tpm': 'under_probabilities_player_tpm',
    'player_turnovers': 'actual_player_turnovers',
    'predicted_turnovers': 'predicted_player_turnovers',
    'over_probabilities_predicted_turnovers': 'over_probabilities_player_turnovers',
    'under_probabilities_predicted_turnovers': 'under_probabilities_player_turnovers',
    'player_blocks': 'actual_player_blocks',
    'predicted_blocks': 'predicted_player_blocks',
    'over_probabilities_predicted_blocks': 'over_probabilities_player_blocks',
    'under_probabilities_predicted_blocks': 'under_probabilities_player_blocks',
    'player_totReb': 'actual_player_rebounds',
    'predicted_rebounds': 'predicted_player_rebounds',
    'over_probabilities_predicted_rebounds': 'over_probabilities_player_rebounds',
    'under_probabilities_predicted_rebounds': 'under_probabilities_player_rebounds',
    'player_fga': 'actual_player_fga',
    'predicted_fga': 'predicted_player_fga',
    'over_probabilities_predicted_fga': 'over_probabilities_player_fga',
    'under_probabilities_predicted_fga': 'under_probabilities_player_fga',
    'player_steals': 'actual_player_steals',
    'predicted_steals': 'predicted_player_steals',
    'over_probabilities_predicted_steals': 'over_probabilities_player_steals',
    'under_probabilities_predicted_steals': 'under_probabilities_player_steals',
    'player_ftm': 'actual_player_ftm',
    'predicted_ftm': 'predicted_player_ftm',
    'over_probabilities_predicted_ftm': 'over_probabilities_player_ftm',
    'under_probabilities_predicted_ftm': 'under_probabilities_player_ftm',
}, inplace=True)

# Select and order the columns as specified
final_df = merged_df[[
    'player_id', 'game_id', 'actual_player_points', 'predicted_player_points',
    'over_probabilities_player_points', 'under_probabilities_player_points',
    'actual_player_assists', 'predicted_player_assists',
    'over_probabilities_player_assists', 'under_probabilities_player_assists',
    'actual_player_tpm', 'predicted_player_tpm', 'over_probabilities_player_tpm',
    'under_probabilities_player_tpm', 'actual_player_turnovers',
    'predicted_player_turnovers', 'over_probabilities_player_turnovers',
    'under_probabilities_player_turnovers',
    'actual_player_blocks',
    'predicted_player_blocks', 'over_probabilities_player_blocks',
    'under_probabilities_player_blocks',
    'actual_player_rebounds',
    'predicted_player_rebounds', 'over_probabilities_player_rebounds',
    'under_probabilities_player_rebounds', 'actual_player_fga',
    'predicted_player_fga', 'over_probabilities_player_fga',
    'under_probabilities_player_fga', 'actual_player_steals',
    'predicted_player_steals', 'over_probabilities_player_steals',
    'under_probabilities_player_steals', 'predicted_player_ftm',
    'over_probabilities_player_ftm', 'under_probabilities_player_ftm',
]]
print(final_df)
# Save the final dataframe to a new CSV file
final_df.to_csv(combined_predictions_output_path, index=False)  # Replace with your desired output path

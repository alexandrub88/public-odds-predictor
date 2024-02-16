import pandas as pd

# Function to read the CSV and split the data accordingly
def split_season_data(input_csv_path):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)
    
    # Convert the 'game_start' column to datetime to ensure chronological order
    df['game_start'] = pd.to_datetime(df['game_start'])

    # Sort the DataFrame by 'game_start' to ensure chronological order
    df_sorted = df.sort_values('game_start')

    # Find the midpoint game_id for the season
    midpoint = df_sorted['game_id'].median()

    # Split the dataframe into two halves
    first_half_season_df = df_sorted[df_sorted['game_id'] <= midpoint]
    second_half_season_df = df_sorted[df_sorted['game_id'] > midpoint]

    # For the second half, we only want the first game for each player
    first_game_second_half_df = second_half_season_df.groupby('player_id').nth(0).reset_index()

    # Save the resulting DataFrames to new CSV files
    first_half_season_df.to_csv('./1st_half_season.csv', index=False)
    first_game_second_half_df.to_csv('./2nd_half_season_first_game.csv', index=False)

# Replace 'your_input_file.csv' with the path to your actual input CSV file
split_season_data('./report_players_2022_all_known_games.csv')

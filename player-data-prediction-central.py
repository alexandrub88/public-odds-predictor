import os
import subprocess
from dotenv import load_dotenv

# Specify the path to your .env file
dotenv_path = './prediction-data.env'

# Load the specified .env file
load_dotenv(dotenv_path=dotenv_path)

# Retrieve variables from .env
api_key = os.getenv('API_KEY')
api_host = os.getenv('API_HOST')
base_url = os.getenv('BASE_URL')
output_file = os.getenv('OUTPUT_FILE')
combined_predictions_and_bet_scores = os.getenv('COMBINED_PREDICTIONS_AND_BET_SCORES_FILEPATH')
players_report_future_match = os.getenv('PLAYERS_REPORT_FUTURE_MATCH')
combined_predictions_output_path = os.getenv('COMBINED_PREDICTIONS_OUTPUT_PATH')

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

def run_script(script_name, args):
    try:
        # Execute the script and capture output and errors
        completed_process = subprocess.run(
            ['python', script_name, *args],
            check=True,
            text=True,  # Ensure text mode for output and errors
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE   # Capture standard error
        )
        # Print the output
        print("Script Output:\n", completed_process.stdout)
    except subprocess.CalledProcessError as e:
        # Print the error message if script execution fails
        print("Script Error Output:\n", e.stderr)
        

# Run each script with the required arguments
# run_script('generate_input_document_optimized.py', [api_key, api_host, base_url, output_file])
run_script('ou_player_predictor_probabilities_with_input_all_parameters.py', [preprocessor_path_player_points, model_path_player_points, preprocessor_path_player_turnovers, model_path_player_turnovers, preprocessor_path_player_steals, model_path_player_steals, preprocessor_path_player_assists, model_path_player_assists, preprocessor_path_player_blocks, model_path_player_blocks, preprocessor_path_player_tpm, model_path_player_tpm, preprocessor_path_player_rebounds, model_path_player_rebounds, preprocessor_path_player_fga, model_path_player_fga, preprocessor_path_player_ftm, model_path_player_ftm, historical_data_path, predictions_output_file])
run_script('final_data_comparator_for_all_criterias_with_actual_data_from_first_match.py', [combined_predictions_and_bet_scores, players_report_future_match, combined_predictions_output_path])

print("All scripts executed successfully.")
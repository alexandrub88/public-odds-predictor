import os
import subprocess
from dotenv import load_dotenv

# Specify the path to your .env file
dotenv_path = '/content/drive/MyDrive/Colab Notebooks/training-data.env'

# Load the specified .env file
load_dotenv(dotenv_path=dotenv_path)

# Retrieve variables from .env
training_dataset = os.getenv('TRAINING_DATASET')

model_checkpoint_fga = os.getenv('MODEL_CHECKPOINT_FGA')
model_fga_path = os.getenv('MODEL_FGA_PATH')
preprocessor_fga_path = os.getenv('PREPROCESSOR_FGA_PATH')

model_assists_path = os.getenv('MODEL_ASSISTS_PATH')
preprocessor_assists_path = os.getenv('PREPROCESSOR_ASSISTS_PATH')

model_blocks_path = os.getenv('MODEL_BLOCKS_PATH')
preprocessor_blocks_path = os.getenv('PREPROCESSOR_BLOCKS_PATH')

model_ftm_path = os.getenv('MODEL_FTM_PATH')
preprocessor_ftm_path = os.getenv('PREPROCESSOR_FTM_PATH')

model_checkpoint_points = os.getenv('MODEL_CHECKPOINT_POINTS')
model_points_path = os.getenv('MODEL_POINTS_PATH')
preprocessor_points_path = os.getenv('PREPROCESSOR_POINTS_PATH')

model_checkpoint_rebounds = os.getenv('MODEL_CHECKPOINT_REBOUNDS')
model_rebounds_path = os.getenv('MODEL_REBOUNDS_PATH')
preprocessor_rebounds_path = os.getenv('PREPROCESSOR_REBOUNDS_PATH')

model_steals_path = os.getenv('MODEL_STEALS_PATH')
preprocessor_steals_path = os.getenv('PREPROCESSOR_STEALS_PATH')

model_tpm_path = os.getenv('MODEL_TPM_PATH')
preprocessor_tpm_path = os.getenv('PREPROCESSOR_TPM_PATH')

model_turnovers_path = os.getenv('MODEL_TURNOVERS_PATH')
preprocessor_turnovers_path = os.getenv('PREPROCESSOR_TURNOVERS_PATH')

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
run_script('final_version_ou_player_total_fga_training_code_probabilities.py', [training_dataset, model_checkpoint_fga, model_fga_path, preprocessor_fga_path])
run_script('final_version_ou_player_total_assists_training_code_probabilities.py', [training_dataset, model_assists_path, preprocessor_assists_path])
run_script('final_version_ou_player_total_blocks_training_code_probabilities.py', [training_dataset, model_blocks_path, preprocessor_blocks_path])
run_script('final_version_ou_player_total_ftm_training_code_probabilities.py', [training_dataset, model_ftm_path, preprocessor_ftm_path])
run_script('final_version_ou_player_total_points_training_code_probabilities.py', [training_dataset, model_checkpoint_points, model_points_path, preprocessor_points_path])
run_script('final_version_ou_player_total_rebounds_training_code_probabilities.py', [training_dataset, model_checkpoint_rebounds, model_rebounds_path, preprocessor_rebounds_path])
run_script('final_version_ou_player_total_steals_training_code_probabilities.py', [training_dataset, model_steals_path, preprocessor_steals_path])
run_script('final_version_ou_player_total_tpm_training_code_probabilities.py', [training_dataset, model_tpm_path, preprocessor_tpm_path])
run_script('final_version_ou_player_total_turnovers_training_code_probabilities.py', [training_dataset, model_turnovers_path, preprocessor_turnovers_path])

print("All scripts executed successfully.")
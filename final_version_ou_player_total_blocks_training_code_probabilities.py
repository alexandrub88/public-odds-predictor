import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description="FGA Training Script")
parser.add_argument('data_file', type=str, help='Path to the dataset training file')
parser.add_argument('model_path', type=str, help='Path of the model file')
parser.add_argument('preprocessor_path', type=str, help='Path of the preprocessor file')

# Parse arguments
args = parser.parse_args()

# Now you can use args.data_file and args.model_name in your script
data_path = args.data_file
model_path = args.model_path
preprocessor_path = args.preprocessor_path

# Load data
# data_path = '/content/drive/MyDrive/Colab Notebooks/report_players_2015_2021.csv'
data = pd.read_csv(data_path)

# Data preprocessing
data.dropna(inplace=True)
data.sort_values('game_id', inplace=True)
data.reset_index(drop=True, inplace=True)

# # Function to convert time strings to total seconds
# def convert_to_seconds(time_str):
#     parts = list(map(int, time_str.split(':')))
#     if len(parts) == 3:  # HH:MM:SS format
#         return 3600 * parts[0] + 60 * parts[1] + parts[2]
#     elif len(parts) == 2:  # MM:SS format
#         return 60 * parts[0] + parts[1]
#     else:
#         return 0  # Default case, should not happen if all data is correct

# # Apply the conversion to seconds
# data['player_min_in_seconds'] = data['player_min'].apply(convert_to_seconds)

# # Optionally, convert to minutes
# data['player_min_in_minutes'] = data['player_min_in_seconds'] / 60

# Dropping certain columns
drop_columns = ['season', 'first_name', 'last_name', 'game_id', 'player_team', 'player_team_nickname', 'player_team_code', 'player_min', 'game_status', 'home_team_name', 'visitors_team_name', 'game_start']
data.drop(columns = drop_columns, inplace=True)

# Define the target variable and features
target = 'player_blocks'
features = [col for col in data.columns if col != target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

# Define preprocessing for numerical and categorical features
numerical_features = [col for col in features if data[col].dtype in ['int64', 'float64']]
categorical_features = [col for col in features if data[col].dtype == 'object']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Preprocess the data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_processed, y_train)

# Predict and evaluate
rf_predictions = rf_model.predict(X_test_processed)
rf_mse = mean_squared_error(y_test, rf_predictions)
print(f"Random Forest Test MSE: {rf_mse}")

# Save the model and the preprocessor
joblib.dump(preprocessor, preprocessor_path)
joblib.dump(rf_model, model_path)

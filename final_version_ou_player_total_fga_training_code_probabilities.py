import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import joblib
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description="FGA Training Script")
parser.add_argument('data_file', type=str, help='Path to the dataset training file')
parser.add_argument('model_checkpoint_path', type=str, help='Path to save the intermediary checkpoint')
parser.add_argument('model_path', type=str, help='Path of the model file')
parser.add_argument('preprocessor_path', type=str, help='Path of the preprocessor file')

# Parse arguments
args = parser.parse_args()

# Now you can use args.data_file and args.model_name in your script
data_path = args.data_file
model_checkpoint_path = args.model_checkpoint_path
model_path = args.model_path
preprocessor_path = args.preprocessor_path


# Load data
# data_path = '/content/drive/MyDrive/Colab Notebooks/report_players_2015_2021.csv'
data = pd.read_csv(data_path)

# Data preprocessing (similar to your existing code)
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

# Define train and test seasons
train_season = 2020
test_season = 2021

# Splitting the data into train and test datasets
train_data = data[data['season'] <= train_season]
test_data = data[data['season'] == test_season]

# Dropping certain columns
drop_columns = ['season', 'first_name', 'last_name', 'game_id', 'player_team', 'player_team_nickname', 'player_team_code', 'player_min', 'game_status', 'home_team_name', 'visitors_team_name', 'game_start']
data.drop(columns = drop_columns, inplace=True)

# Define the features and target variable
target = 'player_fga'  # Adjust as needed
features = [col for col in data.columns if col != target]

# Split the data into training and test sets
X_train, y_train = train_data[features], train_data[target]
X_test, y_test = test_data[features], test_data[target]

# Define numerical and categorical features
numerical_features = [col for col in features if data[col].dtype in ['int64', 'float64']]
categorical_features = [col for col in features if data[col].dtype == 'object']

# Define the preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Define the neural network model with dropout for Monte Carlo
def create_model(input_shape, layers=[64], dropout_rate=0.3, activation='relu', optimizer='adam'):
    model = Sequential()
    model.add(Dense(layers[0], input_shape=(input_shape,), activation=activation))
    for layer_size in layers[1:]:
        model.add(Dense(layer_size, activation=activation))
        model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mean_squared_error'])
    return model

# Split the data into training and test sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
X_train, y_train = train_data[features], train_data[target]
X_test, y_test = test_data[features], test_data[target]

# Preprocess the data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Create the model
model = create_model(X_train_processed.shape[1], layers=[64, 64], dropout_rate=0.3, activation='relu', optimizer='adam')

# Early stopping and model checkpoint callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
model_checkpoint_fga = ModelCheckpoint(model_checkpoint_path, save_best_only=True, monitor='val_loss', mode='min')

# Train the model
model.fit(X_train_processed, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping, model_checkpoint_fga])

# Load the best model from checkpoint
model.load_weights(model_checkpoint_path)

# Evaluate the model on the test set
test_loss, test_mse = model.evaluate(X_test_processed, y_test)
print(f"Test MSE: {test_mse}")

# Save the model and the preprocessor
joblib.dump(preprocessor, preprocessor_path)
model.save(model_path)

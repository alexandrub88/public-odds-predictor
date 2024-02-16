import pandas as pd

# Define a function to classify each prediction
def classify_prediction(actual, predicted, over_prob, under_prob):
    if over_prob >= 55 and actual > predicted:
        return 'True'
    elif under_prob >= 55 and actual < predicted:
        return 'True'
    elif 50 <= over_prob <= 55 or 45 <= under_prob <= 50:
        return 'Neutral'
    else:
        return 'False'

# Read the CSV file
df = pd.read_csv('final_aggregated_data.csv', sep=',')
df.dropna(inplace=True)


# List of prediction types
prediction_types = ['player_points', 'player_assists', 'player_tpm', 'player_turnovers', 'player_blocks', 'player_rebounds', 'player_fga', 'player_steals']#, 'player_ftm']

# Process each prediction type
for pred_type in prediction_types:
    actual_col = f'actual_{pred_type}'
    predicted_col = f'predicted_{pred_type}'
    over_prob_col = f'over_probabilities_{pred_type}'
    under_prob_col = f'under_probabilities_{pred_type}'
    # Apply the classification function
    df[f'{pred_type}_prediction_accuracy'] = df.apply(
        lambda row: classify_prediction(int(row[actual_col]), int(row[predicted_col]), int(row[over_prob_col]), int(row[under_prob_col])),
        axis=1
    )
    # Calculate the counts and accuracy
    counts = df[f'{pred_type}_prediction_accuracy'].value_counts()
    true_count = counts.get('True', 0)
    false_count = counts.get('False', 0)
    neutral_count = counts.get('Neutral', 0)

    # Accuracy calculation (excluding neutrals)
    total_non_neutral = true_count + false_count
    total_with_neutral = true_count + false_count + neutral_count

    accuracy = (true_count / total_non_neutral) * 100 if total_non_neutral > 0 else 0
    accurary_neutral = ((true_count + neutral_count) / total_with_neutral) * 100 if total_with_neutral > 0 else 0
    print(f'{pred_type} - True: {true_count}, False: {false_count}, Neutral: {neutral_count}, Accuracy: {accuracy:.2f}%, Accuracy with neutral: {accurary_neutral:.2f}%')


# Optionally, save the modified dataframe to a new CSV file
df.to_csv('generate_accuracy_final_with_time.csv', index=False)

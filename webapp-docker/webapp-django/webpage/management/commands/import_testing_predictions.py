import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from webpage.models import Predictions, Player  # Adjust 'myapp.models' to the correct path

class Command(BaseCommand):
    help = 'Import predictions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    @transaction.atomic  # Use a transaction to ensure data integrity
    def handle(self, *args, **options):
        df = pd.read_csv(options['csv_file'])
        df.dropna(inplace=True)
        df.sort_values('game_id', inplace=True)
        df.reset_index(drop=True, inplace=True)

        for _, row in df.iterrows():
            try:
                player = Player.objects.get(player_id=int(row['player_id']))
            except Player.DoesNotExist:
                print(f"Skipping unknown player with ID {int(row['player_id'])}")
                continue

            Predictions.objects.get_or_create(
                player=player,
                game_id=int(row['game_id']),          
                predicted_player_points = round(float(row['predicted_player_points']), 2),
                over_probabilities_player_points = round(float(row['over_probabilities_player_points']), 2),
                under_probabilities_player_points = round(float(row['under_probabilities_player_points']), 2),
                predicted_player_fga = round(float(row['predicted_player_fga']), 2),
                over_probabilities_player_fga = round(float(row['over_probabilities_player_fga']), 2),
                under_probabilities_player_fga = round(float(row['under_probabilities_player_fga']), 2),
                predicted_player_ftm = round(float(row['predicted_player_ftm']), 2),
                over_probabilities_player_ftm = round(float(row['over_probabilities_player_ftm']), 2),
                under_probabilities_player_ftm = round(float(row['under_probabilities_player_ftm']), 2),
                predicted_player_tpm = round(float(row['predicted_player_tpm']), 2),
                over_probabilities_player_tpm = round(float(row['over_probabilities_player_tpm']), 2),
                under_probabilities_player_tpm = round(float(row['under_probabilities_player_tpm']), 2),
                predicted_player_totReb = round(float(row['predicted_player_rebounds']), 2),
                over_probabilities_player_rebounds = round(float(row['over_probabilities_player_rebounds']), 2),
                under_probabilities_player_rebounds = round(float(row['under_probabilities_player_rebounds']), 2),
                predicted_player_assists = round(float(row['predicted_player_assists']), 2),
                over_probabilities_player_assists = round(float(row['over_probabilities_player_assists']), 2),
                under_probabilities_player_assists = round(float(row['under_probabilities_player_assists']), 2),
                predicted_player_steals = round(float(row['predicted_player_steals']), 2),
                over_probabilities_player_steals = round(float(row['over_probabilities_player_steals']), 2),
                under_probabilities_player_steals = round(float(row['under_probabilities_player_steals']), 2),
                predicted_player_turnovers = round(float(row['predicted_player_turnovers']), 2),
                over_probabilities_player_turnovers = round(float(row['over_probabilities_player_turnovers']), 2),
                under_probabilities_player_turnovers = round(float(row['under_probabilities_player_turnovers']), 2),
                predicted_player_blocks = round(float(row['predicted_player_blocks']), 2),
                over_probabilities_player_blocks = round(float(row['over_probabilities_player_blocks']), 2),
                under_probabilities_player_blocks = round(float(row['under_probabilities_player_blocks']), 2),
            )
    
        self.stdout.write(self.style.SUCCESS(f'Successfully imported predictions from {options["csv_file"]}'))

import csv
from django.core.management.base import BaseCommand, CommandError
from webpage.models import Player, Game, Championship, Sport
from django.utils.dateparse import parse_datetime
import pandas as pd

class Command(BaseCommand):
    help = 'Imports player and game data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **options):

        df = pd.read_csv(options['csv_file'])
        # Data preprocessing
        df.dropna(inplace=True)
        df.sort_values('game_id', inplace=True)
        df.reset_index(drop=True, inplace=True)
        # Ensure the Sport exists and is associated with the Championship
        sport, _ = Sport.objects.get_or_create(name='Basketball')
        championship, _ = Championship.objects.get_or_create(
            name='NBA',
            defaults={'sport': sport}  # Associate the Championship with the Sport
        )
        for _, row in df.iterrows():
            # Create or update the Player
            player, _ = Player.objects.update_or_create(
                player_id=row['player_id'],
                defaults={
                    'player_id': row['player_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'height': row['height'],
                    'weight': row['weight'],
                    'championship': championship
                }
            )

            # Parse game_start datetime if necessary
            # Ensure your CSV's game_start column is in a compatible format or adjust parsing as needed
            
            # Parse game_start datetime if necessary
            game_start = parse_datetime(row['game_start']) if isinstance(row['game_start'], str) else row['game_start']
            
            # Avoiding cases where player didn't played at all
            try:
                parts = list(map(int, row['player_min'].split(':')))
                if len(parts) == 3:  # HH:MM:SS format
                    player_min_in_seconds = 3600 * parts[0] + 60 * parts[1] + parts[2]
                elif len(parts) == 2:  # MM:SS format
                    player_min_in_seconds = 60 * parts[0] + parts[1]
                else:
                    player_min_in_seconds = 0

                row['player_min'] = player_min_in_seconds / 60
            except:
                row['player_min'] = 0
                
            # For the situation above, we need to treat also this one below
            try:
                player_plusMinus = int(row['player_plusMinus'])
            except:
                row['player_plusMinus'] = 0

            # Create or update the Game
            Game.objects.update_or_create(
                game_id=row['game_id'],
                player=player,
                defaults={
                    'game_id': row['game_id'],
                    'player_points': row['player_points'],
                    'player_team': row['player_team'],
                    'player_team_nickname': row['player_team_nickname'],
                    'player_team_code': row['player_team_code'],
                    'player_pos': row['player_pos'],
                    'player_min': row['player_min'],
                    'player_fgm': row['player_fgm'],
                    'player_fga': row['player_fga'],
                    'player_fgp': row['player_fgp'],
                    'player_ftm': row['player_ftm'],
                    'player_fta': row['player_fta'],
                    'player_ftp': row['player_ftp'],
                    'player_tpm': row['player_tpm'],
                    'player_tpa': row['player_tpa'],
                    'player_tpp': row['player_tpp'],
                    'player_offReb': row['player_offReb'],
                    'player_defReb': row['player_defReb'],
                    'player_totReb': row['player_totReb'],
                    'player_assists': row['player_assists'],
                    'player_pFouls': row['player_pFouls'],
                    'player_steals': row['player_steals'],
                    'player_turnovers': row['player_turnovers'],
                    'player_blocks': row['player_blocks'],
                    'player_plusMinus': row['player_plusMinus'],
                    'game_start': row['game_start'],
                    'game_status': row['game_status'],
                    'home_team_id': row['home_team_id'],
                    'home_team_name': row['home_team_name'],
                    'visitors_team_id': row['visitors_team_id'],
                    'visitors_team_name': row['visitors_team_name'],
                    'visitors_team_score': row['visitors_team_score'],
                    'home_team_score': row['home_team_score'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % options['csv_file']))
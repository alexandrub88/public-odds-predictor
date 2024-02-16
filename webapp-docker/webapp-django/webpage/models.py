from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
            return self.name
class Championship(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):
            return self.name

class Player(models.Model):
    player_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)  # Assuming height in centimeters
    weight = models.IntegerField(null=True, blank=True)  # Assuming weight in kilograms
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    
    def __str__(self):
            return self.player_id    
    
class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=255)
    player_points = models.IntegerField()
    player_team = models.CharField(max_length=255)
    player_team_nickname = models.CharField(max_length=255)
    player_team_code = models.CharField(max_length=10)
    player_pos = models.CharField(max_length=5)
    player_min = models.IntegerField()
    player_fgm = models.IntegerField()
    player_fga = models.IntegerField()
    player_fgp = models.DecimalField(max_digits=5, decimal_places=2)
    player_ftm = models.IntegerField()
    player_fta = models.IntegerField()
    player_ftp = models.DecimalField(max_digits=5, decimal_places=2)
    player_tpm = models.IntegerField()
    player_tpa = models.IntegerField()
    player_tpp = models.DecimalField(max_digits=5, decimal_places=2)
    player_offReb = models.IntegerField()
    player_defReb = models.IntegerField()
    player_totReb = models.IntegerField()
    player_assists = models.IntegerField()
    player_pFouls = models.IntegerField()
    player_steals = models.IntegerField()
    player_turnovers = models.IntegerField()
    player_blocks = models.IntegerField()
    player_plusMinus = models.IntegerField()
    game_start = models.DateTimeField()
    game_status = models.CharField(max_length=20)
    home_team_id = models.CharField(max_length=10)
    home_team_name = models.CharField(max_length=255)
    visitors_team_id = models.CharField(max_length=10)
    visitors_team_name = models.CharField(max_length=255)
    visitors_team_score = models.CharField(max_length=2)
    home_team_score = models.CharField(max_length=2)

    def __str__(self):
            return self.game_id

class Odds(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=10)
    player_odds = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Odds"

    def __str__(self):
            return self.player
    
class Predictions(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=10)
    predicted_player_points = models.CharField(max_length=10, default=0)
    over_probabilities_player_points = models.CharField(max_length=10, default=0)
    under_probabilities_player_points = models.CharField(max_length=10, default=0)
    predicted_player_fga = models.CharField(max_length=10, default=0)
    over_probabilities_player_fga = models.CharField(max_length=10, default=0)
    under_probabilities_player_fga = models.CharField(max_length=10, default=0)
    predicted_player_ftm = models.CharField(max_length=10, default=0)
    over_probabilities_player_ftm = models.CharField(max_length=10, default=0)
    under_probabilities_player_ftm = models.CharField(max_length=10, default=0)
    predicted_player_tpm = models.CharField(max_length=10, default=0)
    over_probabilities_player_tpm = models.CharField(max_length=10, default=0)
    under_probabilities_player_tpm = models.CharField(max_length=10, default=0)
    predicted_player_totReb = models.CharField(max_length=10, default=0)
    over_probabilities_player_rebounds = models.CharField(max_length=10, default=0)
    under_probabilities_player_rebounds = models.CharField(max_length=10, default=0)
    predicted_player_assists = models.CharField(max_length=10, default=0)
    over_probabilities_player_assists = models.CharField(max_length=10, default=0)
    under_probabilities_player_assists = models.CharField(max_length=10, default=0)
    predicted_player_steals = models.CharField(max_length=10, default=0)
    over_probabilities_player_steals = models.CharField(max_length=10, default=0)
    under_probabilities_player_steals = models.CharField(max_length=10, default=0)
    predicted_player_turnovers = models.CharField(max_length=10, default=0)
    over_probabilities_player_turnovers = models.CharField(max_length=10, default=0)
    under_probabilities_player_turnovers = models.CharField(max_length=10, default=0)
    predicted_player_blocks = models.CharField(max_length=10, default=0)
    over_probabilities_player_blocks = models.CharField(max_length=10, default=0)
    under_probabilities_player_blocks = models.CharField(max_length=10, default=0)
     
    class Meta:
        verbose_name_plural = "Predictions"
        
    def get_player_id(self):
        return self.player.player_id  # Assuming `player_id` is a field in your Player model

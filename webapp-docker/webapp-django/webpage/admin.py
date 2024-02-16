from django.contrib import admin
from .models import Player, Game, Championship, Sport, Odds, Predictions
from django.utils.translation import gettext_lazy as _

# Custom filter for Player's First Name
class PlayerFirstNameListFilter(admin.SimpleListFilter):
    title = _('Player First Name')
    parameter_name = 'player_first_name'

    def lookups(self, request, model_admin):
        # This is where you retrieve all the unique first names and return them as a list of tuples.
        first_names = Player.objects.order_by('first_name').values_list('first_name', flat=True).distinct()
        return [(first_name, first_name) for first_name in first_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__first_name=self.value())
        return queryset

# Custom filter for Player's Last Name
class PlayerLastNameListFilter(admin.SimpleListFilter):
    title = _('Player Last Name')
    parameter_name = 'player_last_name'

    def lookups(self, request, model_admin):
        # This is where you retrieve all the unique last names and return them as a list of tuples.
        last_names = Player.objects.order_by('last_name').values_list('last_name', flat=True).distinct()
        return [(last_name, last_name) for last_name in last_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player__last_name=self.value())
        return queryset

# Corrected admin classes
class SportAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport']
    list_filter = ['name', 'sport']

    def get_sport(self, obj):
            return obj.sport.name
    get_sport.admin_order_field = 'sport'
    get_sport.short_description = 'sport'

class PlayerAdmin(admin.ModelAdmin):
    
    def get_championship(self, obj):
        return obj.championship.name
    get_championship.admin_order_field = 'championship'
    get_championship.short_description = 'Championship'
        
    list_display = ['player_id', 'first_name', 'last_name', 'championship']
    list_filter = ['championship']

class GameAdmin(admin.ModelAdmin):

    def get_player_id(self, obj):
        return obj.player.player_id

    def player_first_name(self, obj):
        return obj.player.first_name
    player_first_name.short_description = 'Player First Name'

    def player_last_name(self, obj):
        return obj.player.last_name
    player_last_name.short_description = 'Player Last Name'

    get_player_id.admin_order_field = 'player'  # Allows column order sorting
    get_player_id.short_description = 'Player ID'  # Sets column header

    list_display = ['game_id', 'get_player_id', 'game_start', 'player_first_name', 'player_last_name']
    list_filter = ['game_id', 'player', 'game_start', PlayerFirstNameListFilter, PlayerLastNameListFilter]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('player').order_by('player__first_name', 'player__last_name')
        return queryset

class OddsAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'player_odds']
    list_filter = ['game_id']

    def get_player_id(self, obj):
        return obj.player.player_id

    get_player_id.admin_order_field = 'player'  # Allows column order sorting
    get_player_id.short_description = 'Player ID'  # Sets column header

class PredictionsAdmin(admin.ModelAdmin):
    
    def get_player_id(self, obj):
        return obj.player.player_id
    
    get_player_id.admin_order_field = 'player_id'  # Allows column order sorting
    get_player_id.short_description = 'Player ID'

    list_display = ['game_id', 'player_id', 'predicted_player_points','over_probabilities_player_points','under_probabilities_player_points',
                    'predicted_player_fga','over_probabilities_player_fga','under_probabilities_player_fga','predicted_player_ftm',
                    'over_probabilities_player_ftm','under_probabilities_player_ftm','predicted_player_tpm',
                    'over_probabilities_player_tpm','under_probabilities_player_tpm','predicted_player_totReb','over_probabilities_player_rebounds',
                    'under_probabilities_player_rebounds','predicted_player_assists','over_probabilities_player_assists',
                    'under_probabilities_player_assists','predicted_player_steals','over_probabilities_player_steals',
                    'under_probabilities_player_steals','predicted_player_turnovers','over_probabilities_player_turnovers',
                    'under_probabilities_player_turnovers','predicted_player_blocks','over_probabilities_player_blocks','under_probabilities_player_blocks']
    list_filter = ['game_id', 'player_id']

# Registering models with their corresponding admin class
admin.site.register(Sport, SportAdmin)
admin.site.register(Championship, ChampionshipAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Odds, OddsAdmin)
admin.site.register(Predictions, PredictionsAdmin)
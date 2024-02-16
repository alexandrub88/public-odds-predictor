from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Sport, Championship, Player, Predictions, Game
from django.core.serializers.json import DjangoJSONEncoder
import json


def get_championships(request, sport_id):
    championships = Championship.objects.filter(sport_id=sport_id).values('id', 'name')
    return JsonResponse({'championships': list(championships)})

def home(request):
    sports = Sport.objects.all()
    return render(request, 'home.html', {'sports': sports})

def championships(request, sport_id):
    sport = Sport.objects.get(pk=sport_id)
    championships = sport.championship_set.all()
    return render(request, 'championships.html', {'sport': sport, 'championships': championships})

def players(request, championship_id):
    championship = Championship.objects.get(pk=championship_id)
    players = championship.player_set.all()
    return render(request, 'players.html', {'championship': championship, 'players': players})

def player_stats(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    games = Game.objects.filter(player=player).order_by('-game_start')[:20]

    # Aggregating stats
    stats = {
        'points': [game.player_points for game in games],
        'assists': [game.player_assists for game in games],
        'turnovers': [game.player_turnovers for game in games],
        'ftm': [game.player_ftm for game in games],
        'tpm': [game.player_tpm for game in games],
        'game_dates': [game.game_start.strftime('%Y-%m-%d') for game in games],
    }

    # Convert stats to JSON format for JavaScript
    stats_json = json.dumps(stats)
    return render(request, 'player_stats.html', {'player': player, 'stats_json': stats_json})

def player_predictions(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    predictions = Predictions.objects.filter(player=player)
    return render(request, 'player_predictions.html', {'player': player, 'predictions': predictions})

def championship_players(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    players = championship.player_set.all()
    return render(request, 'championship_players.html', {'championship': championship, 'players': players})

def player_list(request, championship_id, category):
    championship = get_object_or_404(Championship, pk=championship_id)
    players = championship.player_set.all()
    return render(request, 'player_list.html', {
        'championship': championship,
        'players': players,
        'category': category
    })
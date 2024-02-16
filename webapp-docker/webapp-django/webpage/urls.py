from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_championships/<int:sport_id>/', views.get_championships, name='get_championships'),
    path('championships/<int:sport_id>/', views.championships, name='championships'),
    path('championship/<int:championship_id>/<str:category>/players/', views.player_list, name='player_list'),
    path('player/<int:player_id>/stats/', views.player_stats, name='player_statistics'),
    # path('player/<int:player_id>/odds/', views.player_odds, name='player_odds'),
    path('player/<int:player_id>/predictions/', views.player_predictions, name='player_predictions'),
]
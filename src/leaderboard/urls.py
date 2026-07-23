from django.urls import path
from .views import  ListLeagueStandingsView, LeagueStandingsView

app_name = "leaderboard"

urlpatterns = [
    path("", ListLeagueStandingsView.as_view(), name="league-list"),
    path("<slug:slug>/standings/", LeagueStandingsView.as_view(), name="league-standings"),


]
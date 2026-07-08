from django.urls import path
from .views import RoundMatchListView, PredictionEditView, CurrentRoundRedirectView, \
    LeaguesList, LeagueDetail, LeaguesListAll

app_name = "predictions"

urlpatterns = [
    path("leagues/all", LeaguesListAll.as_view(), name="leagues_all_list"),
    path("leagues/", LeaguesList.as_view(), name="leagues_list"),
    path("leagues/<int:pk>/", LeagueDetail.as_view(), name="league_detail"),
    path("round/current/", CurrentRoundRedirectView.as_view(),
         name="current_round"),
    path("round/<int:round_id>/matches/", RoundMatchListView.as_view(),
         name="round_matches"),
    path("match/<int:match_id>/predict/", PredictionEditView.as_view(),
         name="create_prediction"),
]
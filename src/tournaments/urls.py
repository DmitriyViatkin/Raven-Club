from django.urls import path
from .views import TournamentsDetail

app_name = "tournaments"

urlpatterns = [
    path("<int:pk>/", TournamentsDetail.as_view(), name="detail"),
]
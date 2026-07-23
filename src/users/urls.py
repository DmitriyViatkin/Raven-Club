from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView
from ..core.urls import urlpatterns

urlpatterns += [
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),
path(
        "profile/edit/", UserProfileUpdateView.as_view(), name="user_profile_edit"
    ),

]

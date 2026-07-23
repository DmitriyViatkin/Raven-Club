from django.urls import path
from .views import Register, UserLoginView


urlpatterns = [
                path ('register/', Register.as_view(), name='register'),
path('login/',UserLoginView.as_view(), name='login'),
]
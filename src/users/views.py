from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from src.users.models import Player
from django.urls import reverse_lazy
from src.users.forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash

class UserProfileDetailView (LoginRequiredMixin,DetailView):

     model = Player
     template_name = "users/profile_detail.html"
     context_object_name = "player"

     def get_object(self, queryset=None):
         return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class =  UserProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        # Редактируем текущего залогиненного юзера
        return self.request.user

    def form_valid(self, form):
        # Сначала сохраняем форму (и пароль, если он был введен)
        response = super().form_valid(form)

        # Если пароль менялся, обновляем хэш сессии, чтобы юзера не выкинуло из системы
        if form.cleaned_data.get("new_password"):
            update_session_auth_hash(self.request, self.object)

        return response
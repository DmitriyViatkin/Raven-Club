from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import PlayerCreationForm

from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    template_name = 'registration/login1.html'
    redirect_authenticated_user = True


class Register(View):
    template_name = 'authentication/register.html'

    def get(self, request):
        context = {'form': PlayerCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        context = {'form': form}
        return render(request, self.template_name, context)
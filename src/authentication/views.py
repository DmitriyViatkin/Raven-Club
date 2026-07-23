from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import PlayerCreationForm


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
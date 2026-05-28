from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm

class Register(View):
    template_name = 'authentication/register.html'

    def get(self, request):
        context = {'form': UserCreationForm()}
        return render(request, self.template_name, context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        context = {'form': form}
        return render(request, self.template_name, context)
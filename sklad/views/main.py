from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from sklad.forms import AuthForm


@method_decorator(login_required, name='dispatch')
class Dashboard(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Панель управления'
        return context


@method_decorator(login_required, name='dispatch')
class Logout(generic.View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class Login(generic.FormView):
    template_name = 'login.html'
    form_class = AuthForm

    def get_success_url(self):
        return reverse('dashboard', kwargs={})

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

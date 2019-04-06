from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from sklad.forms import LiquidCreateForm, LainCreateForm
from sklad.models import Liquids, Lain


@method_decorator(login_required, name='dispatch')
class LiquidsListView(generic.ListView):
    template_name = 'liquids_list_view.html'
    model = Liquids
    context_object_name = 'liquids'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жидкости и линейки'
        context['category_type'] = 'liquids'
        context['lains'] = Lain.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class CreateLiquid(generic.CreateView):
    template_name = 'create_view.html'
    form_class = LiquidCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая жидкость'
        context['category_type'] = 'liquids'
        return context

    def get_success_url(self):
        return reverse('liquid_list', kwargs={})


@method_decorator(login_required, name='dispatch')
class GetLiquidsList(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('id'):
            liquids = list(Liquids.objects.filter(
                name_lain=self.request.GET.get('id')).values())
        else:
            liquids = list(Liquids.objects.values())
        return JsonResponse(liquids, safe=False)


@method_decorator(login_required, name='dispatch')
class CreateLain(generic.CreateView):
    template_name = 'create_view.html'
    form_class = LainCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая линейка'
        context['category_type'] = 'liquids'
        return context

    def get_success_url(self):
        return reverse('liquid_list', kwargs={})

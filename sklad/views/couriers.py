from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from sklad.forms import CourierCreateForm
from sklad.models import Courier


@method_decorator(login_required, name='dispatch')
class CourierListView(generic.ListView):
    template_name = 'couriers_list.html'
    model = Courier
    context_object_name = 'couriers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Курьерские службы'
        context['category_type'] = 'couriers'
        return context


@method_decorator(login_required, name='dispatch')
class CreateCourier(generic.CreateView):
    template_name = 'create_view.html'
    form_class = CourierCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая курьерская служба'
        context['category_type'] = 'couriers'
        return context

    def get_success_url(self):
        return reverse('courier_list', kwargs={})

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from sklad.forms import DeliveryCreateForm, DeliveryForm, OrderCreateForm, \
    OutCreateForm
from sklad.models import Order, Out, Lain


@method_decorator(login_required, name='dispatch')
class ListOrder(generic.ListView):
    template_name = 'orders_list_view.html'
    model = Order
    queryset = model.objects.filter(status__in=[1, 2])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказы'
        context['category_type'] = 'orders'
        context['tbl_titles'] = [f.name for f in self.model._meta.get_fields()]
        return context


@method_decorator(login_required, name='dispatch')
class DetailOrder(generic.DetailView):
    template_name = 'orders_detail_view.html'
    model = Order
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказ №' + str(self.object.num_order)
        context['delivery_form'] = DeliveryCreateForm
        context['category_type'] = 'orders'
        return context


@method_decorator(login_required, name='dispatch')
class SendDelivery(generic.View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            outs_data = json.loads(self.request.POST['outs'])
            delivery_data = json.loads(self.request.POST['delivery'])
            order = Order.objects.get(id=self.request.POST['id'])

            outs = [outs[4:] for outs in outs_data]

            for out_id in outs:
                out = Out.objects.get(id=int(out_id))
                out.include = True
                out.save()

            delivery_data['num_order'] = order.pk

            delivery = DeliveryForm(data=delivery_data)
            if delivery.is_valid():
                delivery.save()

            return JsonResponse({'status': 'ok'}, status=200)

        return JsonResponse({'errors': 'bad request'}, status=403)


@method_decorator(login_required, name='dispatch')
class CreateOrder(generic.CreateView):
    template_name = 'orders_create_view.html'
    form_class = OrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый заказ'
        context['outsform'] = OutCreateForm
        context['category_type'] = 'orders'
        context['lains'] = Lain.objects.all()
        return context

    def get_success_url(self):
        return reverse('order_list', kwargs={})

    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.POST['data'])
        order_data = data['order']
        outs = data['outs']
        order = OrderCreateForm(data=order_data)
        if order.is_valid():
            order = order.save()

            for index in outs:
                out_data = outs[index]
                out = OutCreateForm(data=out_data)
                if out.is_valid():
                    out = out.save(commit=False)
                    out.include = False
                    out.num_order = order
                    out.save()

            return JsonResponse({'order_id': order.id}, status=200)

        return JsonResponse({'errors': 'bad request'}, status=403)

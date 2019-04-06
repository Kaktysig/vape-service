from django.urls import path

from sklad.views import main, liquids, orders, couriers

urlpatterns = [
    path('', main.Dashboard.as_view(), name='dashboard'),
    path('login', main.Login.as_view(), name='login'),
    path('liquids/add', liquids.CreateLiquid.as_view(), name='add_liquid'),
    path('liquids/lain/add', liquids.CreateLain.as_view(), name='add_lain'),
    path('couriers/list', couriers.CourierListView.as_view(),
         name='courier_list'),
    path('couriers/add', couriers.CreateCourier.as_view(),
         name='add_courier'),
    path('liquids/list', liquids.LiquidsListView.as_view(),
         name='liquid_list'),
    path('order/add', orders.CreateOrder.as_view(), name='add_order'),
    path('order/list', orders.ListOrder.as_view(), name='order_list'),
    path('order/detail/<int:pk>', orders.DetailOrder.as_view(),
         name='order_detail'),
    path('order/delivery', orders.SendDelivery.as_view(),
         name='send_delivery'),
    path('liquids/api/liquids/list', liquids.GetLiquidsList.as_view(),
         name='api_liquids'),
    path('logout', main.Logout.as_view(), name='logout'),
]

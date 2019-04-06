from django.contrib import admin

from sklad.models import Order, Out, Delivery, Liquids, Courier, Lain


class OutAdmin(admin.TabularInline):
    model = Out


class DeliveryAdmin(admin.TabularInline):
    model = Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["status", ]
    inlines = [OutAdmin, DeliveryAdmin]
    list_display = [
        'num_order',
        'customer',
        'status',
    ]
    list_filter = [
        'customer',
        'status',
    ]


@admin.register(Lain)
class LainAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(Liquids)
class LiquidsAdmin(admin.ModelAdmin):
    list_display = [
        'name_ex',
        'name_lain',
        'volume',
        'price',
    ]
    list_filter = [
        'name_lain',
        'volume',
    ]


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = [
        'courier_name',
        'phone'
    ]

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from sklad.models import Order, Liquids, Out, Delivery, Lain, Courier


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = (
            'status',
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LiquidCreateForm(forms.ModelForm):
    class Meta:
        model = Liquids
        fields = '__all__'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LainCreateForm(forms.ModelForm):
    class Meta:
        model = Lain
        fields = '__all__'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CourierCreateForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = '__all__'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AuthForm(AuthenticationForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class DeliveryCreateForm(forms.ModelForm):
    class Meta:
        model = Delivery
        exclude = ['num_order', ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        exclude = ()


class OutCreateForm(forms.ModelForm):
    class Meta:
        model = Out
        exclude = [
            'num_order',
            'include',
        ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

from django.db import models


# таблица заказов
class Order(models.Model):
    _statuses = (
        (1, "Объявлен"),
        (2, "Открыт"),
        (3, "Завершён"),
    )
    num_order = models.IntegerField(verbose_name="Номер заказа")
    customer = models.CharField(max_length=80, verbose_name="Заказчик")
    status = models.IntegerField(choices=_statuses, default=1,
                                 verbose_name="Статус заказа")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.outs.count() == self.outs.filter(include=True).count():
            self.status = 3
        elif self.outs.count() != self.outs.filter(include=False):
            self.status = 2
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    def get_status(self):
        return dict(self._statuses)[self.status]

    def __str__(self):
        return str(self.num_order)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


# Курьерские службы
class Courier(models.Model):
    courier_name = models.CharField(max_length=100, default="",
                                    verbose_name="название")
    phone = models.CharField(max_length=15, verbose_name="Телефон")

    def __str__(self):
        return self.courier_name

    class Meta:
        verbose_name = 'курьерская служба'
        verbose_name_plural = 'курьерские службы'


# таблица отправленияй со склада
class Out(models.Model):
    num_order = models.ForeignKey(Order, on_delete=models.CASCADE,
                                  related_name="outs",
                                  verbose_name="Номер заказа")
    name_ex = models.ForeignKey('Liquids', on_delete=models.CASCADE,
                                verbose_name="жидкость")
    qt = models.IntegerField(verbose_name="Количество")
    include = models.BooleanField(default=False, verbose_name="Отправляем?")
    date = models.DateField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)
        self.num_order.save()

    def __str__(self):
        return '{0} для {1}'.format(self.name_ex, self.num_order.num_order)

    class Meta:
        verbose_name = 'партия'
        verbose_name_plural = 'партии'

    @property
    def liquid_lain(self):
        return self.name_ex.name_lain.name

    @property
    def liquid_volume(self):
        return self.name_ex.volume


# таблица заказов на доставку
class Delivery(models.Model):
    num_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tr_num = models.CharField(max_length=200, verbose_name="Трек-номер")
    courier_name = models.ForeignKey(Courier, on_delete=models.CASCADE,
                                     verbose_name="Курьер")
    sum_delivery = models.FloatField(default=0,
                                     verbose_name="Стоимость доставки")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return '{0} от {1}.{2}.{3}'.format(
            self.num_order.num_order, self.date.day,
            self.date.month, self.date.year
        )

    class Meta:
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'


class Lain(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'линейка'
        verbose_name_plural = 'линейки'


#  таблица товаров
class Liquids(models.Model):
    name_lain = models.ForeignKey(Lain,
                                  on_delete=models.CASCADE,
                                  verbose_name="линейка")
    name_ex = models.CharField(max_length=200, verbose_name="Название")
    volume = models.CharField(max_length=50, verbose_name="Объём")
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                default=0, verbose_name="Цена")

    def __str__(self):
        return self.name_ex + ' (' + self.volume + 'мл)'

    class Meta:
        verbose_name = 'жидкость'
        verbose_name_plural = 'жидкости'



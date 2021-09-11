from django.db import models


class Order(models.Model):
    buyer = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name='买家')

    price_integer = models.BigIntegerField(verbose_name='整数部分', default=0)
    price_decimal = models.IntegerField(verbose_name='小数部分', default=0)

    paid = models.BooleanField(verbose_name='付款', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.buyer.username

    def get_detail(self):
        return OrderDetail.objects.filter(order=self)


class OrderDetail(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.PROTECT, verbose_name='订单')
    snapshot = models.ForeignKey('course.CourseSnapshot', on_delete=models.PROTECT, verbose_name='课程')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order

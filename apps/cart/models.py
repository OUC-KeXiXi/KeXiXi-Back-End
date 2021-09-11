from django.db import models


class Cart(models.Model):
    buyer = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name='买家')

    course = models.ForeignKey('course.Course', on_delete=models.PROTECT, verbose_name='课程')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.buyer.username

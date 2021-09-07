from django.db import models


class AccountRole:
    Buyer = 0
    Seller = 1


class Account(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名', unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, verbose_name='密码', null=False, blank=False)
    email = models.EmailField(verbose_name='邮箱', unique=True, null=False, blank=False)

    role = models.CharField(max_length=1, verbose_name='角色',
                            choices=((AccountRole.Buyer, '买家'), (AccountRole.Seller, '卖家')),
                            null=False, blank=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @property
    def info(self):
        return AccountInfo.objects.filter(account=self)[0]


class AccountInfo(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name='用户')
    nickname = models.CharField(max_length=50, verbose_name='昵称', null=False, blank=True, default='')
    avatar = models.CharField(max_length=50, verbose_name='头像', null=False, blank=False, default='/media/default.png')

    balance_integer = models.BigIntegerField(verbose_name='余额整数部分', default=0)
    balance_decimal = models.IntegerField(verbose_name='余额小数部分', default=0)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.account.username

    def gain(self, integer, decimal):
        self.balance_integer += integer

        decimal_part = self.balance_decimal + decimal
        self.balance_integer += decimal_part // 100
        self.balance_decimal = decimal_part % 100

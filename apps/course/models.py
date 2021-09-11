from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='课程名', unique=False, null=False, blank=False)
    seller = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name='卖家')
    published = models.BooleanField(verbose_name='上架', default=False)

    sales = models.BigIntegerField(verbose_name='销量', default=0)
    pinned = models.BooleanField(verbose_name='置顶', default=False)
    tags = models.ManyToManyField('course.CourseTag', verbose_name='课程标签')
    deleted = models.BooleanField(verbose_name='删除', default=False)

    def get_courses_list(self):
        return CourseSnapshot.objects.filter(root=self)

    def get_latest_course(self):
        return CourseSnapshot.objects.filter(root=self).last()


class CourseSnapshot(models.Model):
    root = models.ForeignKey('course.Course', on_delete=models.PROTECT, verbose_name='课程ID')

    title = models.CharField(max_length=100, verbose_name='课程名', unique=False, null=False, blank=False)
    content = models.TextField(verbose_name='介绍', null=False, blank=False)
    cover = models.CharField(max_length=100, verbose_name='封面')

    price_integer = models.BigIntegerField(verbose_name='整数部分', default=0)
    price_decimal = models.IntegerField(verbose_name='小数部分', default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程快照'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class CourseTag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名', unique=True, null=False, blank=False)

    class Meta:
        verbose_name = '课程标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

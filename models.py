from django.db import models


class PythonInfo(models.Model):
    version = models.CharField(verbose_name='版本', max_length=50)
    is_install = models.BooleanField(verbose_name='安装状态', default=False)
    is_used = models.BooleanField(verbose_name='是否使用', default=False)
    orders = models.IntegerField(verbose_name='排序', default=1)
    is_default = models.BooleanField(verbose_name='默认版本', default=False)
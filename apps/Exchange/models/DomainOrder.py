from django.db import models


class DomainOrder(models.Model):
    """
    域名解析
    """
    domain_name = models.CharField(max_length=30, verbose_name='域名', primary_key=True)
    ip = models.CharField(max_length=30, verbose_name='ip', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    kind = models.CharField(max_length=20, verbose_name='网络类型', null=True, blank=True)

    class Meta:
        verbose_name = '域名解析表'
        verbose_name_plural = verbose_name
        db_table = 'domain_order'

    def __str__(self):
        return self.domain_name

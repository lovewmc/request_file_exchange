from django.db import models


class RequestHistoryOrder(models.Model):
    """
    请求记录表
    """
    STATUS_CHOICES = (
        ('1', "请求成功"),
        ('2', "生成文件"),
        ('3', "读取文件"),
        ('4', "返回结果"),
    )

    file_id = models.CharField(max_length=50, verbose_name='文件id', primary_key=True)
    identity_code = models.CharField(max_length=30, verbose_name='请求id', null=True, blank=True)
    data = models.TextField(verbose_name='请求数据', null=True, blank=True)
    received_time = models.DateTimeField(verbose_name='接收请求时间', null=True, blank=True)
    create_file_time = models.DateTimeField(verbose_name='生成文件时间', null=True, blank=True)
    read_file_time = models.DateTimeField(verbose_name='读取文件时间', null=True, blank=True)
    return_time = models.DateTimeField(verbose_name='返回结果时间', null=True, blank=True)
    # 状态机
    status = models.CharField(max_length=10,verbose_name='状态', choices=STATUS_CHOICES, null=True, blank=True)

    finish_tag = models.BooleanField(verbose_name='完成标记', default=False)

    class Meta:
        verbose_name = '请求记录表'
        verbose_name_plural = verbose_name
        db_table = 'request_order'

    def __str__(self):
        return self.file_id

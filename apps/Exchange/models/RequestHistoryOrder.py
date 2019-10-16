from django.db import models


class RequestHistoryOrder(models.Model):
    """
    请求记录表
    """
    WRITE_STATUS_CHOICES = (
        ('0', '初始状态'),
        ('1', "接收请求"),
        ('2', "生成文件"),
    )

    READ_STATUS_CHOICES = (
        ('0', '初始状态'),
        ('1', "读取文件"),
        ('2', "请求成功"),
    )

    REQUEST_STATUS_CHOICES = (
        ('0', '初始状态'),
        ('1', '请求'),
        ('2', '返回'),
    )
    unique_code = models.CharField(max_length=80, verbose_name='唯一标识', primary_key=True)
    identity_code = models.CharField(max_length=50, verbose_name='请求id', null=True, blank=True)
    request_data = models.TextField(verbose_name='请求数据', null=True, blank=True)
    response_data = models.TextField(verbose_name='返回数据', null=True, blank=True)
    received_time = models.DateTimeField(verbose_name='接收请求时间', null=True, blank=True)
    create_file_time = models.DateTimeField(verbose_name='生成文件时间', null=True, blank=True)
    read_file_time = models.DateTimeField(verbose_name='读取文件时间', null=True, blank=True)
    return_time = models.DateTimeField(verbose_name='请求成功时间', null=True, blank=True)
    # 状态机
    write_status = models.CharField(max_length=10, verbose_name='写状态', choices=WRITE_STATUS_CHOICES, default='0')
    read_status = models.CharField(max_length=10, verbose_name='读状态', choices=READ_STATUS_CHOICES, default='0')

    finish_tag = models.BooleanField(verbose_name='完成标记', default=False)
    request_flag = models.CharField(max_length=10, verbose_name='请求标志', choices=REQUEST_STATUS_CHOICES, default='0')

    class Meta:
        verbose_name = '请求记录表'
        verbose_name_plural = verbose_name
        db_table = 'request_order'

    def __str__(self):
        return self.unique_code

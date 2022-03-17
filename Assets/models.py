from django.db import models

# Create your models here.
from django.db import models
from django.utils.html import format_html


class AssetList(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    ip_address = models.GenericIPAddressField(db_column="ip_address", verbose_name='IP地址')
    top_level_domain = models.CharField(db_column="top_level_domain", max_length=256, verbose_name='主域名', null=True, blank=True)
    subdomain = models.CharField(db_column="subdomain", max_length=256, verbose_name='子域名', null=True, blank=True)
    cname = models.CharField(db_column="cname", max_length=256, verbose_name='别名', null=True, blank=True)
    system = models.CharField(db_column="system", max_length=50, verbose_name='操作系统', null=True, blank=True)
    port = models.IntegerField(db_column="port", verbose_name='端口', null=True, blank=True)
    state_choices = (("0", "关闭"), ("1", "开放"), ("2", "阻断"))
    state = models.CharField(max_length=2, choices=state_choices, verbose_name='端口状态', null=True, blank=True)
    protocol = models.CharField(db_column="protocol", max_length=50, verbose_name='协议', null=True, blank=True)
    service = models.CharField(db_column="service", max_length=50, verbose_name='服务', null=True, blank=True)
    software = models.CharField(db_column="software", max_length=50, verbose_name='组件', null=True, blank=True)
    version = models.CharField(db_column="version", max_length=50, verbose_name='版本', null=True, blank=True)
    website_title = models.CharField(db_column="website_title", max_length=256, verbose_name='站点标题', null=True, blank=True)
    middle_ware = models.CharField(db_column="middle_ware", max_length=512, verbose_name='组件/框架', null=True, blank=True)
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='创建时间', auto_now=True)

    def __str__(self):
        return str(self.ip_address) + ":" + str(self.port)

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                    '<input name="编辑"' \
                    'type="button" id="passButton" ' \
                    'title="passButton" value="编辑">' \
                    '</a>'
        return format_html(btn_str, '%s/change'%self.id)
    change.short_description = '资产编辑'

    class Meta:
        verbose_name = '资产信息'
        verbose_name_plural = verbose_name


class AssetTask(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    name = models.CharField(db_column="name", max_length=50, verbose_name='任务名称')
    top_level_domain = models.CharField(db_column="top_level_domain", max_length=256,  verbose_name='主域名')
    port_scan_type_choices = (("0", "关键端口"), ("1", "常用端口"), ("2", "全端口"))
    port_scan_type = models.CharField(max_length=2, choices=port_scan_type_choices, verbose_name='端口自类型', default="0")
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='创建时间', auto_now=True)

    def __str__(self):
        return self.name

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '任务编辑'

    class Meta:
        verbose_name = '扫描任务'
        verbose_name_plural = verbose_name
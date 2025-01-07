from django.db import models
from Assets.models import AssetList
from django.utils.html import format_html


# Create your models here.
class NucleiPoCRegister(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    exploit_name = models.CharField(max_length=32, db_column="exploit_name", verbose_name='负载名称')
    category_choices = (("1", "WEB漏洞"), ("2", "系统漏洞"))
    category = models.CharField(max_length=2, choices=category_choices, verbose_name='漏洞类型')
    target = models.ForeignKey(AssetList, verbose_name="调试目标", on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=100, db_column="filename", verbose_name='文件名称', default="")
    yamlcode = models.TextField(db_column="yamlcode", null=True, verbose_name="负载代码(仅支持yaml)")
    description = models.TextField(db_column="description", verbose_name='负载描述')
    debug_info = models.TextField(db_column="debug_info", verbose_name='调试信息', default="", null=True, blank=True)
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='创建时间', auto_now=True)

    def __str__(self):
        return self.exploit_name

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑负载"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '负载编辑'

    class Meta:
        verbose_name = '负载管理'
        verbose_name_plural = verbose_name


class NucleiScanTasks(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='编号')
    name = models.CharField(max_length=32, db_column="name", verbose_name='任务名称')
    target = models.ForeignKey(AssetList, verbose_name="目标选择", on_delete=models.CASCADE, null=True, blank=True)
    targets = models.TextField(db_column="targets", verbose_name='目标群', null=True, blank=True)
    exploit = models.ForeignKey(NucleiPoCRegister, verbose_name="漏洞负载选择", on_delete=models.CASCADE, default=None)
    notice = models.BooleanField(db_column='notice', verbose_name="是否钉钉通知", default=False)
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='创建时间', auto_now=True)  # 截止日期

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑任务"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '任务编辑'

    class Meta:
        verbose_name = '任务项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NucleiScanResult(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    task_id = models.IntegerField(db_column="task_id", verbose_name='对应工单序号')
    task_name = models.CharField(max_length=32, db_column="task_name", verbose_name='工单名称')
    ip_address = models.GenericIPAddressField(db_column="ip_address", verbose_name='目标地址')
    port = models.IntegerField(db_column="port", verbose_name='目标端口', null=True)
    result_flag = models.BooleanField(db_column="result_flag", verbose_name='测试结果')
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='结束时间', auto_now=True)

    def __str__(self):
        return "%s号工单" % str(self.task_id)

    def detail(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="查看详情"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="查看">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % str(self.id))

    detail.short_description = '工单详情'

    class Meta:
        verbose_name = '扫描结果'
        verbose_name_plural = verbose_name

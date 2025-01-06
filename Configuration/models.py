# Create your models here.
from django.db import models
from django.utils.html import format_html


class Configuration(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    name_choices = (
        ("1", "VT接口"),
        ("2", "钉钉接口"),
        ("3", "Github接口"),
        ("4", "钟馗接口"),
        ("5", "佛法接口"),
        ("6", "线程数"),
        ("7", "系统地址"),
        ("8", "系统域名"),
        ("9", "常用端口"),
        ("10", "关键端口"),
        ("11", "Nuclei路径")
    )
    name = models.CharField(unique=True, max_length=2, choices=name_choices, verbose_name='配置名称')
    user = models.CharField(db_column="user", max_length=128, verbose_name='用户名', null=True, blank=True)
    value = models.CharField(db_column="value", max_length=512, verbose_name='Token令牌', null=True, blank=True)
    port = models.TextField(db_column="port", verbose_name='端口列表', null=True, blank=True)
    ipaddress = models.GenericIPAddressField(db_column="ipaddress", verbose_name='系统地址', null=True, blank=True, default="127.0.0.1")
    domain = models.CharField(db_column="domain", max_length=256, verbose_name='系统域名', default="apollo.local", null=True, blank=True)
    count = models.IntegerField(db_column="count", verbose_name='配置值', default=10, null=True, blank=True)
    nuclei = models.CharField(db_column="nuclei", max_length=256, verbose_name="Nuclei路径", null=True, blank=True)
    
    def __str__(self):
        for item in self.name_choices:
            if self.name == item[0]:
                return item[1]

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '配置编辑'

    class Meta:
        verbose_name = '配置信息'
        verbose_name_plural = verbose_name


class Services(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    name_choices = (
        ("1", "HTTP服务"),
        ("2", "DNS服务")
    )
    name = models.CharField(unique=True, max_length=2, choices=name_choices, verbose_name='配置名称')
    port = models.IntegerField(db_column="port", verbose_name='端口')
    ip_address = models.GenericIPAddressField(db_column="ip_address", verbose_name='地址', default="127.0.0.1")
    state = models.BooleanField(db_column="state", verbose_name='服务开启', default=False, editable=False)

    def __str__(self):
        for item in self.name_choices:
            if self.name == item[0]:
                return item[1]

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '配置编辑'

    class Meta:
        verbose_name = '服务配置'
        verbose_name_plural = verbose_name


class ServicesLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    name = models.CharField(max_length=20, verbose_name='日志类型', editable=False)
    ip_address = models.GenericIPAddressField(db_column="ip_address", verbose_name='源地址', editable=False)
    method = models.CharField(max_length=20, verbose_name='请求类型', editable=False, default="GET")
    message = models.CharField(max_length=256, verbose_name='访问记录', editable=False)
    status = models.CharField(max_length=20, verbose_name='响应码', editable=False, default="200")
    timestamp = models.DateTimeField(db_column="timestamp", verbose_name='记录时间', auto_now=True, editable=False)

    def __str__(self):
        return str(self.id)


class Worker(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    name = models.CharField(max_length=20, db_column="name", verbose_name='员工姓名', editable=True)
    worker_id = models.CharField(max_length=10, db_column="worker_id", verbose_name="员工工号", editable=True)
    gender_choice = (("0", "女"), ("1", "男"))
    gender = models.CharField(max_length=2, db_column="gender", choices=gender_choice, verbose_name='性别', editable=True)
    department = models.CharField(max_length=20, db_column="department", verbose_name='所在部门', editable=True)
    
    def __str__(self):
        return self.name

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '员工编辑'

    class Meta:
        verbose_name = '员工配置'
        verbose_name_plural = verbose_name


class DutyTable(models.Model):
    id = models.AutoField(primary_key=True, db_column="id", verbose_name='序号')
    worker = models.ForeignKey(Worker, verbose_name="值班人", on_delete=models.SET_NULL, default=None, null=True)
    date = models.DateField(db_column="date", verbose_name='值班时间')
    weekday_choices = (
        ("0", "周一"),
        ("1", "周二"),
        ("2", "周三"),
        ("3", "周四"),
        ("4", "周五"),
        ("5", "周六"),
        ("6", "周日")
    ) 
    weekday = models.CharField(max_length=2, choices=weekday_choices, verbose_name='星期', default="0")
    overtime_choices = (
            ("0", "周末值班"), 
            ("1", "元旦值班"), 
            ("2", "春节值班"), 
            ("3", "清明值班"),
            ("4", "五一值班"),
            ("5", "端午值班"),
            ("6", "中秋值班"),
            ("7", "国庆值班"),
            ("8", "护网值班"),
            ("9", "日常值班")
    )
    overtime_type = models.CharField(max_length=2, choices=overtime_choices, verbose_name='值班类型', default="9")
    work_type_choices = (("0", "现场"), ("1", "远程"))
    work_type = models.CharField(max_length=2, choices=work_type_choices, verbose_name='值班方式', default="0")

    def __str__(self):
        return "%s 排班" % str(self.date)

    def change(self):
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="编辑"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="编辑">' \
                  '</a>'
        return format_html(btn_str, '%s/change' % self.id)

    change.short_description = '排班编辑'

    class Meta:
        verbose_name = "值班表"
        verbose_name_plural = verbose_name

import threading
from django.db import transaction
from django.contrib import admin, messages
from Assets.views import assets_scan, detail
from Assets.models import AssetTask, AssetList
from Configuration.models import Configuration


# Register your models here.
admin.site.site_header = '长城汽车自动化攻击评估系统'  # 设置header
admin.site.site_title = '长城汽车自动化攻击评估系统'  # 设置title


@admin.register(AssetTask)
class AssetTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'top_level_domain', 'port_scan_type', 'timestamp', 'change']
    list_filter = ['top_level_domain', 'timestamp']
    search_fields = ['name', 'top_level_domain']
    ordering = ["id"]
    date_hierarchy = 'timestamp'

    @transaction.atomic
    def scan(self, request, queryset):
        try:
            Configuration.objects.filter(name="1").values_list("value")[0][0]
        except Exception as execption:
            print(execption)
            messages.add_message(request, messages.SUCCESS, '请配置VT接口Token')
            return
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                thread = threading.Thread(target=assets_scan, args=(work_id,))
                thread.start()
                messages.add_message(request, messages.SUCCESS, '开始扫描%s' % str(work_id))
        else:
            messages.add_message(request, messages.SUCCESS, '扫描异常')

    scan.short_description = "启动扫描"
    scan.icon = 'fa fa-rocket'
    scan.style = 'color:white;'
    scan.type = 'danger'
    scan.confirm = '您确定要启动扫描吗？'
    actions = [scan, ]




@admin.register(AssetList)
class AssetListAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'top_level_domain', 'subdomain', 'cname', 'system', 'port', 'state', 'protocol', 'service',
                    'software', 'version', 'middle_ware', 'timestamp', 'change']
    list_filter = ['ip_address', 'top_level_domain', 'system', 'port', 'state', 'protocol', 'service', 'software',
                   'middle_ware', 'timestamp']
    search_fields = ['ip_address', 'top_level_domain', 'subdomain', 'cname', 'system', 'port', 'state', 'protocol',
                     'service', 'software', 'middle_ware']
    ordering = ["id"]
    date_hierarchy = 'timestamp'

    @transaction.atomic
    def detail(self, request, queryset):
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                thread = threading.Thread(target=detail, args=(work_id,))
                thread.start()
                messages.add_message(request, messages.SUCCESS, '详情扫描%s' % str(work_id))
        else:
            messages.add_message(request, messages.SUCCESS, '扫描异常')

    detail.short_description = "详情扫描"
    detail.icon = 'fa fa-rocket'
    detail.style = 'color:white;'
    detail.type = 'danger'
    detail.confirm = '您确定要启动详情扫描吗？'
    actions = [detail, ]


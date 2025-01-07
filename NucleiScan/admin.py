import threading
from django.db import transaction
from django.contrib import admin, messages
from ApolloScanner.dingtalk import dingtalker
from Configuration.models import Configuration
from import_export.admin import ImportExportModelAdmin
from NucleiScan.views import start_scan, debug
from NucleiScan.models import NucleiScanTasks, NucleiPoCRegister, NucleiScanResult

# Register your models here.
admin.site.site_header = '阿波罗自动化攻击评估系统'  # 设置header
admin.site.site_title = '阿波罗自动化攻击评估系统'  # 设置title


@admin.register(NucleiPoCRegister)
class NucleiPoCRegisterAdmin(admin.ModelAdmin):
    list_display = ['exploit_name', 'category', 'yamlcode', 'debug_info', 'timestamp', 'change']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ["-id"]
    date_hierarchy = 'timestamp'

    @transaction.atomic
    def scan(self, request, queryset):
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                thread = threading.Thread(target=debug, args=(work_id,))
                thread.start()
                messages.add_message(request, messages.SUCCESS, '开始调试%s' % str(work_id))
        else:
            messages.add_message(request, messages.SUCCESS, '调试异常')

    scan.short_description = "启动调试"
    scan.icon = 'fa fa-rocket'
    scan.style = 'color:white;'
    scan.type = 'danger'
    scan.confirm = '您确定要启动调试吗？'
    actions = [scan, ]


@admin.register(NucleiScanTasks)
class NucleiScanTasksAdmin(admin.ModelAdmin):
    list_display = ['name', 'target', 'exploit', 'change']
    list_filter = ['target', 'exploit']
    search_fields = ['name']
    ordering = ["-id"]
    date_hierarchy = 'timestamp'

    @transaction.atomic
    def scan(self, request, queryset):
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                notice = NucleiScanTasks.objects.filter(id=work_id).values_list("notice")[0][0]
                if notice == 1:
                    try:
                        token = Configuration.objects.filter(name="2").values_list('value')[0][0]
                        dingtalker.set_token(token)
                    except Exception as exception:
                        messages.add_message(request, messages.SUCCESS, '请配置钉钉接口Token')
                        return
                thread = threading.Thread(target=start_scan, args=(work_id,))
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


@admin.register(NucleiScanResult)
class NucleiScanResultAdmin(ImportExportModelAdmin):
    list_display = ['task_id', 'task_name', 'ip_address', 'port', 'result_flag', 'timestamp', 'detail']
    list_filter = ['result_flag', 'timestamp']
    search_fields = ['task_name', 'timestamp']
    ordering = ["-id"]
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

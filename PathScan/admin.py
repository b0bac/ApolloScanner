import threading
from PathScan.views import start_scan
from django.db import transaction
from django.contrib import admin, messages
from PathScan.models import PathScanTask, PathScanResult

# Register your models here.
admin.site.site_header = '阿波罗自动化攻击评估系统'  # 设置header
admin.site.site_title = '阿波罗自动化攻击评估系统'  # 设置title


@admin.register(PathScanTask)
class PathScanTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'target', 'timestamp', 'change']
    list_filter = []
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
                PathScanTask.objects.filter(id=work_id).update(state=False)
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


@admin.register(PathScanResult)
class PathScanResultAdmin(admin.ModelAdmin):
    list_display = ['url', 'timestamp', 'change']
    list_filter = []
    search_fields = ['name']
    ordering = ["-id"]
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

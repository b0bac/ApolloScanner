import threading
from django.db import transaction
from django.contrib import admin, messages
from Configuration.views import service_start, service_stop, init_year
from Configuration.models import Configuration, Services, ServicesLog, DutyTable, Worker

# Register your models here.
admin.site.site_header = '阿波罗自动化攻击评估系统'  # 设置header
admin.site.site_title = '阿波罗自动化攻击评估系统'  # 设置title


@admin.register(Configuration)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'value', 'count', 'port', 'ipaddress', 'domain', 'change']
    list_filter = ['name', ]
    search_fields = ['name', 'user']
    ordering = ["id"]


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ip_address', 'port', 'state', 'change']
    search_fields = ['name']
    ordering = ["id"]

    @transaction.atomic
    def start(self, request, queryset):
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                thread = threading.Thread(target=service_start, args=(work_id,))
                thread.start()
                messages.add_message(request, messages.SUCCESS, '启动服务%s' % str(work_id))
        else:
            messages.add_message(request, messages.SUCCESS, '启动服务异常')

    start.short_description = "启动服务"
    start.icon = 'fa fa-rocket'
    start.style = 'color:white;'
    start.type = 'danger'
    start.confirm = '您确定要启动服务吗？'

    @transaction.atomic
    def stop(self, request, queryset):
        work_ids = None
        for item in request.POST.lists():
            if item[0] == "_selected_action":
                work_ids = item[1]
        if isinstance(work_ids, list):
            for work_id in work_ids:
                thread = threading.Thread(target=service_stop, args=(work_id,))
                thread.start()
                messages.add_message(request, messages.SUCCESS, '停止服务%s' % str(work_id))
        else:
            messages.add_message(request, messages.SUCCESS, '停止服务异常')

    stop.short_description = "停止服务"
    stop.icon = 'fa fa-rocket'
    stop.style = 'color:white;'
    stop.type = 'danger'
    stop.confirm = '您确定要停止服务吗？'
    actions = [start, stop, ]


@admin.register(ServicesLog)
class ServicesLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ip_address', 'method', 'status', 'message', 'timestamp']
    list_filter = ['name', 'method', 'status', ]
    search_fields = ['ip_address', 'message']
    ordering = ["id"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DutyTable)
class DutyTableAdmin(admin.ModelAdmin):
    list_display = ['date', "worker", 'weekday', 'overtime_type', 'work_type']
    list_filter = ['overtime_type',  ]
    search_fields = ['worker', 'date']
    ordering = ["date"]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker_id', "department", "gender"]
    list_filter = ["gender"]
    search_fields = ['department', 'worker_id']
    ordering = ["id"]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

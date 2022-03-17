import sys
import threading
from Assets.models import AssetList
from ApolloScanner.dingtalk import dingtalker
from Configuration.models import Configuration
from VulnerableScan.models import ExploitRegister, VulnerableScanTasks, VulnerableScanResult


class MyLogger:
    def __init__(self, exp_id, debug_flag):
        self.exploit_id = exp_id
        self.debug = debug_flag

    def log(self, message):
        if not self.debug:
            return
        print(1)
        old_content = ExploitRegister.objects.filter(id=self.exploit_id).values_list("debug_info")[0][0]
        print(old_content)
        new_content = str(old_content) + str(message)
        print(new_content)
        ExploitRegister.objects.filter(id=self.exploit_id).update(debug_info=new_content)


class ResultStruts:
    def __init__(self, task_id, task_name):
        self.cursor = VulnerableScanResult.objects
        self.result = {
            "task_id": task_id,
            "task_name": task_name,
            "ip_address": None,
            "port": None,
            "result_flag": False,
        }

    def insert(self, address, port, result):
        self.result["ip_address"] = address
        self.result["port"] = int(port)
        self.result["result_flag"] = result
        self.cursor.create(**self.result)


class VulnerableScanner:
    def __init__(self, task_id, debug=False):
        self.task_name = "debug"
        self.exploit_id = task_id
        if not debug:
            self.task_name = VulnerableScanTasks.objects.filter(id=task_id).values_list("name")[0][0]
            self.exploit_id = VulnerableScanTasks.objects.filter(id=task_id).values_list("exploit")[0][0]
        try:
            self.max_thread_count = int(Configuration.objects.filter(name="6").values_list("count")[0][0])
        except Exception as exception:
            print(exception)
            self.max_thread_count = 10
        self.thread_size = 0
        self.debug = debug
        self.exploit_name = ExploitRegister.objects.filter(id=self.exploit_id).values_list("exploit_name")[0][0]
        self.exploit_code = ExploitRegister.objects.filter(id=self.exploit_id).values_list("code")[0][0]
        self.function_name = ExploitRegister.objects.filter(id=self.exploit_id).values_list("function_name")[0][0]
        self.target_id = None
        self.targets = []
        if not debug:
            self.targets = str(VulnerableScanTasks.objects.filter(id=task_id).values_list("targets")[0][0]).split(",")
            self.targets = [] if self.targets == [""] else self.targets
            self.target_id = VulnerableScanTasks.objects.filter(id=task_id).values_list("target")[0][0]
        else:
            self.target_id = ExploitRegister.objects.filter(id=task_id).values_list("target")[0][0]
        if self.target_id is not None:
            address = AssetList.objects.filter(id=self.target_id).values_list("ip_address")[0][0]
            port = AssetList.objects.filter(id=self.target_id).values_list("port")[0][0]
            self.targets.append("%s:%s" % (address, str(port)))
        self.targets = list(set(self.targets))
        self.cursor = ResultStruts(task_id, self.task_name)
        self.logger = MyLogger(self.exploit_id, self.debug)

    def function_execute_by_function_name(self, *args, **kwargs):
        exec(self.exploit_code)
        return eval(self.function_name)(*args, **kwargs)

    def verify(self, address, port):
        result = self.function_execute_by_function_name(address, port, self.logger)
        if result:
            message = "漏洞: %s %s %s\n" % (str(self.exploit_name), address, str(port))
            if not self.debug:
                dingtalker.send(message)
            self.cursor.insert(address, port, result)
        self.thread_size -= 1

    def run(self):
        for target in self.targets:
            address, port = target.split(":")
            port = int(port)
            while True:
                if self.thread_size < self.max_thread_count:
                    self.thread_size += 1
                    thread = threading.Thread(target=self.verify, args=(address, int(port),))
                    thread.start()
                    break
                else:
                    continue


def start_scan(task_id):
    scanner = VulnerableScanner(task_id)
    scanner.run()


def debug(task_id):
    scanner = VulnerableScanner(task_id, debug=True)
    scanner.run()
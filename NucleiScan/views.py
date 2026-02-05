import sys
import threading
import subprocess
from Assets.models import AssetList
from ApolloScanner.dingtalk import dingtalker
from Configuration.models import Configuration
from NucleiScan.models import NucleiPoCRegister, NucleiScanTasks, NucleiScanResult


def nuclei_scan(engine, target, templates):
    command = [engine, '-target', target, '-t', templates]
    print(command)
    try:
        result = subprocess.Popen(command, stdout=subprocess.PIPE)
        return str(result.communicate())
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e.stderr}"

def haslevel(content):
    if content.find("high") > 0:
        return True
    elif content.find("critical") > 0:
        return True
    elif content.find("medium") > 0:
        return True
    elif content.find("info") > 0:
        return True
    elif content.find("low") > 0:
        return True
    elif content.find("unknown") > 0:
        return True
    else:
        return False


def nuclei_result_parse(target, content, logger):
    logger.log(content)
    if content.find(target) > 0 and (haslevel(content)):
        return True
    elif content.find("No results found. Better luck next time!") > 0:
        return False
    else:
        return False


def NucleiScanVerify(engine, target, template, logger):
    return nuclei_result_parse(target, nuclei_scan(engine, target, template), logger)


class MyLogger:
    def __init__(self, exp_id, debug_flag):
        self.exploit_id = exp_id
        self.debug = debug_flag

    def log(self, message):
        if not self.debug:
            return
        old_content = NucleiPoCRegister.objects.filter(id=self.exploit_id).values_list("debug_info")[0][0]
        print(old_content)
        new_content = str(old_content) + str(message)
        print(new_content)
        NucleiPoCRegister.objects.filter(id=self.exploit_id).update(debug_info=new_content)


class ResultStruts:
    def __init__(self, task_id, task_name):
        self.cursor = NucleiScanResult.objects
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


class NucleiScanner:
    def __init__(self, task_id, debug=False):
        self.task_name = "debug"
        self.exploit_id = task_id
        self.engine = Configuration.objects.filter(name="11").values_list("nuclei")[0][0]
        if not debug:
            self.task_name = NucleiScanTasks.objects.filter(id=task_id).values_list("name")[0][0]
            self.exploit_id = NucleiScanTasks.objects.filter(id=task_id).values_list("exploit")[0][0]
        try:
            self.max_thread_count = int(Configuration.objects.filter(name="6").values_list("count")[0][0])
        except Exception as exception:
            print(exception)
            self.max_thread_count = 10
        self.thread_size = 0
        self.debug = debug
        self.exploit_name = NucleiPoCRegister.objects.filter(id=self.exploit_id).values_list("exploit_name")[0][0]
        self.exploit_code = NucleiPoCRegister.objects.filter(id=self.exploit_id).values_list("yamlcode")[0][0]
        self.filename = "/tmp/%s"  %str(NucleiPoCRegister.objects.filter(id=self.exploit_id).values_list("filename")[0][0])
        self.target_id = None
        self.targets = []
        if not debug:
            self.targets = str(NucleiScanTasks.objects.filter(id=task_id).values_list("targets")[0][0]).split(",")
            self.targets = [] if self.targets == [""] else self.targets
            self.target_id = NucleiScanTasks.objects.filter(id=task_id).values_list("target")[0][0]
        else:
            self.target_id = NucleiPoCRegister.objects.filter(id=self.exploit_id).values_list("target")[0][0]
        if self.target_id is not None:
            address = AssetList.objects.filter(id=self.target_id).values_list("ip_address")[0][0]
            port = AssetList.objects.filter(id=self.target_id).values_list("port")[0][0]
            domain = AssetList.objects.filter(id=self.target_id).values_list("subdomain")[0][0]
            protocol = AssetList.objects.filter(id=self.target_id).values_list("protocol")[0][0]
            if protocol is None:
                protocol = "http"
            if domain is not None:
                self.targets.append("%s://%s:%s" % (str(protocol), str(domain), str(port)))
            self.targets.append("%s://%s:%s" % (str(protocol), str(address), str(port)))
        self.targets = list(set(self.targets))
        self.cursor = ResultStruts(task_id, self.task_name)
        self.logger = MyLogger(self.exploit_id, self.debug)

    def exploit_poc_registed(self, *args, **kwargs):
        try:
            with open(self.filename, 'w') as filewriter:
                filewriter.write(self.exploit_code)
            return True
        except Exception as error:
            return False

    def verify(self, target):
        self.exploit_poc_registed()
        address = target.split("://")[1].split(":")[0]
        port = 0
        try:
            port = int(target.split(":")[-1])
        except Exception:
            port = 443 if target[0:5] == "https" else 80
        result = NucleiScanVerify(self.engine, target, self.filename, self.logger)
        self.logger.log("[*] %s [%s]" % (str(target), str(result)))
        if result:
            message = "漏洞: %s %s %s\n" % (str(self.exploit_name), address, str(port))
            if not self.debug:
                dingtalker.send(message)
            self.cursor.insert(address, port, result)
        self.thread_size -= 1

    def run(self):
        for target in self.targets:
            print(target)
            while True:
                if self.thread_size < self.max_thread_count:
                    self.thread_size += 1
                    thread = threading.Thread(target=self.verify, args=(target,))
                    thread.start()
                    break
                else:
                    continue


def start_scan(task_id):
    scanner = NucleiScanner(task_id)
    scanner.run()


def debug(task_id):
    scanner = NucleiScanner(task_id, debug=True)
    scanner.run()

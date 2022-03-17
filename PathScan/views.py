import urllib3
import requests
from ApolloScanner.settings import BASE_DIR
from Configuration.models import Configuration
from PathScan.models import PathScanTask, PathScanResult
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FileScanner(object):
    def __init__(self, task_id):
        self.task_id = task_id
        self.name = PathScanTask.objects.filter(id=task_id).values_list("name")[0][0]
        try:
            self.max_thread_count = Configuration.objects.filter(name="6").values_list("count")[0][0]
        except Exception as exception:
            print(exception)
            self.max_thread_count = 10
        self.target_url = PathScanTask.objects.filter(id=task_id).values_list("target")[0][0]
        if self.target_url[-1] == "/":
            self.target_url = self.target_url[0:-1]
        self.payloads = [filename.split("\n")[0] for filename in open(str(BASE_DIR) + "/PathScan/Dictionary/filenames.txt", 'r')]
        if '' in self.payloads:
            self.payloads.remove('')

    def scan(self):
        for payload in self.payloads:
            print(repr(payload))
            url = self.target_url + "/%s" % str(payload)
            response = requests.get(url, verify=False, allow_redirects=False, timeout=5)
            if response.status_code == 200:
                result = {
                    "name": self.name,
                    "url": url
                }
                PathScanResult.objects.create(**result)
        PathScanTask.objects.filter(id=self.task_id).update(state=True)


def start_scan(task_id):
    scanner = FileScanner(task_id)
    scanner.scan()



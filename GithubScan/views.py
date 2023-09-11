import time
import github
from github import Github
from Configuration.models import Configuration
from GithubScan.models import GithubScanTask, GithubScanResult


class GithubScanner(object):
    def __init__(self, name, keyword, domain=None):
        self.name = name
        self.token = Configuration.objects.filter(name="3").values_list("value")[0][0]
        self.scanner = None
        self.results = []
        self.keyword = keyword
        self.domain = domain
        self.word = self.keyword if self.domain is None else '"%s" %s' % (str(keyword), str(domain))

    def login(self):
        try:
            self.scanner = Github(login_or_token=self.token)
        except Exception as exception:
            print(exception)

    def scan(self):
        if self.scanner is None:
            return
        else:
            while True:
                try:
                    self.results = self.scanner.search_code(self.word)
                    break
                except Exception as exception:
                    if exception is github.RateLimitExceededException:
                        print(exception)
                        time.sleep(60)
                        continue
                    else:
                        print(exception)
                        return
            if self.results.totalCount < 0:
                return
            print("start")
            try:
                for result in self.results:
                    _result = {
                        "name": self.name,
                        "keyword": self.keyword,
                        "domain": self.domain,
                        "url": result.html_url,
                    }
                    GithubScanResult.objects.create(**_result)
                    time.sleep(2)
            except Exception as exception:
                print(exception)


def start_scan(task_id):
    task_name = GithubScanTask.objects.filter(id=task_id).values_list("name")[0][0]
    keyword = GithubScanTask.objects.filter(id=task_id).values_list("keyword")[0][0]
    domain = GithubScanTask.objects.filter(id=task_id).values_list("domain")[0][0]
    scanner = GithubScanner(task_name, keyword, domain)
    scanner.login()
    scanner.scan()




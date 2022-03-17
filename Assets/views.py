import re
import json
import nmap
import urllib3
import masscan
import requests
import threading
import dns.resolver
import urllib.parse
import urllib.request
from Assets.models import AssetList, AssetTask
from Configuration.models import Configuration
from Assets.wappalyzer import Wappalyzer, WebPage
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AssetsScanner(object):
    def __init__(self):
        try:
            self.virustotal_token = Configuration.objects.filter(name="1").values_list("value")[0][0]
        except Exception as exception:
            print(exception)
        self.api_url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        self.parameters = {'domain': None, 'apikey': self.virustotal_token}
        self.resolver = dns.resolver
        self.result = {
            "top_level_domain":"",
            "ipaddress": {},
            "subdomains":{}
        }
        self.subdomain_flag = True
        self.cname_flag = True
        self.port_scan_type = "0"
        self.port_list = None
        self.threader = threading
        self.masscan_port_scanner = masscan.PortScanner()
        try:
            self.max_thread_count = Configuration.objects.filter(name="6").values_list("count")[0][0]
        except Exception as exception:
            print(exception)
            self.max_thread_count = 10
        self.max_thread_count = 1
        self.thread_size = 0

    def set_port_scan_type(self, port_scan_type):
        self.port_scan_type = port_scan_type
        if self.port_scan_type == "2":
            self.port_list = "1-65535"
            return
        index = "10"
        if self.port_scan_type == "0":
            index = "10"
        elif self.port_scan_type == "1":
            index = "9"
        else:
            index = "10"
        try:
            self.port_list = Configuration.objects.filter(name=index).values_list("port")[0][0]
        except Exception as exeception:
            self.port_list = "22,23,80,443,445,1433,3306,3389,6379,8080,8443,9200"

    def get_subdomains(self, top_level_domain):
        self.result["top_level_domain"] = top_level_domain
        self.parameters['domain'] = top_level_domain
        try:
            response = urllib.request.urlopen('%s?%s' % (self.api_url, urllib.parse.urlencode(self.parameters))).read()
            subdomain_list = json.loads(response)
            subdomain_list = subdomain_list["subdomains"]
        except Exception as exception:
            print(exception)
            self.result = {
                "top_level_domain": top_level_domain,
                "ipaddress": {},
                "subdomains": {}
            }
            self.subdomain_flag = False
            return
        for subdomain in subdomain_list:
            if subdomain == top_level_domain:
                continue
            self.result["subdomains"][str(subdomain)] = {
                "ipaddress": {},
                "cnames": {}
            }

    def get_cname_record_helper(self, subdomain):
        try:
            cname_list = self.resolver.resolve(subdomain, "CNAME").response.answer
        except Exception as exception:
            print(exception)
            self.thread_size -= 1
            return
        for cname in cname_list:
            if cname.rdtype == 5:
                for item in cname:
                    self.result["subdomains"][subdomain]["cnames"][str(item)] = {}
        self.thread_size -= 1

    def get_cname_record(self):
        if not self.subdomain_flag:
            self.cname_flag = False
            return
        subdomains = self.result["subdomains"].keys()
        subdomains_count = len(subdomains)
        subdomains_index = 0
        for subdomain in subdomains:
            while True:
                if self.thread_size < self.max_thread_count:
                    thread = self.threader.Thread(target=self.get_cname_record_helper, args=(subdomain, ))
                    self.thread_size += 1
                    subdomains_index += 1
                    thread.start()
                    if subdomains_count - subdomains_index <= self.max_thread_count:
                        thread.join()
                    break
                else:
                    continue

    def get_a_record_helper(self, domain):
        _list = []
        try:
            ip_list = self.resolver.resolve(domain, "A").response.answer
        except Exception as exception:
            print(exception)
            return []
        for ip in ip_list:
            if ip.rdtype == 1:
                for item in ip:
                    _list.append(str(item))
        return _list

    def get_a_record_helper_multi_thread(self, position, hostname):
        _list = []
        try:
            ip_list = self.resolver.resolve(hostname, "A").response.answer
        except Exception as exception:
            print(exception)
            self.thread_size -= 1
            return
        for ip in ip_list:
            if ip.rdtype == 1:
                for item in ip:
                    _list.append(str(item))
        for real_ip in _list:
            position[real_ip] = {}
        self.thread_size -= 1

    def get_a_record(self):
        top_level_domain = self.result["top_level_domain"]
        top_level_domain_ip_list = self.get_a_record_helper(top_level_domain)
        for ip in top_level_domain_ip_list:
            self.result["ipaddress"][ip] = {}
        if not self.subdomain_flag:
            return
        subdomains = self.result["subdomains"].keys()
        subdomains_count = len(subdomains)
        subdomains_index = 0
        for subdomain in subdomains:
            while True:
                if self.thread_size < self.max_thread_count:
                    thread = self.threader.Thread(target=self.get_a_record_helper_multi_thread, args=(self.result["subdomains"][subdomain]["ipaddress"], subdomain))
                    self.thread_size += 1
                    thread.start()
                    subdomains_index += 1
                    if subdomains_count - subdomains_index <= self.max_thread_count:
                        thread.join()
                    break
                else:
                    continue
            if not self.cname_flag:
                continue
            cnames = self.result["subdomains"][subdomain]["cnames"].keys()
            cnames_count = len(cnames)
            cnames_index = 0
            for cname in cnames:
                while True:
                    if self.thread_size < self.max_thread_count:
                        thread = self.threader.Thread(target=self.get_a_record_helper_multi_thread,
                                                      args=(self.result["subdomains"][subdomain]["cnames"][cname], subdomain))
                        self.thread_size += 1
                        thread.start()
                        cnames_index += 1
                        if cnames_count - cnames_index <= self.max_thread_count:
                            thread.join()
                        break
                    else:
                        continue

    def assets_data_insert(self, ip, tld, subdomain, cname, port):
        result = {
            "ip_address": ip,
            "top_level_domain": tld,
            "subdomain": subdomain,
            "cname": cname,
            "port": port,
            "state": "1",
            "protocol": "tcp"
        }
        AssetList.objects.create(**result)

    def get_port_helper(self, ip):
        try:
            response = self.masscan_port_scanner.scan(ip, ports=self.port_list, arguments='--max-rate 10000 --wait 3')
            return response["scan"][ip]["tcp"]
        except Exception as execption:
            print(execption)
            return []

    def get_port_by_ip(self):
        for ip in self.result["ipaddress"]:
            port_structs = self.get_port_helper(ip)
            for port in port_structs:
                self.assets_data_insert(ip, self.result["top_level_domain"], "", "", port)
        for subdomain in self.result["subdomains"].keys():
            for ip in self.result["subdomains"][subdomain]["ipaddress"].keys():
                port_structs = self.get_port_helper(ip)
                for port in port_structs:
                    self.assets_data_insert(ip, self.result["top_level_domain"], subdomain, "", port)
        for subdomain in self.result["subdomains"].keys():
            for cname in self.result["subdomains"][subdomain]["cnames"].keys():
                for ip in self.result["subdomains"][subdomain][cname]["ipaddress"].keys():
                    port_structs = self.get_port_helper(ip)
                    for port in port_structs:
                        self.assets_data_insert(ip, self.result["top_level_domain"], subdomain, cname, port)


class PortInformationScanner(object):
    def __init__(self):
        self.requester = requests
        self.port_scanner = nmap.PortScanner()
        self.headers = None

    def port_information_scanner(self, ipaddress, port):
        print(ipaddress)
        print(port)
        try:
            self.port_scanner.scan(hosts=ipaddress, ports=str(port), arguments="-sV", sudo=True)
            service = self.port_scanner[ipaddress]["tcp"][port]["name"]
            product = self.port_scanner[ipaddress]["tcp"][port]["product"]
            version = self.port_scanner[ipaddress]["tcp"][port]["version"]
            return [service, product, version]
        except Exception as exception:
            print(exception)
            return ["", "", ""]

    def service_information_scanner(self, ipaddress, port):
        url = "http://%s:%s" % (ipaddress, str(port))
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            title = re.findall('<title>(.+)</title>', str(response.text))
            if len(title) > 0:
                return title[0]
        except Exception as exception:
            print(exception)
        url = "https://%s:%s" % (ipaddress, str(port))
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=5)
            title = re.findall('<title>(.+)</title>', str(response.text))
            if len(title) > 0:
                return title[0]
        except Exception as exception:
            print(exception)
        return ''

    def middle_ware_information_scanner(self, ipaddress, port):
        middle_scanner = Wappalyzer.latest()
        url = "http://%s:%s" % (str(ipaddress), str(port))
        try:
            webpage = WebPage.new_from_url(url)
        except Exception as exception:
            print(exception)
            return ""
        web_prints = list(middle_scanner.analyze(webpage))
        if len(web_prints) > 0:
            message = ''
            for middle in web_prints:
                message += middle + ', '
            return message[0:-1]
        else:
            return ''


def assets_scan(task_id):
    scanner = AssetsScanner()
    top_level_domain = AssetTask.objects.filter(id=task_id).values_list("top_level_domain")[0][0]
    port_scan_type = AssetTask.objects.filter(id=task_id).values_list("port_scan_type")[0][0]
    scanner.set_port_scan_type(port_scan_type)
    scanner.get_subdomains(top_level_domain)
    scanner.get_cname_record()
    scanner.get_a_record()
    scanner.get_port_by_ip()

def detail(task_id):
    scanner = PortInformationScanner()
    ipaddress = AssetList.objects.filter(id=task_id).values_list("ip_address")[0][0]
    port = AssetList.objects.filter(id=task_id).values_list("port")[0][0]
    service_string, software_string, version_string = scanner.port_information_scanner(ipaddress, port)
    if service_string.find("http") >= 0:
        title_string = scanner.service_information_scanner(ipaddress, port)
        midware_string = scanner.middle_ware_information_scanner(ipaddress, port)
    else:
        title_string = ""
        midware_string = ""

    AssetList.objects.filter(id=task_id).update(
        service=service_string,
        software=software_string,
        version=version_string,
        website_title=title_string,
        middle_ware=midware_string
    )

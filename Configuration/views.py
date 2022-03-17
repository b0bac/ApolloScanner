import struct
import http.server
import socketserver
from Configuration.models import Configuration, Services, ServicesLog


http_server = None
dns_server = None
tcp_server = None


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        message = "%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args)
        _list = message.split(" ")
        url = _list[6]
        if url.find("/") != 0:
            return
        method = _list[5].split('"')[-1]
        status = str(_list[8])
        message = {
            "name": "HTTP日志",
            "ip_address": self.client_address[0],
            'method': method,
            'status': status,
            "message": str(url)
        }
        ServicesLog.objects.create(**message)


def http_server_start(service_id, ip, port):
    global http_server
    server_address = (ip, int(port))
    http_server = http.server.HTTPServer(server_address, HttpHandler)
    Services.objects.filter(id=service_id).update(state=True)
    http_server.serve_forever()


def http_server_stop():
    global http_server
    if http_server is not None:
        http_server.server_close()


class SinDNSQuery:
    def __init__(self, data_array, ipaddress):
        index = 1
        self.ipaddress = ipaddress
        self.name = ''
        while True:
            data = data_array[index]
            if data == 0:
                break
            if data < 32:
                self.name = self.name + '.'
            else:
                self.name = self.name + chr(data)
            index = index + 1
        self.query_bytes = data_array[0:index + 1]
        (self.type, self.classify) = struct.unpack('>HH', data_array[index + 1:index + 5])
        self.length = index + 5

    def get_bytes(self):
        _domain = self.query_bytes + struct.pack('>HH', self.type, self.classify)
        _flag = str(_domain).replace("\\t", "\\x00").replace("\\r", "")
        _flag = str(_flag).split("\\x00\\x00\\x01\\x00\\x01")[0]
        flag = ""
        for item in _flag.split("\\x"):
            flag += item[2:] + "."
        flag = flag[0:-1]
        if flag[0] == ".":
            flag = flag[1:]
        method = "DNS-QUERY"
        status = ""
        message = {
            "name": "DNS日志",
            "ip_address": self.ipaddress,
            'method': method,
            'status': status,
            "message": flag
        }
        ServicesLog.objects.create(**message)
        return message, _domain


class SinDNSAnswer:
    def __init__(self, ip):
        self.name = 49164
        self.type = 1
        self.classify = 1
        self.time_to_live = 190
        self.data_length = 4
        self.ip = ip

    def get_bytes(self):
        response = struct.pack('>HHHLH', self.name, self.type, self.classify, self.time_to_live, self.data_length)
        ip_split_str = self.ip.split('.')
        response = response + struct.pack('BBBB', int(ip_split_str[0]), int(ip_split_str[1]), int(ip_split_str[2]), int(ip_split_str[3]))
        return response


class SinDNSFrame:
    def __init__(self, data, ip):
        self.answer = None
        (self.id, self.flags, self.quests, self.answers, self.author, self.addition) = struct.unpack('>HHHHHH', data[0:12])
        self.query = SinDNSQuery(data[12:], ip)

    def get_name(self):
        return self.query.name

    def set_ip(self, ip):
        self.answer = SinDNSAnswer(ip)
        self.answers = 1
        self.flags = 33152

    def get_bytes(self):
        response = struct.pack('>HHHHHH', self.id, self.flags, self.quests, self.answers, self.author, self.addition)
        response = response + self.query.get_bytes()[1]
        if self.answers != 0:
            response = response + self.answer.get_bytes()
        return response


class SinDNSUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        ip = self.client_address[0]
        dns = SinDNSFrame(data, ip)
        socket = self.request[1]
        name_map = SinDNSServer.name_map
        if(dns.query.type==1):
            name = dns.get_name()
            if name_map.__contains__(name):
                dns.set_ip(name_map[name])
                socket.sendto(dns.get_bytes(), self.client_address)
            elif name_map.__contains__('*'):
                # Response default address
                dns.set_ip(name_map['*'])
                socket.sendto(dns.get_bytes(), self.client_address)
            else:
                # ignore it
                socket.sendto(data, self.client_address)
        else:
            # If this is not query a A record, ignore it
            socket.sendto(data, self.client_address)


class SinDNSServer:
    def __init__(self, port=53):
        SinDNSServer.name_map = {}
        self.port = port
        self.server = None

    def add_name(self, name, ip):
        SinDNSServer.name_map[name] = ip

    def start(self):
        host, port = "0.0.0.0", self.port
        self.server = socketserver.UDPServer((host, port), SinDNSUDPHandler)
        self.server.serve_forever()

    def close(self):
        self.server.server_close()


class SinDNSUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        ip = self.client_address[0]
        dns = SinDNSFrame(data, ip)
        socket = self.request[1]
        name_map = SinDNSServer.name_map
        if(dns.query.type==1):
            name = dns.get_name()
            if name_map.__contains__(name):
                dns.set_ip(name_map[name])
                socket.sendto(dns.get_bytes(), self.client_address)
            elif name_map.__contains__('*'):
                # Response default address
                dns.set_ip(name_map['*'])
                socket.sendto(dns.get_bytes(), self.client_address)
            else:
                # ignore it
                socket.sendto(data, self.client_address)
        else:
            # If this is not query a A record, ignore it
            socket.sendto(data, self.client_address)


def dns_server_start(service_id, ipaddress, port=53):
    global dns_server
    dns_server = SinDNSServer(port)
    domain = Configuration.objects.filter(name="8").values_list("domain")[0][0]
    dns_server.add_name(str(domain), ipaddress)
    dns_server.add_name('*', '0.0.0.0')
    Services.objects.filter(id=service_id).update(state=True)
    dns_server.start()


def dns_server_stop():
    global dns_server
    dns_server.close()


def service_start(service_id):
    name = Services.objects.filter(id=service_id).values_list("name")[0][0]
    port = Services.objects.filter(id=service_id).values_list("port")[0][0]
    ipaddress = Services.objects.filter(id=service_id).values_list("ip_address")[0][0]
    if name == "1":
        http_server_start(service_id, ipaddress, port)
    elif name == "2":
        dns_server_start(service_id, ipaddress, port)


def service_stop(service_id):
    name = Services.objects.filter(id=service_id).values_list("name")[0][0]
    if name == "1":
        try:
            http_server_stop()
        except Exception as exception:
            print(exception)
            pass
    elif name == "2":
        try:
            dns_server_stop()
        except Exception as exception:
            print(exception)
            pass
    Services.objects.filter(id=service_id).update(state=False)

import http.server
from Configuration.models import Services, ServicesLog


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
        print(message)
        ServicesLog.objects.create(**message)


def http_server_start(service_id, ip, port):
    global http_server
    server_address = (ip, int(port))
    http_server = http.server.HTTPServer(server_address, HttpHandler)
    Services.objects.filter(name=service_id).update(state=True)
    http_server.serve_forever()


def http_server_stop():
    global http_server
    if http_server is not None:
        http_server.server_close()


def service_start(service_id):
    port = Services.objects.filter(name=service_id).values_list("port")[0][0]
    ipaddress = Services.objects.filter(name=service_id).values_list("ip_address")[0][0]
    http_server_start(service_id, ipaddress, port)


def service_stop(service_id):
    http_server_stop()
    Services.objects.filter(name=service_id).update(state=False)

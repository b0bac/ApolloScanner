import socket


def redis_unauth_scan(address, port):
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.settimeout(5)
    try:
        sender.connect((address, int(port)))
    except Exception as exception:
        print(exception)
        return False
    try:
        sender.send(b"INFO\r\n")
        receive_data = sender.recv(1024)
        if b"redis_version" in receive_data:
            return True
    except Exception as exception:
        print(exception)
        return False



# Декораторы
def time_benchmark(function):
    """Декоратор для подсчета времени работы"""

    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        print("[*]Время выполнения функции {0} сек".format(end_time - start_time))
        return result
    return inner


def function_time_control(timeout=float):
    """Декоратор для контроля максимального времени выполнения"""

    def shutdown(function_name, timeout):
        print("Функция {1} выполняется дольше {0} сек".format(timeout, function_name))
        thread.interrupt_main()

    def outer(function):
        def inner(*args, **kwargs):
            timer = threading.Timer(timeout, function=shutdown, args=[function.__name__, timeout])
            timer.start()
            try:
                result = function(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

# Классы для чтения и записи данных в контроллер
import socket
import snap7


class S7Connection:

    def __init__(self, ip, rack, slot):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.connection = None

    def connect(self):
        self.connection = snap7.client.Client()
        self.connection.connect(self.ip, self.rack, self.slot)
        return self.connection.get_connected()

    def read(self, db_number, start_addr, size):
        return self.connection.db_read(db_number, start_addr, size)

    def write(self, db_number, start_addr, size, data=bytearray):
        self.connection.db_write(db_number, start_addr, size, data)

    def get_state(self):
        return self.connection.get_cpu_state()


class TcpConnection:

    def __init__(self, ip, port):
        self.address = None
        self.connection = None
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPIDLE, 1)     # время бездействия, сек
        self.sock.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPINTVL, 3)    # интервал ping-запросов, сек
        self.sock.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPCNT, 5)      # количество ошибок ping-запросов
        self.sock.settimeout(600)
        self.sock.bind((ip, port))

    def connect(self):
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()
        return self.address

    def send(self, data):
        self.connection.sendall(data)

    def receive(self, data_len):
        return self.connection.recv(data_len)

    def disconnect(self):
        self.connection.shutdown(1)
        self.connection.close()
        
        
#Генератор паролей

import random
import argparse


ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
SPECIAL = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

password_chars = ''
password = ''

parser = argparse.ArgumentParser(description='Password generator')
parser.add_argument('pass_len', help='Password len', type=int)
parser.add_argument('-u', '--uppercase', help='Use uppercase characters', action='store_true')
parser.add_argument('-l', '--lowercase', help='Use lowercase characters', action='store_true')
parser.add_argument('-d', '--digits', help='Use digits', action='store_true')
parser.add_argument('-s', '--special', help='Use special characters', action='store_true')
args = parser.parse_args()

if not args.uppercase and not args.lowercase and not args.digits and not args.special:
    password_chars += ASCII_LOWERCASE + ASCII_UPPERCASE + DIGITS + SPECIAL
else:
    if args.uppercase:
        password_chars += ASCII_UPPERCASE
    if args.lowercase:
        password_chars += ASCII_LOWERCASE
    if args.digits:
        password_chars += DIGITS
    if args.special:
        password_chars += SPECIAL

for i in range(args.pass_len):
    password += random.choice(password_chars)
print(password)

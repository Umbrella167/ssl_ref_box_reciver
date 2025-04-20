import socket
import struct
import threading

class UDPReceiver:
    def __init__(self, port, *, bind_ip='', multicast=False, multicast_group=None, callback=None, plugin=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind((bind_ip, port))
        if multicast:
            mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        if callback:
            self.callback = callback if not plugin else lambda x: callback((plugin.decode(x[0]),x[1]))
            self.stop_token = threading.Event()
            self.recvThread = threading.Thread(target=self.__recv)
            self.recvThread.daemon = True
            self.recvThread.start()

    def recv(self):
        try:
            return True, self.sock.recvfrom(65536)
        except socket.error as e:
            return False, None
    
    def __recv(self):
        while True:
            res, recv = self.recv()
            if self.stop_token.is_set():
                break
            if res:
                self.callback(recv)
    def stop(self):
        self.stop_token.set()
        self.recvThread.join()

    def setblocking(self, blocking):
        self.sock.setblocking(blocking)

class UDPMultiCastReceiver(UDPReceiver):
    def __init__(self, group, port, *, bind_ip='', callback=None, plugin=None):
        super().__init__(port, multicast=True, multicast_group=group, bind_ip=bind_ip, callback=callback, plugin=plugin)

class UDPSender:
    def __init__(self, *, multicast=False, ttl=2, multicast_interface=None, plugin=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if multicast:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            if multicast_interface:
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(multicast_interface))
        self.plugin = plugin
    
    def send(self, msg, ep):
        if self.plugin:
            msg = self.plugin.encode(msg)
        self.sock.sendto(msg, ep)

class UDPMultiCastSender(UDPSender):
    def __init__(self, *, ttl=2, multicast_interface=None, plugin=None):
        super().__init__(multicast=True, ttl=ttl, multicast_interface=multicast_interface, plugin=plugin)
    def setInterface(self, ip):
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip))

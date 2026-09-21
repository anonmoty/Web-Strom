import os
import random
import socket
import urllib.request
from core.colors import *
from core.animations import Animation

class ProxyManager:
    def __init__(self, proxy_file=None):
        self.proxies = []
        self.proxy_file = proxy_file or "proxies/socksku.txt"
        
        # Agar user ne custom proxy file nahi di, toh auto-fetch karega online API se
        if not proxy_file:
            self.fetch_online_proxies()
        else:
            self.load_local_proxies(proxy_file)

    def fetch_online_proxies(self):
        """
        Aapka diya hua code: ProxyScrape API se fresh aur popular SOCKS4 proxies
        download karke save aur load karta hai.
        """
        # Ensure directories exist
        os.makedirs("proxies", exist_ok=True)
        
        print(f"\n  {lightning('Fetching fresh, popular SOCKS4 proxies from server...')}")
        Animation.loading("Connecting to ProxyScrape API", 1.5)
        
        api_url = (
            "https://api.proxyscrape.com/v2/"
            "?request=displayproxies"
            "&protocol=socks4"
            "&timeout=10000"
            "&country=all"
            "&ssl=all"
            "&anonymity=all"
        )
        
        try:
            # Native urllib use kiya hai taaki Termux mein 'requests' module ka dependancy error na aaye
            req = urllib.request.Request(
                api_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                proxylist = response.read().decode('utf-8')
            
            # File mein save karna 'socksku.txt'
            with open(self.proxy_file, 'w') as f:
                f.write(proxylist)
                
            self.proxies = [line.strip() for line in proxylist.splitlines() if line.strip()]
            print(f"  {success(f'Successfully loaded {len(self.proxies)} live SOCKS4 proxies!')}")
            
        except Exception as e:
            print(f"  {error('Failed to fetch online proxies, using offline backup if available.')}")
            # Fallback: Agar internet slow ho toh purani saved file load karega
            self.load_local_proxies(self.proxy_file)

    def load_local_proxies(self, filepath):
        """Purani saved file se proxy load karne ke liye"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                print(f"  {success(f'Loaded {len(self.proxies)} proxies from {filepath}')}")
            except Exception as e:
                print(f"  {error(f'Error reading local proxy file: {e}')}")
        else:
            print(f"  {warning('No offline proxy file found.')}")

    def get_random(self):
        """Random proxy select karne ke liye"""
        return random.choice(self.proxies) if self.proxies else None

    def count(self):
        """Total proxies count"""
        return len(self.proxies)

    def test_all(self):
        """Proxies check karne ke liye"""
        working = 0
        test_list = self.proxies[:15]  # Pehli 15 proxy fast test karega
        
        print(f"  {info('Testing connection speed of top 15 proxies...')}")
        for proxy in test_list:
            try:
                host, port = proxy.split(':')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((host, int(port)))
                s.close()
                working += 1
            except:
                pass
        return working

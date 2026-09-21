import socket
import ssl
import time
import urllib.request
from urllib.parse import urlparse
from core.colors import *
from core.useragent import UserAgent
from core.animations import Animation

class TargetAnalyzer:
    def __init__(self, url):
        self.url = url
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.is_ssl = parsed.scheme == 'https'
    
    def resolve_ip(self):
        try: return socket.gethostbyname(self.host)
        except: return None
    
    def check_port(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            result = s.connect_ex((self.host, self.port))
            s.close()
            return result == 0
        except: return False
    
    def http_info(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': UserAgent.random_agent()})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            start = time.time()
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            return {
                'status': resp.status,
                'server': resp.headers.get('Server', 'Unknown'),
                'powered': resp.headers.get('X-Powered-By', 'Unknown'),
                'latency': round((time.time() - start) * 1000, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def quick_check(self):
        print(f"\n  {info('Quick target verification...')}")
        Animation.loading("Resolving DNS", 1)
        ip = self.resolve_ip()
        if not ip:
            print(f"  {error('DNS resolution failed')}")
            return False
        print(f"  {success(f'IP: {ip}')}")
        
        Animation.loading("Checking port", 1)
        if not self.check_port():
            print(f"  {error(f'Port {self.port} closed')}")
            return False
        print(f"  {success(f'Port {self.port} open')}")
        return True
    
    def deep_scan(self):
        """Complete deep analysis"""
        print(f"\n  {CYAN}━━━ Deep Target Analysis ━━━{RESET}\n")
        
        Animation.loading("Analyzing target", 2)
        
        ip = self.resolve_ip()
        info_data = self.http_info()
        
        print(f"""
    {CYAN}╔══════════════════════════════════════════════════╗
    ║              TARGET INTELLIGENCE                 ║
    ╠══════════════════════════════════════════════════╣{RESET}
    {CYAN}║{RESET}  {YELLOW}🎯 Target      :{RESET} {WHITE}{self.url}{RESET}
    {CYAN}║{RESET}  {YELLOW}🌐 IP Address  :{RESET} {WHITE}{ip or 'N/A'}{RESET}
    {CYAN}║{RESET}  {YELLOW}🔌 Port        :{RESET} {WHITE}{self.port}{RESET}
    {CYAN}║{RESET}  {YELLOW}🔐 Protocol    :{RESET} {WHITE}{'HTTPS' if self.is_ssl else 'HTTP'}{RESET}
    {CYAN}║{RESET}  {YELLOW}📡 Status      :{RESET} {GREEN}{info_data.get('status', 'N/A')}{RESET}
    {CYAN}║{RESET}  {YELLOW}🖥  Server      :{RESET} {WHITE}{info_data.get('server', 'N/A')}{RESET}
    {CYAN}║{RESET}  {YELLOW}⚙️  Powered By  :{RESET} {WHITE}{info_data.get('powered', 'N/A')}{RESET}
    {CYAN}║{RESET}  {YELLOW}⏱  Latency     :{RESET} {WHITE}{info_data.get('latency', 'N/A')} ms{RESET}
    {CYAN}╚══════════════════════════════════════════════════╝{RESET}
        """)

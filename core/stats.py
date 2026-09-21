import time
import sys
import threading
from core.colors import *

class Statistics:
    def __init__(self):
        self.total_requests = 0
        self.successful = 0
        self.failed = 0
        self.total_bytes = 0
        self.start_time = None
        self.end_time = None
        self.lock = threading.Lock()
    
    def start(self): self.start_time = time.time()
    def stop(self): self.end_time = time.time()
    
    def increment_sent(self):
        with self.lock:
            self.total_requests += 1
            self.successful += 1
    
    def increment_failed(self):
        with self.lock:
            self.failed += 1
    
    def add_bytes(self, size):
        with self.lock:
            self.total_bytes += size
    
    def get_elapsed(self):
        if not self.start_time: return 0
        return (self.end_time or time.time()) - self.start_time
    
    def print_live(self):
        elapsed = self.get_elapsed()
        rps = self.total_requests / elapsed if elapsed > 0 else 0
        mb = self.total_bytes / (1024 * 1024)
        
        status = (
            f"\r  {RED}💥{RESET} "
            f"{CYAN}HITS:{RESET} {BOLD}{GREEN}{self.total_requests:,}{RESET} "
            f"{CYAN}| FAIL:{RESET} {RED}{self.failed:,}{RESET} "
            f"{CYAN}| RPS:{RESET} {YELLOW}{rps:.1f}{RESET} "
            f"{CYAN}| TIME:{RESET} {WHITE}{elapsed:.1f}s{RESET} "
            f"{CYAN}| DATA:{RESET} {PURPLE}{mb:.2f}MB{RESET}    "
        )
        sys.stdout.write(status)
        sys.stdout.flush()
    
    def print_final(self):
        elapsed = self.get_elapsed()
        rps = self.total_requests / elapsed if elapsed > 0 else 0
        mb = self.total_bytes / (1024 * 1024)
        success_rate = (self.successful / self.total_requests * 100) if self.total_requests > 0 else 0
        
        print(f"""
    {CYAN}╔══════════════════════════════════════════════════╗
    ║           💥 ATTACK FINAL REPORT 💥              ║
    ╠══════════════════════════════════════════════════╣{RESET}
    {CYAN}║{RESET}  {YELLOW}⏱  Duration     :{RESET} {WHITE}{elapsed:.2f} seconds{RESET}
    {CYAN}║{RESET}  {YELLOW}📊 Total Hits   :{RESET} {WHITE}{self.total_requests:,}{RESET}
    {CYAN}║{RESET}  {YELLOW}✓ Successful   :{RESET} {GREEN}{self.successful:,}{RESET}
    {CYAN}║{RESET}  {YELLOW}✗ Failed       :{RESET} {RED}{self.failed:,}{RESET}
    {CYAN}║{RESET}  {YELLOW}📈 Success Rate :{RESET} {GREEN}{success_rate:.2f}%{RESET}
    {CYAN}║{RESET}  {YELLOW}⚡ Requests/sec :{RESET} {YELLOW}{rps:.2f} rps{RESET}
    {CYAN}║{RESET}  {YELLOW}💾 Data Sent    :{RESET} {PURPLE}{mb:.2f} MB{RESET}
    {CYAN}║{RESET}  {YELLOW}📡 Bandwidth    :{RESET} {PURPLE}{mb/elapsed if elapsed > 0 else 0:.2f} MB/s{RESET}
    {CYAN}╚══════════════════════════════════════════════════╝{RESET}
        """)

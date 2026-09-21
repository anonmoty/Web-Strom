import threading
import time
from core.colors import *

class SystemMonitor:
    """
    Monitor system resources natively on Termux/Linux without psutil.
    Reads system stats directly from /proc directory.
    """
    
    def __init__(self):
        self.running = False
        self.cpu_usage = []
        self.mem_usage = []
        self.net_sent = []
        self.net_recv = []
        self.thread = None
        
        # CPU tracking variables
        self.prev_idle = 0
        self.prev_total = 0
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _get_cpu_usage(self):
        """Read CPU usage from /proc/stat"""
        try:
            with open('/proc/stat', 'r') as f:
                first_line = f.readline()
            
            if first_line.startswith('cpu '):
                parts = [float(x) for x in first_line.split()[1:]]
                # idle time is at index 3, iowait is at index 4
                idle = parts[3] + parts[4]
                total = sum(parts)
                
                diff_idle = idle - self.prev_idle
                diff_total = total - self.prev_total
                
                self.prev_idle = idle
                self.prev_total = total
                
                if diff_total == 0:
                    return 0.0
                
                return (1.0 - (diff_idle / diff_total)) * 100.0
        except:
            pass
        return 0.0

    def _get_mem_usage(self):
        """Read RAM usage from /proc/meminfo"""
        try:
            meminfo = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        meminfo[parts[0].rstrip(':')] = float(parts[1])
            
            total = meminfo.get('MemTotal', 0)
            # Available memory fallback for older kernels
            available = meminfo.get('MemAvailable', 0)
            if available == 0:
                available = meminfo.get('MemFree', 0) + meminfo.get('Buffers', 0) + meminfo.get('Cached', 0)
            
            if total > 0:
                used = total - available
                return (used / total) * 100.0
        except:
            pass
        return 0.0

    def _get_net_bytes(self):
        """Read Network TX/RX bytes from /proc/net/dev"""
        try:
            sent = 0
            recv = 0
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
            
            # Skip first 2 lines (headers)
            for line in lines[2:]:
                parts = line.split()
                if len(parts) >= 10:
                    # Rx bytes is index 1, Tx bytes is index 9
                    recv += int(parts[1])
                    sent += int(parts[9])
            return sent, recv
        except:
            pass
        return 0, 0

    def _monitor(self):
        prev_sent = 0
        prev_recv = 0
        
        # Initialize net bytes
        initial_sent, initial_recv = self._get_net_bytes()
        prev_sent = initial_sent
        prev_recv = initial_recv
        
        while self.running:
            try:
                # Get CPU
                cpu = self._get_cpu_usage()
                self.cpu_usage.append(cpu)
                
                # Get RAM
                mem = self._get_mem_usage()
                self.mem_usage.append(mem)
                
                # Get Network Speed
                curr_sent, curr_recv = self._get_net_bytes()
                if prev_sent > 0:
                    self.net_sent.append(max(0, curr_sent - prev_sent))
                    self.net_recv.append(max(0, curr_recv - prev_recv))
                
                prev_sent = curr_sent
                prev_recv = curr_recv
                
                # Keep last 100 entries only
                if len(self.cpu_usage) > 100:
                    self.cpu_usage.pop(0)
                    self.mem_usage.pop(0)
                if len(self.net_sent) > 100:
                    self.net_sent.pop(0)
                    self.net_recv.pop(0)
                    
            except Exception:
                pass
            
            time.sleep(1)
    
    def get_stats(self):
        return {
            'cpu_avg': sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0.0,
            'cpu_max': max(self.cpu_usage) if self.cpu_usage else 0.0,
            'mem_avg': sum(self.mem_usage) / len(self.mem_usage) if self.mem_usage else 0.0,
            'net_sent_total': sum(self.net_sent),
            'net_recv_total': sum(self.net_recv)
        }
    
    def print_stats(self):
        stats = self.get_stats()
        # Fallback values if OS blocks access to /proc files (SELinux)
        cpu_display = f"{stats['cpu_avg']:.1f}%" if stats['cpu_avg'] > 0 else "N/A"
        cpu_peak = f"{stats['cpu_max']:.1f}%" if stats['cpu_max'] > 0 else "N/A"
        mem_display = f"{stats['mem_avg']:.1f}%" if stats['mem_avg'] > 0 else "N/A"
        
        print(f"""
    {CYAN}╔══════════════════════════════════════════════════╗
    ║           SYSTEM RESOURCE USAGE                  ║
    ╠══════════════════════════════════════════════════╣{RESET}
    {CYAN}║{RESET}  {YELLOW}CPU Average    :{RESET} {WHITE}{cpu_display}{RESET}
    {CYAN}║{RESET}  {YELLOW}CPU Peak       :{RESET} {RED}{cpu_peak}{RESET}
    {CYAN}║{RESET}  {YELLOW}Memory Average :{RESET} {WHITE}{mem_display}{RESET}
    {CYAN}║{RESET}  {YELLOW}Data Sent      :{RESET} {GREEN}{stats['net_sent_total']/(1024*1024):.2f} MB{RESET}
    {CYAN}║{RESET}  {YELLOW}Data Received  :{RESET} {GREEN}{stats['net_recv_total']/(1024*1024):.2f} MB{RESET}
    {CYAN}╚══════════════════════════════════════════════════╝{RESET}
        """)

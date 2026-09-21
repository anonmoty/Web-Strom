import sys

# Basic colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BLACK = '\033[30m'

# Effects
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'
STRIKE = '\033[9m'
RESET = '\033[0m'

# Background
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_PURPLE = '\033[45m'
BG_CYAN = '\033[46m'

# Bright colors
B_RED = '\033[1;91m'
B_GREEN = '\033[1;92m'
B_YELLOW = '\033[1;93m'
B_BLUE = '\033[1;94m'
B_PURPLE = '\033[1;95m'
B_CYAN = '\033[1;96m'

# Status messages
def success(msg): return f"{GREEN}[✓]{RESET} {msg}"
def error(msg): return f"{RED}[✗]{RESET} {msg}"
def info(msg): return f"{CYAN}[ℹ]{RESET} {msg}"
def warning(msg): return f"{YELLOW}[⚠]{RESET} {msg}"
def fire(msg): return f"{RED}[🔥]{RESET} {msg}"
def target(msg): return f"{PURPLE}[🎯]{RESET} {msg}"
def bomb(msg): return f"{RED}[💣]{RESET} {msg}"
def lightning(msg): return f"{YELLOW}[⚡]{RESET} {msg}"
def skull(msg): return f"{RED}[💀]{RESET} {msg}"

def gradient(text, colors=[91, 93, 92, 96, 94, 95]):
    """Print text with gradient colors"""
    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += f"\033[{color}m{char}"
    return result + RESET

def rainbow(text):
    """Rainbow effect"""
    return gradient(text)

def status_color(code):
    code = int(code)
    if 200 <= code < 300: return GREEN
    if 300 <= code < 400: return BLUE
    if code == 403: return YELLOW
    if code >= 500: return RED
    return WHITE

import sys
import time
import random
import threading
from core.colors import *

class Animation:
    @staticmethod
    def loading(text, duration=3):
        """Spinner loading animation"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f'\r  {CYAN}{frames[i % len(frames)]}{RESET} {text}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write(f'\r  {GREEN}✓{RESET} {text} {GREEN}[COMPLETE]{RESET}    \n')
    
    @staticmethod
    def typewriter(text, delay=0.03, color=CYAN):
        """Typewriter effect"""
        for char in text:
            sys.stdout.write(f'{color}{char}{RESET}')
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def matrix_effect(duration=3):
        """Matrix falling code effect"""
        chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ'
        end_time = time.time() + duration
        while time.time() < end_time:
            line = ""
            for _ in range(60):
                if random.random() < 0.5:
                    line += f"{GREEN}{random.choice(chars)}{RESET}"
                else:
                    line += " "
            print(f"  {line}")
            time.sleep(0.05)
    
    @staticmethod
    def progress_bar(current, total, prefix="", suffix="", length=40):
        """Progress bar"""
        if total == 0: return
        percent = 100 * (current / total)
        filled = int(length * current // total)
        bar = f"{GREEN}█{RESET}" * filled + f"{DIM}░{RESET}" * (length - filled)
        sys.stdout.write(f'\r  {prefix} [{bar}] {percent:.1f}% {suffix}')
        sys.stdout.flush()
    
    @staticmethod
    def countdown(seconds, message="Starting in"):
        """Countdown timer"""
        for i in range(seconds, 0, -1):
            sys.stdout.write(f'\r  {YELLOW}⏱  {message} {RED}{i}{YELLOW} seconds...{RESET}   ')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f'\r  {GREEN}🚀 LAUNCHING NOW!{RESET}                          \n')
    
    @staticmethod
    def firing_animation():
        """Attack firing animation"""
        stages = [
            f"{RED}          .          ",
            f"{RED}         .·.         ",
            f"{RED}        .·:·.        ",
            f"{RED}       .·:•:·.       ",
            f"{RED}      .·:•*•:·.      ",
            f"{YELLOW}     .·:•*■*•:·.     ",
            f"{YELLOW}    .·:•*■■■*•:·.    ",
            f"{RED}   .·:•*■💀■*•:·.   ",
            f"{RED}  .·:•*■💀💀■*•:·.  ",
        ]
        for stage in stages:
            sys.stdout.write(f'\r  {stage}{RESET}')
            sys.stdout.flush()
            time.sleep(0.15)
        print(f"\n  {RED}💥 {BOLD}ATTACK LAUNCHED!{RESET}\n")
    
    @staticmethod
    def glitch_text(text, iterations=5):
        """Glitchy text effect"""
        chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        for _ in range(iterations):
            glitched = ""
            for char in text:
                if random.random() < 0.3:
                    glitched += f"{RED}{random.choice(chars)}{RESET}"
                else:
                    glitched += f"{WHITE}{char}{RESET}"
            sys.stdout.write(f'\r  {glitched}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r  {CYAN}{text}{RESET}\n')
    
    @staticmethod
    def pulse(text, times=3, color=RED):
        """Pulsing text effect"""
        for _ in range(times):
            sys.stdout.write(f'\r  {DIM}{text}{RESET}')
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write(f'\r  {BOLD}{color}{text}{RESET}')
            sys.stdout.flush()
            time.sleep(0.3)
        print()

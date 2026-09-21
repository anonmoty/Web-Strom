import os

def create_dirs():
    for d in ['output/logs', 'output/reports', 'proxies']:
        os.makedirs(d, exist_ok=True)

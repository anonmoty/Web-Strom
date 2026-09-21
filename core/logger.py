import os
import logging
from datetime import datetime

class Logger:
    _init = False
    
    @staticmethod
    def setup():
        if Logger._init: return
        os.makedirs("output/logs", exist_ok=True)
        f = f"output/logs/webstorm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                          handlers=[logging.FileHandler(f, encoding='utf-8')])
        Logger._init = True
    
    @staticmethod
    def info(msg): Logger.setup(); logging.info(msg)
    @staticmethod
    def error(msg): Logger.setup(); logging.error(msg)
    @staticmethod
    def warning(msg): Logger.setup(); logging.warning(msg)

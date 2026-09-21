import random
import os

class UserAgent:
    """Random User-Agent generator for evading detection"""
    
    # Comprehensive user-agent list
    AGENTS = [
        # Chrome - Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        
        # Chrome - Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        
        # Chrome - Linux
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        
        # Opera
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
        
        # Mobile - Android
        'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        
        # Mobile - iOS
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        
        # Bots (for variety)
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        
        # Old browsers (for randomization)
        'Mozilla/5.0 (compatible; MSIE 11.0; Windows NT 10.0; WOW64; Trident/7.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        
        # Console/Game devices
        'Mozilla/5.0 (PlayStation 5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.2.20.4 NintendoBrowser/5.1.0.22023',
        
        # Smart TVs
        'Mozilla/5.0 (SMART-TV; LINUX; Tizen 6.0) AppleWebKit/537.36 (KHTML, like Gecko) 85.0.4183.93/6.0 TV Safari/537.36',
        
        # Older mobile
        'Mozilla/5.0 (Linux; U; Android 8.0.0; en-us; SM-G950U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    ]
    
    REFERERS = [
        'https://www.google.com/',
        'https://www.google.com/search?q=',
        'https://www.bing.com/',
        'https://www.yahoo.com/',
        'https://duckduckgo.com/',
        'https://www.facebook.com/',
        'https://twitter.com/',
        'https://www.reddit.com/',
        'https://www.youtube.com/',
        'https://www.instagram.com/',
        'https://www.linkedin.com/',
        'https://www.pinterest.com/',
        'https://www.tumblr.com/',
        'https://news.ycombinator.com/',
        'https://www.wikipedia.org/',
        'https://github.com/',
        'https://stackoverflow.com/',
        'https://www.amazon.com/',
        'https://www.ebay.com/',
        'https://www.netflix.com/',
        'https://www.baidu.com/',
        'https://www.yandex.com/',
        'https://www.quora.com/',
        'https://medium.com/',
        'https://www.twitch.tv/',
    ]
    
    ACCEPT_LANGUAGES = [
        'en-US,en;q=0.9',
        'en-GB,en;q=0.9',
        'en-US,en;q=0.8,es;q=0.6',
        'de-DE,de;q=0.9,en;q=0.8',
        'fr-FR,fr;q=0.9,en;q=0.8',
        'es-ES,es;q=0.9,en;q=0.8',
        'it-IT,it;q=0.9,en;q=0.8',
        'ja-JP,ja;q=0.9,en;q=0.8',
        'zh-CN,zh;q=0.9,en;q=0.8',
        'ru-RU,ru;q=0.9,en;q=0.8',
        'pt-BR,pt;q=0.9,en;q=0.8',
        'ar-SA,ar;q=0.9,en;q=0.8',
        'hi-IN,hi;q=0.9,en;q=0.8',
        'ko-KR,ko;q=0.9,en;q=0.8',
        'nl-NL,nl;q=0.9,en;q=0.8',
    ]
    
    CACHE_CONTROLS = [
        'no-cache',
        'max-age=0',
        'no-store, no-cache',
        'must-revalidate, no-cache',
        'no-cache, no-store, must-revalidate',
        'max-age=0, must-revalidate',
        'private, no-cache',
    ]
    
    ACCEPT_ENCODINGS = [
        'gzip, deflate',
        'gzip, deflate, br',
        'gzip',
        'identity',
        'compress, gzip',
        'deflate, gzip',
    ]
    
    ACCEPT_CHARSETS = [
        'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'utf-8, iso-8859-1;q=0.5, *;q=0.1',
        'ISO-8859-1',
        'utf-8;q=0.7,*;q=0.3',
        'windows-1251,utf-8;q=0.7,*;q=0.7',
    ]
    
    ACCEPT_TYPES = [
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'application/json, text/plain, */*',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        '*/*',
    ]
    
    @staticmethod
    def load_from_file(filepath):
        """Load custom user agents from file"""
        if not os.path.exists(filepath):
            return UserAgent.AGENTS
        try:
            with open(filepath, 'r') as f:
                agents = [line.strip() for line in f if line.strip()]
            return agents if agents else UserAgent.AGENTS
        except:
            return UserAgent.AGENTS
    
    @staticmethod
    def random_agent(agents=None):
        return random.choice(agents or UserAgent.AGENTS)
    
    @staticmethod
    def random_referer(referers=None):
        base = random.choice(referers or UserAgent.REFERERS)
        # Sometimes add search query
        if random.random() > 0.5 and 'search' in base:
            terms = ['news', 'weather', 'tutorial', 'download', 'video',
                     'music', 'game', 'movie', 'app', 'shop']
            base += random.choice(terms)
        return base
    
    @staticmethod
    def random_language():
        return random.choice(UserAgent.ACCEPT_LANGUAGES)
    
    @staticmethod
    def random_cache():
        return random.choice(UserAgent.CACHE_CONTROLS)
    
    @staticmethod
    def random_encoding():
        return random.choice(UserAgent.ACCEPT_ENCODINGS)
    
    @staticmethod
    def random_charset():
        return random.choice(UserAgent.ACCEPT_CHARSETS)
    
    @staticmethod
    def random_accept():
        return random.choice(UserAgent.ACCEPT_TYPES)

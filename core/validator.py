from urllib.parse import urlparse

class Validator:
    @staticmethod
    def validate_url(url):
        if not url: return False, "Empty URL"
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        try:
            parsed = urlparse(url)
            if all([parsed.scheme, parsed.netloc]):
                return True, url
            return False, "Invalid URL"
        except:
            return False, "Parse error"

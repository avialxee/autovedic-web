from urllib.parse import urlparse, urljoin
from flask import request

class URLSafe:
    def __init__(self, target) -> None:
        self.target = target
        
    def is_safe_url(self):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, self.target))
        return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc

def is_url_safe(target):
    url_instance = URLSafe(target)
    return url_instance.is_safe_url()
import re

class Utils:
    @staticmethod
    def get_blog_name_from_url(url):
        match = re.search(r'blog.naver.com/([^/]+)', url)
        return match.group(1) if match else "unknown"

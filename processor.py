import re
from bs4 import BeautifulSoup

class Processor:
    @staticmethod
    def extract_image_urls(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                images.append(src)
        return images

    @staticmethod
    def process_image_urls(images):
        processed_images = [
            img for img in images if img.startswith("https://mblogthumb-phinf.pstatic.net/")
        ]
        processed_images = [
            re.sub(r'https?://[^/]+', 'https://blogfiles.pstatic.net', img) for img in processed_images
        ]
        processed_images = [re.sub(r'\?.*$', '', img) for img in processed_images]
        return processed_images

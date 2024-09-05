import os
import requests

class Downloader:
    @staticmethod
    def save_images(images, save_path, blog_name):
        if not images or not save_path:
            return 0

        successful_downloads = 0
        for i, img_url in enumerate(images):
            base_filename = f"{blog_name}_{i}.jpg"
            filename = base_filename
            file_path = os.path.join(save_path, filename)
            counter = 1

            while os.path.exists(file_path):
                filename = f"{blog_name}_{i}({counter}).jpg"
                file_path = os.path.join(save_path, filename)
                counter += 1

            try:
                img_data = requests.get(img_url).content
                with open(file_path, 'wb') as img_file:
                    img_file.write(img_data)
                successful_downloads += 1
            except Exception:
                continue

        return successful_downloads

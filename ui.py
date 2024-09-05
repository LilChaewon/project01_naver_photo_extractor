import tkinter as tk
from tkinter import filedialog, messagebox
from fetcher import Fetcher
from processor import Processor
from downloader import Downloader
from utils import Utils
import config

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("네이버 블로그 원본 사진 추출기")
        self.root.geometry("500x450")

        self.create_widgets()

    def create_widgets(self):
        url_label = tk.Label(self.root, text="네이버 블로그 URL들:")
        url_label.pack()

        self.url_entry = tk.Text(self.root, height=10, width=50)
        self.url_entry.pack()

        save_path_label = tk.Label(self.root, text="저장 경로:")
        save_path_label.pack()

        self.save_path_entry = tk.Entry(self.root, width=50)
        self.save_path_entry.pack()
        self.save_path_entry.insert(0, config.DEFAULT_SAVE_PATH)  # 기본 저장 경로 설정

        save_path_button = tk.Button(self.root, text="경로 선택", command=self.select_save_path)
        save_path_button.pack()

        submit_button = tk.Button(self.root, text="추출 시작", command=self.check_urls)
        submit_button.pack()

        self.status_label = tk.Label(self.root, text="상태: 대기 중")
        self.status_label.pack()

    def select_save_path(self):
        folder_selected = filedialog.askdirectory()
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, folder_selected)

    def check_urls(self):
        text = self.url_entry.get("1.0", tk.END)
        urls = text.strip().split('\n')
        failed_urls = []
        processed_count = 0

        for url in urls:
            if url:
                blog_name = Utils.get_blog_name_from_url(url)
                if not any(domain in url for domain in config.SUPPORTED_DOMAINS):
                    failed_urls.append(url)
                    continue

                html_content = Fetcher.get_html(url)
                if not html_content:
                    failed_urls.append(url)
                    continue

                images = Processor.extract_image_urls(html_content)
                processed_images = Processor.process_image_urls(images)
                if len(images) < 1 or Downloader.save_images(processed_images, self.save_path_entry.get(), blog_name) == 0:
                    failed_urls.append(url)
                    continue

                processed_count += 1
                self.status_label.config(text=f"처리 중... {processed_count}/{len(urls)} 완료")

        self.status_label.config(text="처리 완료!")
        if failed_urls:
            messagebox.showinfo("완료", f"작업 완료! 실패한 URL: {len(failed_urls)}\n" + "\n".join(failed_urls))
        else:
            messagebox.showinfo("완료", "모든 URL이 성공적으로 처리되었습니다.")

    def run(self):
        self.root.mainloop()

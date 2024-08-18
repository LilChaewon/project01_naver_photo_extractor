import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import re
import os

def select_save_path():
    folder_selected = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, folder_selected)

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            images.append(src)
    return images

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 200 OK 코드가 아니면 예외 발생
        return response.text
    except requests.RequestException as e:
        return None

def get_blog_name_from_url(url):
    match = re.search(r'blog.naver.com/([^/]+)', url)
    return match.group(1) if match else "unknown"

def download_and_save_images(images, save_path, blog_name):
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

def process_and_show_images(images, blog_name):
    save_path = save_path_entry.get()
    processed_images = [img for img in images if img.startswith("https://mblogthumb-phinf.pstatic.net/")]
    processed_images = [re.sub(r'https?://[^/]+', 'https://blogfiles.pstatic.net', img) for img in processed_images]
    processed_images = [re.sub(r'\?.*$', '', img) for img in processed_images]

    if processed_images:
        return download_and_save_images(processed_images, save_path, blog_name)
    else:
        return 0

def check_urls():
    text = url_entry.get("1.0", tk.END)
    urls = text.strip().split('\n')
    failed_urls = []
    processed_count = 0
    for url in urls:
        if url:
            blog_name = get_blog_name_from_url(url)
            if "blog.naver.com" not in url:
                failed_urls.append(url)
                continue
            html_content = fetch_html(url)
            if not html_content:
                failed_urls.append(url)
                continue
            images = extract_images(html_content)
            if len(images) < 1 or process_and_show_images(images, blog_name) == 0:
                failed_urls.append(url)
                continue
            processed_count += 1
            status_label.config(text=f"처리 중... {processed_count}/{len(urls)} 완료")

    status_label.config(text="처리 완료!")
    if failed_urls:
        messagebox.showinfo("완료", f"작업 완료! 실패한 URL: {len(failed_urls)}\n" + "\n".join(failed_urls))
    else:
        messagebox.showinfo("완료", "모든 URL이 성공적으로 처리되었습니다.")

root = tk.Tk()
root.title("네이버 블로그 원본 사진 추출기")
root.geometry("500x450")

url_label = tk.Label(root, text="네이버 블로그 URL들:")
url_label.pack()

url_entry = tk.Text(root, height=10, width=50)
url_entry.pack()

save_path_label = tk.Label(root, text="저장 경로:")
save_path_label.pack()

save_path_entry = tk.Entry(root, width=50)
save_path_entry.pack()

save_path_button = tk.Button(root, text="경로 선택", command=select_save_path)
save_path_button.pack()

submit_button = tk.Button(root, text="추출 시작", command=check_urls)
submit_button.pack()

status_label = tk.Label(root, text="상태: 대기 중")
status_label.pack()

root.mainloop()
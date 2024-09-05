import requests
from tkinter import messagebox

class Fetcher:
    @staticmethod
    def get_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            messagebox.showerror("오류", f"웹페이지를 가져오지 못했습니다: {e}")
            return None

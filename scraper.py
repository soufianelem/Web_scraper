import requests
from bs4 import BeautifulSoup
from plyer import notification
import time
import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event

def check_new_posts(url, log_text):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    posts = soup.find_all('article')

    if posts:
        notification.notify(
            title='New Post Detected',
            message=f'Found {len(posts)} new posts on {url}!',
            timeout=10
        )
        log_text.insert(tk.END, f"Found {len(posts)} new posts on {url}.\n")
    else:
        log_text.insert(tk.END, f"No new posts found on {url}.\n")

def start_monitoring(urls, interval, log_text, stop_event):
    urls = urls.split(',')
    urls = [url.strip() for url in urls]
    
    while not stop_event.is_set():
        for url in urls:
            check_new_posts(url, log_text)
        log_text.insert(tk.END, f"Waiting for {interval} minutes...\n")
        time.sleep(interval * 60)  # Convert minutes to seconds

def on_start_button_click():
    urls = url_entry.get()
    interval = int(interval_entry.get())
    if urls:
        log_text.insert(tk.END, f"Started monitoring: {urls}\n")
        stop_event.clear()
        monitor_thread = Thread(target=start_monitoring, args=(urls, interval, log_text, stop_event))
        monitor_thread.start()
    else:
        messagebox.showwarning("Input Error", "Please enter at least one URL.")

def on_stop_button_click():
    stop_event.set()
    log_text.insert(tk.END, "Monitoring stopped.\n")

# Set up the GUI
root = tk.Tk()
root.title("Post Monitor")

tk.Label(root, text="Enter URLs (comma-separated):").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

tk.Label(root, text="Check Interval (minutes):").pack(pady=10)
interval_entry = tk.Entry(root, width=10)
interval_entry.pack(pady=5)
interval_entry.insert(0, "5")

start_button = tk.Button(root, text="Start Monitoring", command=on_start_button_click)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Monitoring", command=on_stop_button_click)
stop_button.pack(pady=5)

log_text = tk.Text(root, height=10, width=60)
log_text.pack(pady=10)

# Use threading.Event to signal stopping
stop_event = Event()

root.mainloop()

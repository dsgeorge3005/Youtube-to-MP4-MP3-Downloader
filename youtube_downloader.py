import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import re
import sys

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Use bundled binaries
FFMPEG_PATH = os.path.join(BASE_PATH, "ffmpeg")
YT_DLP_PATH = os.path.join(BASE_PATH, "yt-dlp")

print(f"BASE_PATH: {BASE_PATH}")
print(f"FFMPEG_PATH: {FFMPEG_PATH}")
print(f"YT_DLP_PATH: {YT_DLP_PATH}")

def check_ffmpeg():
    exists = os.path.exists(FFMPEG_PATH)
    print(f"Checking FFmpeg: exists={exists}")
    return exists

def check_yt_dlp():
    exists = os.path.exists(YT_DLP_PATH)
    print(f"Checking yt-dlp: exists={exists}")
    return exists

def get_video_title(url):
    print(f"Getting title for URL: {url}")
    try:
        result = subprocess.run(
            [YT_DLP_PATH, "--get-title", url],
            check=True, text=True, capture_output=True
        )
        print(f"yt-dlp output: {result.stdout}")
        invalid_chars = '<>:"/\\|?*'
        title = result.stdout.strip()
        for char in invalid_chars:
            title = title.replace(char, "-")
        return title or "downloaded_video"
    except subprocess.CalledProcessError as e:
        print(f"Title fetch failed: {e.stderr}")
        return "downloaded_video"

def download_and_convert(url, format_choice, output_folder, status_text, stop_flag, download_btn, progress_bar, canvas, percent_text):
    video_title = get_video_title(url)
    output_file = os.path.join(output_folder, f"{video_title}")
    print(f"Output file: {output_file}")
    try:
        cmd = [
            YT_DLP_PATH, "--newline", "--no-check-certificate",
            "-o", f"{output_file}.%(ext)s", url
        ]
        if format_choice == "mp4":
            cmd.extend([
                "-f", "bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best",
                "--merge-output-format", "mp4",
                "--recode-video", "mp4",
                "--ffmpeg-location", FFMPEG_PATH
            ])
        elif format_choice == "mp3":
            cmd.extend([
                "-f", "bestaudio",
                "--extract-audio",
                "--audio-format", "mp3",
                "--no-playlist",
                "--ffmpeg-location", FFMPEG_PATH
            ])
        print(f"Running command: {' '.join(cmd)}")

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1)
        percent_pattern = re.compile(r"\[download\]\s+(\d+\.\d+)%")
        for line in process.stdout:
            print(f"yt-dlp output: {line.strip()}")
            status_text.config(state=tk.NORMAL)
            status_text.insert(tk.END, line)
            status_text.config(state=tk.DISABLED)
            match = percent_pattern.search(line)
            if match:
                percent = float(match.group(1))
                canvas_width = 400
                bar_width = (percent / 100) * canvas_width
                canvas.coords(progress_bar, 0, 0, bar_width, 20)
                canvas.itemconfig(percent_text, text=f"{percent:.1f}%")
                text_x = min(max(bar_width / 2, 20), canvas_width - 20)
                canvas.coords(percent_text, text_x, 10)
                status_text.config(state=tk.NORMAL)
                status_text.delete("1.0", tk.END)
                status_text.insert(tk.END, f"Downloading: {percent:.1f}%\n")
                status_text.config(state=tk.DISABLED)
            canvas.update()

        process.wait()
        if process.returncode == 0:
            stop_flag[0] = True
            canvas.coords(progress_bar, 0, 0, 400, 20)
            canvas.itemconfig(percent_text, text="100%")
            canvas.coords(percent_text, 200, 10)
            status_text.config(state=tk.NORMAL)
            status_text.delete("1.0", tk.END)
            status_text.insert(tk.END, f"Saved as {output_file}.{format_choice}\n")
            status_text.config(state=tk.DISABLED)
        else:
            raise subprocess.CalledProcessError(process.returncode, cmd)
    except subprocess.CalledProcessError as e:
        stop_flag[0] = True
        status_text.config(state=tk.NORMAL)
        status_text.insert(tk.END, f"Error: Return code {e.returncode}\n")
        status_text.config(state=tk.DISABLED)
    except Exception as e:
        stop_flag[0] = True
        status_text.config(state=tk.NORMAL)
        status_text.insert(tk.END, f"Failed: {str(e)}\n")
        status_text.config(state=tk.DISABLED)
    finally:
        download_btn.config(state=tk.NORMAL)

def choose_folder(folder_label, root):
    folder = filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), title="Choose Download Folder")
    if folder:
        folder_label.config(text=f"Destination: {folder}")
        root.output_folder = folder

def start_download(url_entry, format_var, status_text, download_btn, root, canvas, progress_bar, percent_text):
    url = url_entry.get().strip()
    format_choice = format_var.get().lower()
    output_folder = getattr(root, "output_folder", os.path.expanduser("~/Downloads"))
    if not url or url == "Paste link here":
        status_text.config(state=tk.NORMAL)
        status_text.delete("1.0", tk.END)
        status_text.insert(tk.END, "Please enter a valid YouTube URL.\n")
        status_text.config(state=tk.DISABLED)
        return
    if format_choice not in ["mp3", "mp4"]:
        status_text.config(state=tk.NORMAL)
        status_text.delete("1.0", tk.END)
        status_text.insert(tk.END, "Please select MP3 or MP4.\n")
        status_text.config(state=tk.DISABLED)
        return
    download_btn.config(state=tk.DISABLED)
    canvas.itemconfig(percent_text, text="0%")
    canvas.coords(progress_bar, 0, 0, 0, 20)
    stop_flag = [False]
    Thread(target=download_and_convert, args=(url, format_choice, output_folder, status_text, stop_flag, download_btn, progress_bar, canvas, percent_text), daemon=True).start()

def create_ui():
    print("Checking FFmpeg before UI")
    if not check_ffmpeg():
        root = tk.Tk()
        root.title("YouTube Downloader")
        root.geometry("400x150")
        tk.Label(root, text="FFmpeg Not Found", font=("Helvetica", 14, "bold"), fg="red").pack(pady=20)
        tk.Label(root, text="FFmpeg is missing from the app bundle.", font=("Helvetica", 12)).pack(pady=5)
        root.mainloop()
        return
    if not check_yt_dlp():
        root = tk.Tk()
        root.title("YouTube Downloader")
        root.geometry("400x150")
        tk.Label(root, text="yt-dlp Not Found", font=("Helvetica", 14, "bold"), fg="red").pack(pady=20)
        tk.Label(root, text="yt-dlp is missing from the app bundle.", font=("Helvetica", 12)).pack(pady=5)
        root.mainloop()
        return
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("500x420")
    root.resizable(False, False)
    root.configure(bg="#f0f0f0")
    root.output_folder = os.path.expanduser("~/Downloads")
    tk.Label(root, text="YouTube Downloader", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(root, text="YouTube URL", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=(0, 5))
    url_entry = tk.Entry(root, width=40, font=("Helvetica", 12), justify="center", bd=2, relief="flat")
    url_entry.pack(pady=5)
    url_entry.insert(0, "Paste link here")
    tk.Label(root, text="Format", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=(10, 5))
    format_var = tk.StringVar(value="MP4")
    format_menu = tk.OptionMenu(root, format_var, "MP4", "MP3")
    format_menu.config(font=("Helvetica", 12), bg="white", activebackground="#e0e0e0", bd=2, relief="flat")
    format_menu.pack(pady=5)
    tk.Label(root, text="Destination", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=(10, 5))
    folder_label = tk.Label(root, text=f"Destination: {root.output_folder}", font=("Helvetica", 11), bg="#f0f0f0")
    folder_label.pack(pady=2)
    choose_btn = tk.Button(root, text="Choose Folder", command=lambda: choose_folder(folder_label, root),
                          font=("Helvetica", 10), bg="#d0d0d0", activebackground="#c0c0c0", bd=0, padx=10, pady=5)
    choose_btn.pack(pady=5)
    download_btn = tk.Button(root, text="Download", command=lambda: start_download(url_entry, format_var, status_text, download_btn, root, canvas, progress_bar, percent_text),
                            font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", bd=0, padx=10, pady=5)
    download_btn.pack(pady=20)
    canvas = tk.Canvas(root, width=400, height=20, bg="#e0e0e0", highlightthickness=0)
    canvas.pack(pady=5)
    progress_bar = canvas.create_rectangle(0, 0, 0, 20, fill="#4CAF50")
    percent_text = canvas.create_text(20, 10, text="0%", font=("Helvetica", 10, "bold"), fill="white")
    status_text = tk.Text(root, height=6, width=50, font=("Helvetica", 11), state=tk.DISABLED, bd=1, relief="solid")
    status_text.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    create_ui()

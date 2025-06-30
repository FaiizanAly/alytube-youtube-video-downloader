import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp

available_formats = []
selected_url = ""
video_title = ""
is_playlist = False

def fetch_formats():
    global available_formats, selected_url, video_title, is_playlist
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    selected_url = url
    quality_combo.set("")
    quality_combo["values"] = []
    format_radio_audio.deselect()
    format_radio_video.select()

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_color': True}) as ydl:
            info = ydl.extract_info(url, download=False)

            if 'entries' in info:
                is_playlist = True
                first_video = list(info['entries'])[0]
                video_title = f"Playlist: {info.get('title', 'Untitled')}"
                formats = first_video['formats']
            else:
                is_playlist = False
                video_title = info.get("title", "Untitled")
                formats = info['formats']

            video_options = []
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    label = f"{f['format_id']} - {f.get('height', '')}p - {f.get('ext', '')}"
                    video_options.append((label, f['format_id']))

            available_formats = video_options
            if not video_options:
                raise Exception("No video formats found.")

            quality_combo['values'] = [opt[0] for opt in video_options]
            quality_combo.current(0)
            download_button.config(state='normal')
            status_label.config(text=f"✔ Found formats for: {video_title}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch formats:\n{e}")

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def start_download():
    threading.Thread(target=download).start()

def download():
    try:
        folder = folder_entry.get() or '.'
        os.makedirs(folder, exist_ok=True)

        fmt = format_type.get()
        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'no_color': True  # ✅ Disable colored output
        }

        if fmt == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            selected_index = quality_combo.current()
            format_id = available_formats[selected_index][1]
            ydl_opts.update({'format': format_id})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([selected_url])

        status_label.config(text="✅ Download complete!")
        progress_var.set(0)
        messagebox.showinfo("Success", "Download completed.")
    except Exception as e:
        status_label.config(text="❌ Error during download.")
        messagebox.showerror("Error", f"Download failed:\n{e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0.0%').strip()
        percent = ''.join(c for c in percent_str if c.isdigit() or c == '.')
        try:
            progress_var.set(float(percent))
        except ValueError:
            progress_var.set(0)
        status_label.config(text=f"Downloading: {percent_str}")
    elif d['status'] == 'finished':
        status_label.config(text="Processing...")

# GUI Layout
root = tk.Tk()
root.title("YouTube Downloader by Faizan")
root.geometry("600x400")
root.resizable(False, False)

tk.Label(root, text="YouTube URL (Video or Playlist):").pack(pady=5)
url_entry = tk.Entry(root, width=70)
url_entry.pack()

tk.Button(root, text="Fetch Qualities", command=fetch_formats).pack(pady=8)

format_frame = tk.Frame(root)
format_frame.pack()
format_type = tk.StringVar(value="video")
format_radio_video = tk.Radiobutton(format_frame, text="Video (MP4)", variable=format_type, value="video")
format_radio_audio = tk.Radiobutton(format_frame, text="Audio (MP3)", variable=format_type, value="mp3")
format_radio_video.pack(side=tk.LEFT, padx=10)
format_radio_audio.pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Available Qualities:").pack()
quality_combo = ttk.Combobox(root, width=60, state="readonly")
quality_combo.pack(pady=5)

tk.Label(root, text="Save To Folder:").pack()
folder_frame = tk.Frame(root)
folder_frame.pack()
folder_entry = tk.Entry(folder_frame, width=45)
folder_entry.pack(side=tk.LEFT, padx=5)
tk.Button(folder_frame, text="Browse", command=choose_folder).pack(side=tk.LEFT)

download_button = tk.Button(root, text="Download", state='disabled', command=start_download)
download_button.pack(pady=15)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate', variable=progress_var)
progress_bar.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

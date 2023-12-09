import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from moviepy.editor import VideoFileClip
import os
import threading
from moviepy.video.fx.all import resize


def split_video(video_path, output_dir, progress_bar, cancel_button):
    def update_progress(current_part, total_parts):
        progress = (current_part / total_parts) * 100
        progress_bar['value'] = progress

    def split():
        nonlocal is_cancelled
        is_cancelled = False
        if not os.path.exists(video_path):
            result_label.config(text="File not found.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        clip = VideoFileClip(video_path)
        duration = clip.duration

        if duration <= 60:
            result_label.config(text="Video is already 1 minute or less.")
            if duration <= 60:  # Check if the video is <= 1 minute
                clip = resize(clip, newsize=(clip.h, clip.w))  # Rotate to vertical
                clip.write_videofile(os.path.join(output_dir, "vertical_video.mp4"), codec="libx264")
                result_label.config(text="Video converted to vertical.")
            return

        num_parts = int(duration // 60) + 1

        for i in range(num_parts):
            if is_cancelled:
                result_label.config(text="Splitting canceled.")
                break

            start_time = i * 60
            end_time = min((i + 1) * 60, duration)
            part = clip.subclip(start_time, end_time)

            if end_time - start_time <= 60:  # Check if part duration <= 1 minute
                part = resize(part, newsize=(part.h, part.w))  # Rotate to vertical

            part.write_videofile(
                os.path.join(output_dir, f"part_{i + 1}.mp4"),
                codec="libx264",  # Video codec
                audio_codec="aac",  # Audio codec
                temp_audiofile=f"temp_audio_{i}.m4a",  # Temporary audio file
                remove_temp=True,  # Remove temporary audio file after writing video
                threads=4  # Number of threads for processing
            )

            update_progress(i + 1, num_parts)
            root.after(10, update_progress, i + 1, num_parts)

        clip.close()
        if not is_cancelled:
            result_label.config(text=f"Video split into {num_parts} parts. Check the output directory.")
        cancel_button.config(state=tk.DISABLED)

    is_cancelled = True
    threading.Thread(target=split).start()


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


def browse_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, output_dir)


def cancel_split():
    global is_cancelled
    is_cancelled = True
    result_label.config(text="Splitting canceled.")
    cancel_button.config(state=tk.DISABLED)


def split_video_gui():
    global is_cancelled
    video_path = file_entry.get()
    output_directory = directory_entry.get()

    is_cancelled = False
    cancel_button.config(state=tk.NORMAL)
    progress_bar['value'] = 0
    result_label.config(text="")

    split_video(video_path, output_directory, progress_bar, cancel_button)


# Initialize and set up the GUI
root = tk.Tk()
root.title("Video Splitter")
root.geometry("520x400")
root.configure(bg="#f3f4f6")  # Background color

main_frame = tk.Frame(root, padx=20, pady=10, bg="#ffffff")
main_frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(main_frame, text="Video Splitter", font=('Arial', 20, 'bold'), bg="#ffffff")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

file_label = tk.Label(main_frame, text="Select Video File:", font=('Arial', 12), bg="#ffffff")
file_label.grid(row=1, column=0, sticky='w', padx=10)

file_entry = tk.Entry(main_frame, width=30, font=('Arial', 12))
file_entry.grid(row=1, column=1, padx=10)

file_button = tk.Button(main_frame, text="Browse", command=browse_file, font=('Arial', 12), bg="#b8c1ec", fg="#ffffff", relief=tk.FLAT)
file_button.grid(row=1, column=2, padx=10)

directory_label = tk.Label(main_frame, text="Select Output Directory:", font=('Arial', 12), bg="#ffffff")
directory_label.grid(row=2, column=0, sticky='w', padx=10)

directory_entry = tk.Entry(main_frame, width=30, font=('Arial', 12))
directory_entry.grid(row=2, column=1, padx=10)

directory_button = tk.Button(main_frame, text="Browse", command=browse_directory, font=('Arial', 12), bg="#b8c1ec", fg="#ffffff", relief=tk.FLAT)
directory_button.grid(row=2, column=2, padx=10)

split_button = tk.Button(main_frame, text="Split Video", command=split_video_gui, font=('Arial', 12), bg="#2ecc71", fg="#ffffff", relief=tk.FLAT)
split_button.grid(row=3, column=1, pady=15)

progress_label = tk.Label(main_frame, text="Progress:", font=('Arial', 12), bg="#ffffff")
progress_label.grid(row=4, column=0, sticky='w', padx=10)

progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, column=1, columnspan=2, pady=5)

cancel_button = tk.Button(main_frame, text="Cancel", command=cancel_split, state=tk.DISABLED, font=('Arial', 12), bg="#ff4757", fg="#ffffff", relief=tk.FLAT)
cancel_button.grid(row=5, column=1, pady=10)

result_label = tk.Label(main_frame, text="", font=('Arial', 12), bg="#ffffff")
result_label.grid(row=6, column=0, columnspan=3, pady=10)

is_cancelled = False  # Initializing the cancel flag

root.mainloop()

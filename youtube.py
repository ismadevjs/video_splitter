import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import threading
from PIL import Image, ImageTk

def download_video():
    video_url = url_entry.get()
    output_path = path_var.get()

    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        download_thread = threading.Thread(target=start_download, args=(stream, output_path))
        download_thread.start()
    except Exception as e:
        display_error(str(e))

def start_download(stream, output_path):
    try:
        stream.download(output_path)
        print("Download completed successfully!")
    except Exception as e:
        display_error(str(e))

def on_progress(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    bytes_downloaded = file_size - bytes_remaining
    percentage = int((bytes_downloaded / file_size) * 100)
    update_progress(percentage)

def update_progress(progress_value):
    progress_bar['value'] = progress_value

def browse_output_path():
    path = filedialog.askdirectory()
    path_var.set(path)

def display_error(message):
    error_label.config(text=message, fg="red")

# GUI setup
root = tk.Tk()
root.title("Toolspace YouTube Downloader")

# Load the PNG image
png_image = Image.open('C:\\Users\\ismai\\OneDrive\\Documents\\toolspace\\900ppi\\ico.png')  # Replace 'path_to_image.png' with your PNG file
png_image = png_image.resize((32, 32))  # Resize the image if needed for the icon

# Convert the PNG image to an ICO image
ico_image = ImageTk.PhotoImage(png_image)
root.iconphoto(True, ico_image)


# Load the logo image
logo_image = Image.open('C:\\Users\\ismai\\OneDrive\\Documents\\toolspace\\900ppi\\done png.png')  # Replace 'path_to_logo.png' with your logo file
logo_image = logo_image.resize((350, 150))  # Adjust the size of the logo if needed
logo_img = ImageTk.PhotoImage(logo_image)

# Display the logo above the input fields
logo_label = tk.Label(root, image=logo_img)
logo_label.pack()

style = ttk.Style()
style.theme_use('clam')

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill=tk.BOTH)

url_label = ttk.Label(main_frame, text="Enter YouTube URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

url_entry = ttk.Entry(main_frame, width=40)
url_entry.grid(row=0, column=1, padx=5, pady=5)

path_label = ttk.Label(main_frame, text="Select Output Path:")
path_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

path_var = tk.StringVar()
path_entry = ttk.Entry(main_frame, width=30, textvariable=path_var, state='readonly')
path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_button = ttk.Button(main_frame, text="Browse", command=browse_output_path)
browse_button.grid(row=1, column=2, padx=5, pady=5)

download_button = ttk.Button(main_frame, text="Download", command=download_video)
download_button.grid(row=2, column=1, padx=5, pady=15)

progress_bar = ttk.Progressbar(main_frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=3, columnspan=3, padx=5, pady=5)

error_label = ttk.Label(main_frame, text="", foreground="red")
error_label.grid(row=4, columnspan=3, padx=5, pady=5)

root.mainloop()

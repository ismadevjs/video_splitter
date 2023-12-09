from moviepy.editor import VideoFileClip
import os

def split_video(video_path, output_dir):
    if not os.path.exists(video_path):
        print("File not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clip = VideoFileClip(video_path)
    duration = clip.duration

    if duration <= 60:
        print("Video is already 1 minute or less.")
        return

    num_parts = int(duration // 60) + 1

    for i in range(num_parts):
        start_time = i * 60
        end_time = min((i + 1) * 60, duration)
        part = clip.subclip(start_time, end_time)
        part.write_videofile(os.path.join(output_dir, f"part_{i + 1}.mp4"))

    clip.close()
    print(f"Video split into {num_parts} parts of 1-minute duration each.")

if __name__ == "__main__":
    video_path = input("Enter the video file path: ").strip()
    output_directory = input("Enter the output directory for split videos (leave blank for current directory): ").strip()
    if output_directory == "":
        output_directory = os.getcwd()

    split_video(video_path, output_directory)

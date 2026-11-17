import subprocess
import os

def split_webm_ffmpeg_encoded(input_path, split_minutes=30):
    base_filename, _ = os.path.splitext(os.path.basename(input_path))
    output_dir = f"{base_filename}_split"
    os.makedirs(output_dir, exist_ok=True)

    output_pattern = os.path.join(output_dir, f"{base_filename}_part%03d.webm")

    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libvpx',             # VP8 or use libvpx-vp9 for VP9
        '-c:a', 'libvorbis',          # libopus도 가능
        '-map', '0',
        '-f', 'segment',
        '-segment_time', str(split_minutes * 60),
        '-reset_timestamps', '1',
        output_pattern
    ]

    subprocess.run(cmd)

# 예시 실행
split_webm_ffmpeg_encoded("/home/gpuadmin/Downloads/Screencast from 2025년 04월 29일 13시 16분 53초.webm", split_minutes=30)

import os
import subprocess

def merge_videos(root_dir_saving = None, output_file_name = 'merged_output.mp4'):
    folders = [f for f in os.listdir(root_dir_saving) if os.path.isdir(os.path.join(root_dir_saving, f))]
    for folder in folders:
        folder_path = os.path.join(root_dir_saving, folder)
        mp4_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp4')]
        if not mp4_files:
            continue

        mp4_files.sort()
        list_file = os.path.join(folder_path, 'files.txt')
        with open(list_file, 'w') as f:
            for file in mp4_files:
                abs_path = os.path.abspath(file)
                f.write(f"file '{abs_path}'\n")


        output_file = os.path.join(folder_path, output_file_name)
        subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file, '-c', 'copy', output_file])
        os.remove(list_file)
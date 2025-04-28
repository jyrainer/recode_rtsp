import os
import time
from datetime import datetime

import cv2

from recode_rtsp.utils.trans_str import sanitize_folder_name


def record_stream(stream_url, info, running_flag, max_duration):
    video_postfix = info["postfix"]
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print(f"Failed to open stream: {stream_url}")
        return

    folder_name = sanitize_folder_name(stream_url)
    save_folder = os.path.join(info["root_dir_saving"], folder_name)
    os.makedirs(save_folder, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 1 or fps != fps:  # 0 or NaN
        fps = 15.0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = None
    frame_count = 0
    segment_frame_count = 0

    try:
        print(f"[INFO] Starting recording for {stream_url}")
        while running_flag:
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to read frame from: {stream_url}")
                break

            frame_count += 1
            segment_frame_count += 1

            elapsed_video_time = frame_count / fps
            segment_elapsed_time = segment_frame_count / fps

            if max_duration is not None and elapsed_video_time >= max_duration:
                print(
                    f"[INFO] Max duration {max_duration} seconds reached based on frame count. Stopping recording."
                )
                break

            current_time = time.time()

            if out is None or segment_elapsed_time >= info["recode_period"]:
                if out is not None:
                    out.release()
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + f".{video_postfix}"
                filepath = os.path.join(save_folder, filename)
                out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
                segment_frame_count = 0

            if out:
                out.write(frame)

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, saving file...")

    finally:
        if out:
            out.release()
        cap.release()
        print(f"Recording stopped and saved for {stream_url}")

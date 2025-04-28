import os
import threading
import time
from datetime import datetime
from queue import Queue

import cv2

from recode_rtsp.utils.capture_threading import frame_capture_thread
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

    # Declare Queue
    frame_queue = Queue(maxsize=300)
    capture_running = threading.Event()
    capture_running.set()

    # Start capture thread
    capture_thread = threading.Thread(
        target=frame_capture_thread, args=(cap, frame_queue, capture_running)
    )
    capture_thread.start()

    try:
        print(f"[INFO] Starting recording for {stream_url}")
        while running_flag:
            try:
                frame = frame_queue.get(timeout=1)  # 1초 이내 못 받으면 timeout
            except:
                print("[WARNING] Frame queue empty. Waiting for frames...")
                continue

            frame_count += 1
            segment_frame_count += 1

            elapsed_video_time = frame_count / fps
            segment_elapsed_time = segment_frame_count / fps

            if max_duration is not None and elapsed_video_time >= max_duration:
                print(f"[INFO] Max duration {max_duration} seconds reached. Stopping recording.")
                break

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

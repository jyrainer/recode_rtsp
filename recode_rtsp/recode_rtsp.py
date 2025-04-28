import os
import cv2
import threading
import time
from datetime import datetime

class RecodeRtsp:
    def __init__(self, rtsp_stream, root_dir_saving, recode_period=300, postfix='mp4'):
        if isinstance(rtsp_stream, str):
            rtsp_stream = [rtsp_stream]
        self.rtsp_streams = rtsp_stream
        self.root_dir_saving = root_dir_saving
        self.recode_period = recode_period
        self.postfix = postfix
        self.threads = []
        self.running = True

        if not os.path.exists(self.root_dir_saving):
            os.makedirs(self.root_dir_saving)

    @classmethod
    def new(cls, rtsp_stream, root_dir_saving, recode_period=300, postfix='mp4'):
        instance = cls(rtsp_stream, root_dir_saving, recode_period, postfix)
        instance.start_recording()
        return instance

    def start_recording(self):
        for stream in self.rtsp_streams:
            t = threading.Thread(target=self.record_stream, args=(stream,))
            t.start()
            self.threads.append(t)

    def record_stream(self, stream_url):
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print(f"Failed to open stream: {stream_url}")
            return

        folder_name = self.sanitize_folder_name(stream_url)
        save_folder = os.path.join(self.root_dir_saving, folder_name)
        os.makedirs(save_folder, exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0 or fps != fps:  # NaN check
            fps = 25.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = None
        start_time = time.time()

        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print(f"Failed to read frame from: {stream_url}")
                    break

                current_time = time.time()
                if out is None or (current_time - start_time) >= self.recode_period:
                    if out is not None:
                        out.release()
                    filename = datetime.now().strftime('%Y%m%d_%H%M%S') + f'.{self.postfix}'
                    filepath = os.path.join(save_folder, filename)
                    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
                    start_time = current_time

                if out:
                    out.write(frame)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected, saving file...")
        finally:
            if out:
                out.release()
            cap.release()
            print(f"Recording stopped and saved for {stream_url}")

    def sanitize_folder_name(self, stream_url):
        return stream_url.replace(':', '_').replace('/', '_').replace('.', '_')

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()

# Example usage:
if __name__ == "__main__":
    rtsp_streams = [
        'rtsp://172.168.47.35:8555/A_walljump',
        'rtsp://172.168.47.35:8555/B_walljump',
        'rtsp://172.168.47.35:8555/C_walljump'
    ]
    recorder = RecodeRtsp.new(rtsp_stream=rtsp_streams, root_dir_saving="./assets", recode_period=10, postfix='mp4')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all recordings...")
        recorder.stop()

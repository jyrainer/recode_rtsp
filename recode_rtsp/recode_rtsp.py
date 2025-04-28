import os
import threading
import time
import subprocess

from recode_rtsp.utils.file_io import save_yaml, load_yaml
from recode_rtsp.utils.recode import record_stream
from recode_rtsp.utils.manage_videos import merge_vidoes

class RecodeRtsp:
    """RecodeRtsp class for recording RTSP streams and managing video files."""

    DEFAULT_INFO_DICT = {
        'rtsp_streams': None,
        'recode_period': None,
        'postfix': None,
        'root_dir_saving': None
    }
    YAML_FILE = 'info.yaml'

    def __init__(self, root_dir_saving, rtsp_stream = None):
        if isinstance(rtsp_stream, str):
            rtsp_stream = [rtsp_stream]
        self.rtsp_streams = rtsp_stream
        self.root_dir_saving = root_dir_saving

        self.threads = []
        self.running = True

        if not os.path.exists(self.root_dir_saving):
            os.makedirs(self.root_dir_saving)

    @classmethod
    def new(cls, root_dir_saving, rtsp_stream = None):
        instance = cls(root_dir_saving, rtsp_stream)
        return instance

    @classmethod
    def load(cls, root_dir_saving):
        file_path = os.path.join(root_dir_saving, cls.YAML_FILE)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        info = load_yaml(file_path)
        instance = cls(
            root_dir_saving=info.get('root_dir_saving', './assets'),
        )

        instance.rtsp_stream = info.get('rtsp_streams', [])
        instance.recode_period = info.get('recode_period', 300)
        instance.postfix = info.get('postfix', 'mp4')

        return instance

    def recode(self, rtsp_streams, recode_period=300, postfix='mp4', max_duration=None, merge = False):
        self.rtsp_streams = rtsp_streams
        self.recode_period = recode_period
        self.postfix = postfix
        self.max_duration = max_duration
        
        info = {
            'rtsp_streams': self.rtsp_streams,
            'recode_period': self.recode_period,
            'postfix': self.postfix,
            'root_dir_saving': self.root_dir_saving
        }
        info_path = os.path.join(self.root_dir_saving, 'info.yaml')
        save_yaml(info, info_path)

        for stream in self.rtsp_streams:
            t = threading.Thread(target=record_stream, args=(stream, info, self.running, max_duration))
            t.start()
            time.sleep(1)
            self.threads.append(t)

        while any(t.is_alive() for t in self.threads):
            time.sleep(1)
        self.running = False
        print(f"[INFO] All threads have finished.")

        if not self.running and merge:
            print(f"[INFO] Merging videos in {self.root_dir_saving}")
            self.merge()


    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()

    def merge(self):
        merge_vidoes(self.root_dir_saving)
        print(f"[INFO] Merging completed.")
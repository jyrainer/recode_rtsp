from recode_rtsp.recode_rtsp import RecodeRtsp

rtsp_streams = [
    'rtsp://172.168.47.35:8555/minite_timer',
    'rtsp://172.168.47.35:8555/tailgate_134'
]
recorder = RecodeRtsp.new(root_dir_saving="./assets/TEST_250428")
recorder.recode(rtsp_streams=rtsp_streams, recode_period=4, postfix='mp4', max_duration=14, merge=True)

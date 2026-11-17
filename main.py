from recode_rtsp.recode_rtsp import RecodeRtsp
 
rtsp_streams = [
    'rtsp://172.168.47.35:8555/A_walljump',
    'rtsp://172.168.47.35:8555/B_walljump',
    'rtsp://172.168.47.35:8555/C_walljump',
    'rtsp://172.168.47.35:8555/D_walljump',
    'rtsp://172.168.47.35:8555/D1_walljump',
    'rtsp://172.168.47.35:8555/E_walljump',
    'rtsp://172.168.47.35:8555/F_walljump',
    'rtsp://172.168.47.35:8555/G_walljump',
    'rtsp://172.168.47.35:8555/A_tailgate',
    'rtsp://172.168.47.35:8555/B_tailgate',
    'rtsp://172.168.47.35:8555/C_tailgate',
    'rtsp://172.168.47.35:8555/D_tailgate',
    'rtsp://172.168.47.35:8555/D1_tailgate',
    'rtsp://172.168.47.35:8555/E_tailgate',
    'rtsp://172.168.47.35:8555/F_tailgate',
    'rtsp://172.168.47.35:8555/G_tailgate',
]
recorder = RecodeRtsp.new(root_dir_saving="./assets/TEST_250428_3")
recorder.recode(rtsp_streams=rtsp_streams, recode_period=10, postfix='mp4', max_duration=25, merge=False)
 
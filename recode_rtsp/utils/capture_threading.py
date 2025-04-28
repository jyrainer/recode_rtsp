def frame_capture_thread(cap, frame_queue, running_flag):
    while running_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame")
            continue
        try:
            frame_queue.put_nowait(frame)
        except frame_queue.Full:
            print("[WARNING] Frame queue full, dropping frame")
        # print(frame_queue.qsize())

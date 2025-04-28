# Recode RTSP

`Recode RTSP`는 RTSP 스트림을 받아서 주기적으로 녹화하고 저장하는 Python 모듈입니다.  
스트림을 일정 간격으로 나누어 저장하거나, 최대 녹화 시간 제한을 설정할 수 있습니다.

---

## ✨ Features
- 여러 개의 RTSP 스트림 동시 녹화
- 지정 시간마다 새로운 파일로 분할 저장
- 전체 녹화 최대 시간 설정 지원
- 녹화 파일 포맷 지정 가능 (e.g., mp4)
- 녹화 완료 후 파일 병합(merge) 지원

---

## 📦 설치 방법

```bash
git clone https://github.com/jyrainer/recode_rtsp.git
cd recode_rtsp
pip install -e .

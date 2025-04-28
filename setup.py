# setup.py
from setuptools import setup, find_packages

setup(
    name='recode-rtsp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'pyyaml'
    ],
    python_requires='>=3.9',
    author='Jaeyong Park',
    author_email='jy.park@pia.space',
    description='Record RTSP streams and save them as MP4 files.',
    url='https://github.com/jyrainer/recode_rtsp.git',
)
import sys
from pyunpack import Archive
import requests
import os
import shutil

try:
    if not os.path.isdir("temp"):
        print(" - no temp folder found, creating one...")
        os.mkdir("temp")

    print(" - downloading ffmpeg...")
    ffmpeg = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z").content
    with open("temp/ffmpeg.7z", "wb") as file:
        file.write(ffmpeg)

    if not os.path.isdir("temp/ffmpeg"):
        print(" - no temp/ffmpeg folder found, creating one...")
        os.mkdir("temp/ffmpeg")

    print(" - extracting ffmpeg...")
    Archive("temp/ffmpeg.7z").extractall("temp/ffmpeg/")

    print(" - copying ffmpeg...")
    shutil.copy(f"temp/ffmpeg/{os.listdir('temp/ffmpeg')[0]}/bin/ffmpeg.exe", "ffmpeg.exe")

    print(" - done!")
except KeyboardInterrupt:
    print(" - aborting...")
    sys.exit(0)

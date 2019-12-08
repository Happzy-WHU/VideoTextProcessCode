import cv2
from PIL import Image
import numpy as np
import os
import datetime

def cal_stderr(img, imgo=None):
    if imgo is None:
        return (img ** 2).sum() / img.size * 100
    else:
        return ((img - imgo) ** 2).sum() \
               / img.size * 100


def formatTime(s):
    h = s // 3600
    m = (s - h * 3600) // 60
    s = s - h * 3600 - m * 60
    t = datetime.time(hour=h, minute=m, second=s)
    return datetime.time.isoformat(t)


def save_image(ex_folder, img: Image, starts: int, ends: int):
    start_time = formatTime(starts)
    end_time = formatTime(ends)
    timeline = '-'.join([start_time, end_time]) + ".png"
    try:
        imgname = os.path.join(ex_folder, timeline.replace(':',''))
        img.save(imgname)
        print('%s' % timeline+"以前没有问题")
    except Exception:
        print('%s' % timeline+"处出现了问题")


def getPictures(video_filename):
    ex_folder = os.path.splitext(video_filename)[0]
    if not os.path.exists(ex_folder):
        os.mkdir(ex_folder)
    skip_frames = 2818
    vCap = cv2.VideoCapture(video_filename)
    for i in range(skip_frames):
        vCap.read()
    startFrame = skip_frames
    currFrame = skip_frames
    # 帧频
    fps = vCap.get(cv2.CAP_PROP_FPS)
    picIsNotNor = True
    subtitleImg = None
    lastImg = None
    img_count = 0
    while picIsNotNor:
        for j in range(9):
            vCap.read()
            currFrame += 1
        picIsNotNor, frame = vCap.read()
        currFrame += 1
        if frame is None:
            print('video: %s already finished at %d frame.' % (video_filename, currFrame))
            break

        img = frame[:, :, 0]
        img = img[700:770, :]
        _, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)

        if cal_stderr(img) < 1:
            continue

        if img_count == 0:
            subtitleImg = img
            print('video: %s add subtitle at %d frame.' % (video_filename, currFrame))
            lastImg = img
            img_count += 1
        elif img_count > 10:
            img_count = 0
            subtitleImg = Image.fromarray(subtitleImg)
            save_image(ex_folder, subtitleImg, int(startFrame/fps), int(currFrame/fps))
            startFrame = currFrame    # 开始时间往后移
        else:
            if cal_stderr(img, lastImg) > 1:
                subtitleImg = np.vstack((subtitleImg, img))
                lastImg = img
                img_count += 1
                print('video: %s add subtitle at %d frame.' % (video_filename, currFrame))
    if img_count > 0:
        subtitleImg = Image.fromarray(subtitleImg)
        save_image(ex_folder, subtitleImg, int(startFrame / fps), int(currFrame / fps))
    print('video: %s pictures all get!' % video_filename)


if __name__ == '__main__':
    video_filename = 'D:\\Videos\\陈翔六点半之铁头无敌.mp4'
    getPictures(video_filename)

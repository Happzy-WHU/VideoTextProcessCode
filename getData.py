import cv2
video_filename = 'D:/Videos/陈翔六点半之铁头无敌.mp4'
videoCap = cv2.VideoCapture(video_filename)
# 帧频
fps = videoCap.get(cv2.CAP_PROP_FPS)
# 视频总帧数
total_frames = int(videoCap.get(cv2.CAP_PROP_FRAME_COUNT))
# 图像尺寸
image_size = (int(videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
              int(videoCap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print(fps)
print(total_frames)
print(image_size)

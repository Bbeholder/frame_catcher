import os
import pandas as pd
import numpy as np
import cv2  # 代入OpenCV模块
video_list = []
# 存储原视频路径
file_dir = '输入视频文件夹'
# 存储标签路径（最好不要放一个文件夹叭qwq）
file_result = '输入标签文件夹'

file_list = os.listdir(file_dir)
for files in file_list:
    file_type = str(files).split('.')[1]
    if file_type == "avi":
        video_list.append(files)
# 对视频排序
video_list.sort()
# 看看当前做到哪了
files_res = os.listdir(file_result)
final_label = 0
for txt in files_res:
    if str(txt).split('.')[1] == "txt":
        final_label = final_label + 1
# 工作标志
keep_flag = False
for name_num in range(final_label, len(video_list)):
    name = video_list[name_num]
    video_path = os.path.join(file_dir, name)
    v = cv2.VideoCapture(video_path)
    label = []
    if keep_flag:
        # 释放
        v.release()
        # 关闭窗口，清除程序所占用的内存
        cv2.destroyAllWindows()
        break
    # 获取帧总数
    frame_num = int(v.get(7))
    for j in range(frame_num):
        label.append(0)
    # 获取视频帧率
    fps = v.get(5)
    tar_file = [name.split('.')[0], 'txt']
    file_name = '.'.join(tar_file)
    tar_path = os.path.join(file_result, file_name)
    # 控制前进标志
    forward_flag = False
    # 后退标
    label_flag = True
    now_frame = 0
    ret, frame = v.read()
    while True:
        if forward_flag:
            ret, frame = v.read()
        if ret:
            frame_down = cv2.pyrDown(frame)
            cv2.imshow(name, frame_down)
            if v.get(1) >= now_frame:
                label_flag = True
            else:
                label_flag = False
        else:
            file = open(tar_path, 'w+')
            file.truncate(0)
            for m in range(frame_num):
                line_list = [str(m), str(label[m]), '\n']
                line = ' '.join(line_list)
                file.write(line)
            file.close()
            break
        key = cv2.waitKey(int(1000 / fps))
        # 暂停和播放
        if key & 0xFF == ord('b'):
            if forward_flag:
                forward_flag = False
            else:
                forward_flag = True
        # 前进
        if key & 0xFF == ord('d'):
            future_frame = v.get(1) + 24
            v.set(1, future_frame)
            ret, frame = v.read()
        # 后退
        if key & 0xFF == ord('a'):
            if now_frame == 0 or now_frame < v.get(1):
                now_frame = v.get(1)
            else:
                now_frame = now_frame
            old_frame = v.get(1) - 26
            v.set(1, old_frame)
            ret, frame = v.read()
        # 标记帧
        if key & 0xFF == ord('j'):
            if label_flag:
                frame_flag = int(v.get(1))  # 从0开始帧的位置
                label[frame_flag] = 1
                print(frame_flag)
        # 暂时结束
        if key & 0xFF == ord('q'):
            keep_flag = True
            break
    # 释放
    v.release()
    # 关闭窗口，清除程序所占用的内存
    cv2.destroyAllWindows()

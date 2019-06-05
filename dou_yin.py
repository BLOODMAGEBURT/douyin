#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: dou_yin.py 
@time: 5/14/19 09:16 
@description：抖音自动化运营
"""

import os
import shutil
import time
from datetime import datetime

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from utils.baidu_utils import get_access_token, analysis_face, parse_face_pic, TYPE_IMAGE_LOCAL
from utils.device_utils import start_my_app, play_next_video, get_screen_shot_part_img
from utils.douyin_utils import wait_for_download_finished, is_a_ad

# 应用包名和Activity
package_name = 'com.ss.android.ugc.aweme'
activity_name = 'com.ss.android.ugc.aweme.splash.SplashActivity'

# 一条视频识别的最长时间
RECOGNITE_TOTAL_TIME = 10

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


def save_video_met():
    """
    :return:
    """
    # 分享 根据手机 设置不同的 x y 坐标
    os.system("adb shell input tap 1009 1362")
    time.sleep(0.05)

    # 保存到本地 根据手机 设置不同的 x y 坐标
    os.system("adb shell input tap 366 1581")

    time.sleep(0.2)

    # 等待视频保存成功
    wait_for_download_finished(poco)


if __name__ == '__main__':

    access_token = get_access_token()

    # 处理的次数
    handle_count = 0

    print('打开抖音~')
    # 打开抖音
    start_my_app(package_name, activity_name)

    time.sleep(5)

    while True:
        time.sleep(2)
        if is_a_ad():
            print('这是一条广告，过滤~')
            play_next_video()
            time.sleep(2)
        # 判断存储文件夹是否存在
        if not os.path.exists('./images'):
            os.mkdir('./images')

        # 开始识别的时间
        recognize_time_start = datetime.now()

        # 识别次数
        recognize_count = 1

        # 循环地去刷抖音
        while True:
            if is_a_ad():
                print('这是一条广告，过滤~')
                play_next_video()
                time.sleep(2)
            # 获取截图
            print('开始第{}次截图'.format(recognize_count))

            # 截取屏幕有用的区域，过滤视频作者的头像、BGM作者的头像
            screen_name = get_screen_shot_part_img('images/temp{}.jpg'.format(recognize_count))

            # 人脸识别
            recognize_result = analysis_face(parse_face_pic(screen_name, TYPE_IMAGE_LOCAL, access_token))

            recognize_count += 1

            # 第n次识别结束后的时间
            recognize_time_end = datetime.now()

            # 这是一个美女
            if recognize_result:
                save_video_met()
                handle_count += 1
                print('识别到一个美女，继续下一个视频~')
                break
            else:
                if (recognize_time_end - recognize_time_start).seconds < RECOGNITE_TOTAL_TIME:
                    print('继续识别~')
                    continue
                else:
                    print('超时！！！这是一条没有吸引力的视频！')
                    # 跳出里层循环
                    break

        # 删除临时文件
        shutil.rmtree('./images')
        os.mkdir('./images')

        # 播放下一条视频
        print('==' * 30)
        time.sleep(1)
        print('准备播放下一个视频~')
        play_next_video()
        time.sleep(1.5)

# by hkkk
# thanks https://github.com/1033020837/Bilibili for the idea of adding the Referer in the headers

import requests
import re
import json
from moviepy.editor import *

def get_reponse(url):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    response=requests.get(url=url,headers=headers)
    return response

def getinfo(url):

    response=get_reponse(url)
    title = re.findall('<h1 title="(.*?)" class="video-title tit">', response.text)[0]
    data=re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
    jsondata=json.loads(data)
    audiourl=jsondata['data']['dash']['audio'][0]['baseUrl']
    videourl = jsondata['data']['dash']['video'][0]['baseUrl']
    videoinfo=[title,audiourl,videourl]
    return videoinfo

def save(title,audiourl,videourl):
    audio_content = get_reponse(audiourl).content
    video_content = get_reponse(videourl).content
    with open(title+'.mp3',mode='wb') as f:
        f.write(audio_content)
    with open(title+'.mp4',mode='wb') as f:
        f.write(video_content)
    print("视频和音频已保存……")


url='https://www.bilibili.com/video/BV1kW4y1V7Uj'
video_info=getinfo(url)
print(video_info)
save(video_info[0],video_info[1],video_info[2])

ad = AudioFileClip(video_info[0]+'.mp3')
vd = VideoFileClip(video_info[0]+'.mp4')

vd2 = vd.set_audio(ad)  # 将提取到的音频和视频文件进行合成
vd2.write_videofile(video_info[0]+'output.mp4')  # 输出新的视频文件
os.remove(video_info[0]+'.mp3')
os.remove(video_info[0]+'.mp4')

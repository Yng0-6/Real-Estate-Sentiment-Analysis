# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:01:13 2024

@author: lenovo
"""
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
import time
from time import strftime, localtime
import os
from snownlp import SnowNLP

import jieba.analyse
def get_bilibili_danmu(v_url,v_result_file):
    headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",}
    print('The video url is:',v_url)
    r1=requests.get(url=v_url,headers=headers)
    html1=r1.json()
    cid=html1['data'][0]['cid']
    print('The CID for this video is:',cid)
    danmu_url='http://comment.bilibili.com/{}.xml'.format(cid)
    print('The bullet url is',danmu_url)
    r2=requests.get(danmu_url)
    html2=r2.text.encode('raw_unicode_escape')
    soup=BS(html2,'xml')
    danmu_list=soup.find_all('d')
    print('A total of {} bullet comments were crawled.'.format(len(danmu_list)))
    video_url_list=[]
    danmu_url_list=[]
    time_list=[]
    text_list=[]
    for d in danmu_list:
        data_split=d['p'].split(',')
        temp_time=time.localtime(int(data_split[4]))
        danmu_time=strftime("%Y-%m-%d %H:%M:%S",temp_time)
        video_url_list.append(v_url)
        danmu_url_list.append(danmu_url)
        time_list.append(danmu_time)
        text_list.append(d.text)
        print('{}:{}'.format(danmu_time,d.text))
    df=pd.DataFrame()
    df['Video URL']=video_url_list
    df['Bullet URL']=danmu_url_list
    df['Bullet Time']=time_list
    df['Bullet Text']=text_list
    if os.path.exists(v_result_file):
        header=None
    else:
        header=['Video URL','Bullet UR','Bullet Time','Bullet Text']
    df.to_csv(v_result_file,encoding='utf_8_sig',mode='a+',index=False,header=header)
    
print('The crawler program has begun execution!')
csv_file='Bilibili bullet.csv'
if os.path.exists(csv_file):
    print('The file{}already exists, Starting to delete the file.'.format(csv_file))
    os.remove(csv_file)
    print('{}Deleted file'.format(csv_file))
bv_list=['BV1Z4411P7KN','BV1tg4y1z7Xb','BV1DE411h75g']
for bv in bv_list:
    get_bilibili_danmu(v_url='https://api.bilibili.com/x/player/pagelist?bvid={}'.format(bv),v_result_file='Bilibili bullet.csv')
print('The web crawler has completed its execution.')







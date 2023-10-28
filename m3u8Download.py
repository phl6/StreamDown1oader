import os
import re
import requests
import subprocess

def getM3U8(url):
    return requests.get(url).content.decode('utf-8')

def downloadTs(urls, destination):
    if (not os.path.exists(destination)):
        os.mkdir(destination)
    fileIndex = 0
    for url in urls:
        fileIndex = fileIndex + 1
        print(f'downloading from: {url}')
        fileName = f'{destination}/{fileIndex}.ts'
        # download video and save to destinationFolder
        r = requests.get(url, stream=True)
        if r:
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        print(f'downloaded: {fileName}')
    print('download completed')

def sortFiles(directory):
    sortedStr = sorted(os.listdir(directory), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
    appended_list = [f'{directory}/{item}' for item in sortedStr]
    return appended_list

def merge(tsFiles, output):
    # Create a command to merge the TS files using ffmpeg
    command = ['ffmpeg', '-i', 'concat:' + '|'.join(tsFiles), '-c', 'copy', output + ".mp4"]
    subprocess.call(command)

def isDailyMotion(url): 
    patternSec = re.compile(r'(https://.+.dailymotion.com)(/sec.+)')
    if patternSec.match(url):
        return re.search(patternSec, url).group(1)
    
def isPH(url):
    patternSec = re.compile(r'(https://.+phncdn.com/.+.urlset/)(.+)')
    if patternSec.match(url):
        return re.search(patternSec, url).group(1)
    
def getDailyMotionTsUrls(url, m3u8):
    pattern = re.compile(r'(/sec.+.ts)')
    urls = []
    for tsUrl in re.findall(pattern, m3u8):
        urls.append(url + tsUrl)
    return urls

def getPhnCdnTsUrls(url, m3u8):
    pattern = re.compile(r'(seg.+)')
    urls = []
    for tsUrl in re.findall(pattern, m3u8):
        urls.append(url + tsUrl)
    return urls

def getTsUrls(m3u8):    
    pattern = re.compile(r'(https://.+.ts)')
    urls = []
    for url in re.findall(pattern, m3u8):
        urls.append(url)
    return urls
    
def main(url, output):
    result = getM3U8(url)
    
    urls = None
    dailyMotionUrl = isDailyMotion(url)
    phUrl = isPH(url)
    
    if dailyMotionUrl is not None:
        urls = getDailyMotionTsUrls(dailyMotionUrl, result)
    elif phUrl is not None: #ph
        urls = getPhnCdnTsUrls(phUrl, result)
    else:
        urls = getTsUrls(result)
    
    downloadTs(urls, output)
    merge(sortFiles(f'./{output}'), output)

if __name__ == '__main__':    
    #dailyMotion
    url = "https://proxy-29.sg1.dailymotion.com/sec(IbTcRogFtkG5Xv5BOy6Jot5saDD534gHRqyNnGO_w5nu1deiDHew4X_AAJ40Ba-KJltZd6K9TmUpAx9XgzIhNW5Mv35GwwUpFXogFCY3QrQ)/video/406/733/523337604_mp4_h264_aac_1.m3u8"
    #ph
    # url = "https://ev-h.phncdn.com/hls/videos/202112/15/399717401/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_399717401.mp4.urlset/index-f4-v1-a1.m3u8?validfrom=1698509996&validto=1698517196&ipa=192.166.244.75&hdl=-1&hash=6bGqFC2fQ5sHmfg%2FX41SaB8SwhA%3D"
    main(url, "test")
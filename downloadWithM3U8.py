import re
from m3u8Helper import getM3U8, downloadTs, sortFiles, merge, rmdirAndContents

def isDailyMotion(url): 
    patternSec = re.compile(r'(https://.+.dailymotion.com)(/sec.+)')
    if patternSec.match(url):
        return re.search(patternSec, url).group(1)
    
def isPH(url):
    patternSec = re.compile(r'(https://.+phncdn.com/.+.urlset/)(.+)')
    if patternSec.match(url):
        return re.search(patternSec, url).group(1)

def getTsUrls(url, m3u8, pattern):
    urls = []
    for tsUrl in re.findall(pattern, m3u8):
        if url is not None:
            urls.append(url + tsUrl)            
        else:
            rawLinkPattern = re.compile(r'(https://.+)')
            resourceLink = re.search(rawLinkPattern, tsUrl).group(1)
            urls.append(resourceLink)
    return urls

def checkSource(url, m3u8):
    dailyMotionUrl = isDailyMotion(url)
    phUrl = isPH(url)
    urls = None
    if dailyMotionUrl is not None:
        urls = getTsUrls(dailyMotionUrl, m3u8, re.compile(r'(/sec.+.ts)'))
    elif phUrl is not None:
        urls = getTsUrls(phUrl, m3u8, re.compile(r'(seg.+)'))
    else:
        urls = getTsUrls(None, m3u8, re.compile(r'(https://.+.ts)'))
    return urls

def main(url, output):
    m3u8 = getM3U8(url)
    urls = checkSource(url, m3u8)
    downloadTs(urls, output)
    merge(sortFiles(f'./{output}'), output)
    rmdirAndContents(f'./{output}')

if __name__ == '__main__':    
    #dailyMotion
    url = "https://proxy-17.sg1.dailymotion.com/sec(saQeXx3qXZg3T3rkC8HACJ-5WJrUttT0_WkDpKLyTNVvUkhNnM3qAwmPVG2H0ImsEHNmUVMHujRBAaVUL7ka0kX6VNKon0SPW0nAq0o73kU)/video/480/909/327909084_mp4_h264_aac_hd.m3u8"
    #ph
    # url = "https://dv-h.phncdn.com/hls/videos/202310/24/441800011/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_441800011.mp4.urlset/index-f4-v1-a1.m3u8?ttl=1698571389&l=0&ipa=192.166.244.75&hash=ccd2a6908123ec762935bcb8bdc7b0f2"
    
    main(url, "test")
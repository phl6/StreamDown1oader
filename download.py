import os
import re
import requests
from m3u8Helper import sortFiles, merge, rmdirAndContents

def downloadTs(tsUrl, startRange, endRange, destination, regex):
    # create folder if not exists
    if (not os.path.exists(destination)):
        os.mkdir(destination)
        
    for i in range(startRange, endRange + 1):            
        # create url string for download
        phrase = re.search(regex, tsUrl)
        url = f'{phrase.group(1)}{i}{phrase.group(3)}'
        fileName = f'{destination}/{i}.ts'
        
        # download video and save to destinationFolder
        r = requests.get(url, stream=True)
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
        print(f'downloaded: {fileName}')
    print('download completed')

# startRange, endRange - retrieve from *m3u8 file in developer tool
# regex - each website has its own video retrieval url format
def main(tsUrl, output, startRange, endRange, regex):
    downloadTs(tsUrl, startRange, endRange, output, regex)
    merge(sortFiles(f'./{output}'), output)
    rmdirAndContents(f'./{output}')

if __name__ == '__main__':
    # Video Source Regex
    DAILY_MOTION_REGEX = r"(.+/frag\()([0-9]+)(\).+)"
    PB_REGEX = r"(.+/seg-)([0-9+])(.+)"
    
    # example1
    # tsUrl = "https://proxy-17.sg1.dailymotion.com/sec(saQeXx3qXZg3T3rkC8HACJ-5WJrUttT0_WkDpKLyTNVvUkhNnM3qAwmPVG2H0ImsEHNmUVMHujRBAaVUL7ka0sEdlNF4qSgofqUzDdhrgyI)/frag(9)/video/480/909/327909084_mp4_h264_aac_hd.ts"
    # output = 'example1'
    
    # example2
    tsUrl = "https://dv-h.phncdn.com/hls/videos/202310/24/441800011/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_441800011.mp4.urlset/seg-1-f2-v1-a1.ts?ttl=1698571389&l=0&ipa=192.166.244.75&hash=ccd2a6908123ec762935bcb8bdc7b0f2"
    output = 'example2'
    main(tsUrl, output, 1, 14, PB_REGEX)
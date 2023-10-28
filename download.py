import os
import re
import requests
import subprocess

def downloadTs(videoSource, startRange, endRange, destination, regex):
    for i in range(startRange, endRange+1):
        # create folder if not exists
        if (not os.path.exists(destination)):
            os.mkdir(destination)
            
        # create url string for download
        phrase = re.search(regex, videoSource)
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

def sortFiles(directory):
    sortedStr = sorted(os.listdir(directory), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
    appended_list = [f'{directory}/{item}' for item in sortedStr]
    return appended_list

def merge(tsFiles, outputFileName):
    # Create a command to merge the TS files using ffmpeg
    command = ['ffmpeg', '-i', 'concat:' + '|'.join(tsFiles), '-c', 'copy', outputFileName]
    subprocess.call(command)

# startRange, endRange - retrieve from *m3u8 file in developer tool
# regex - each website has its own video retrieval url format
def main(url, destination, outputName, startRange, endRange, regex):
    downloadTs(url, startRange, endRange, destination, regex)
    merge(sortFiles(f'./{destination}'), outputName)


if __name__ == '__main__':
    # Video Source Regex
    DAILY_MOTION_REGEX = r"(.+/frag\()([0-9]+)(\).+)"
    PB_REGEX = r"(.+/seg-)([0-9+])(.+)"
    
    # example1
    # url = "https://proxy-17.sg1.dailymotion.com/sec(saQeXx3qXZg3T3rkC8HACJ-5WJrUttT0_WkDpKLyTNVvUkhNnM3qAwmPVG2H0ImsEHNmUVMHujRBAaVUL7ka0sEdlNF4qSgofqUzDdhrgyI)/frag(9)/video/480/909/327909084_mp4_h264_aac_hd.ts"
    # destination = 'example1'
    # outputName = 'example1.mp4'    
    
    # example2
    url = "https://cv-h.phncdn.com/hls/videos/202310/04/440603361/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_440603361.mp4.urlset/seg-6-f2-v1-a1.ts?EcfyprBnymb1miLRgBOqvyL3025wnu_C_Jpifd1mYfrdXrDUWpz8mq4T5IxzLnS4vXgx6MF-8yrrLhwvJAcFf6vfVjC06YWubzSa4RAZj4EAeL9yfk1SieqDlr6i2Jm0J1SAmZLF1BR7uo4LR6bdUh_fdpKm6ECcuPCTsf5GxQHspMIrAvO1l1T7yemsI_pmPb9OdDLWxw7P"
    destination = 'example2'
    outputName = 'example2.mp4'
    main(url, destination, outputName, 1, 16, PB_REGEX)
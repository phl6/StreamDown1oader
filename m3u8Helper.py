import os
import requests
import subprocess
import shutil

def getM3U8(url):
    return requests.get(url).content.decode('utf-8')

def downloadTs(urls, destination):
    print(f'Total files to be downloaded: {len(urls)}')
    if (not os.path.exists(destination)):
        os.mkdir(destination)
    fileIndex = 0
    for url in urls:
        fileIndex += 1
        print(f'downloading from: {url}')
        fileName = f'{destination}/{fileIndex}.ts'
        # download video and save to destinationFolder
        r = requests.get(url, stream=True)
        if r:
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
        print(f'downloaded: {fileName}')
    print('download completed')

def sortFiles(directory):
    sortedStr = sorted(os.listdir(directory), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
    return [f'{directory}/{item}' for item in sortedStr]

def merge(tsFiles, output):
    # Create a command to merge the TS files using ffmpeg
    outputFile = output + ".mp4"
    command = ['ffmpeg', '-i', 'concat:' + '|'.join(tsFiles), '-c', 'copy', outputFile]
    subprocess.call(command)

def rmdirAndContents(directory):
    shutil.rmtree(directory)
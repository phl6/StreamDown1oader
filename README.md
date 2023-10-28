# StreamDown1oader
Download videos from Streaming Platforms

## Requirement
- python
- ffmpeg 
    ```bash
    brew install ffmpeg
     ```

## Installation 

1. clone and cd into this project
   
2. ```bash
    pip install virtualenv    

    python -m venv venv

    source ./venv/bin/activate

    pip install -r requirements.txt
    ```

3. go to developer tool -> network -> look for postfix "m3u8" file<br/>
    this contains the total number of ts files for this streaming video, find the first and last number of video fragments

    remarks: look for frag / seg keywords in m3u8 or ts url 😉

    e.g.</br>
    /sec(Y1vpsrJkRaxa6jF-j2RR0t6BMk26dKEGMI_FBit0hLEpEt3Bj9n5CBRhMR_MAovimKqZsg_QsCfjOalJE5FOqm3eRSUwyNvMPfWAqfwo7fY)/frag(<strong>153</strong>)/video/580/909/327909085_mp4_h264_aac.ts
#EXT-X-ENDLIST
    ![Alt text](image.png)

4. go to download.py, edit the main()
   
5. sit back and enjoy 😏

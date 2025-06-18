import re
import os
import urllib.parse
from m3u8Helper import getM3U8, downloadTs, sortFiles, merge, rmdirAndContents

def extract_ts_urls_from_m3u8(m3u8_content, base_url):
    """
    Extract TS URLs from m3u8 content regardless of source.
    This function handles both absolute and relative URLs in m3u8 playlists.
    """
    # Extract all lines that might be TS file references
    lines = m3u8_content.split('\n')
    ts_urls = []
    
    # If the m3u8 contains references to other m3u8 files (master playlist), follow them
    # Look for lines containing .m3u8, but filter out comments
    sub_playlist_urls = [line for line in lines if '.m3u8' in line and not line.startswith('#')]
    if sub_playlist_urls:
        # This could be a master playlist with references to other m3u8 files
        for sub_url in sub_playlist_urls:
            sub_url = sub_url.strip()
            # Skip if this is part of a comment or empty
            if not sub_url or sub_url.startswith('#'):
                continue
                
            # Handle relative URLs
            full_sub_url = make_absolute_url(sub_url, base_url)
            # Fetch and process the sub-playlist
            sub_content = getM3U8(full_sub_url)
            sub_ts_urls = extract_ts_urls_from_m3u8(sub_content, get_base_url(full_sub_url))
            if sub_ts_urls:
                return sub_ts_urls
    
    # Look for .ts files
    for line in lines:
        line = line.strip()
        # Skip if this is a comment or empty
        if not line or line.startswith('#'):
            continue
            
        # Support multiple formats: .ts, .m4s segments
        if line.endswith('.ts') or line.endswith('.m4s') or 'seg-' in line:
            ts_urls.append(make_absolute_url(line, base_url))
    
    return ts_urls

def get_base_url(url):
    """
    Extract the base URL from a full URL to properly resolve relative paths.
    """
    parsed_url = urllib.parse.urlparse(url)
    path_parts = parsed_url.path.split('/')
    
    # If path ends with a file, remove the file part
    if '.' in path_parts[-1]:
        path_parts.pop()
    
    base_path = '/'.join(path_parts)
    if not base_path.endswith('/'):
        base_path += '/'
    
    return urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        base_path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))

def make_absolute_url(url, base_url):
    """
    Convert a relative URL to an absolute URL based on the base URL.
    If the URL is already absolute, return it unchanged.
    """
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    # Handle absolute paths (starting with /)
    if url.startswith('/'):
        parsed_base = urllib.parse.urlparse(base_url)
        return urllib.parse.urlunparse((
            parsed_base.scheme,
            parsed_base.netloc,
            url,
            '',
            '',
            ''
        ))
    
    # Handle relative paths
    return urllib.parse.urljoin(base_url, url)

def main(url, output, fileFormatExtension):
    """
    Main function to process an m3u8 URL and download the video/audio.
    """
    print(f"Processing URL: {url}")
    m3u8_content = getM3U8(url)
    base_url = get_base_url(url)
    
    print(f"Extracting TS URLs from m3u8 content...")
    ts_urls = extract_ts_urls_from_m3u8(m3u8_content, base_url)
    
    if not ts_urls:
        print("No media segments found in the m3u8 file!")
        return
    
    print(f"Found {len(ts_urls)} media segments")
    downloadTs(ts_urls, output)
    merge(sortFiles(f'./{output}'), output, fileFormatExtension)
    rmdirAndContents(f'./{output}')
    print(f"Successfully downloaded and merged to {output}{fileFormatExtension}")

if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Download video/audio from m3u8 URL')
    parser.add_argument('url', nargs='?', help='URL of the m3u8 file')
    parser.add_argument('-o', '--output', default='output', help='Output filename (without extension)')
    parser.add_argument('-e', '--extension', default='.mp4', help='Output file extension (default: .mp4)')
    
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args.url:
            main(args.url, args.output, args.extension)
        else:
            parser.print_help()
    else:
        print("Usage: python downloadWithM3U8.py <m3u8_url> -o [output_filename] -e [file_extension]")
        print("\nExample:")
        print("python downloadWithM3U8.py https://example.com/video.m3u8 -o my_video -e .mp4")
        
        # For convenience, uncomment one of these examples or add your own:
        main("https://jx2.ke-mi.vip:2087/K2_M3u8/TIqalVai16fEKsC3_aH4L8sH27AUAJ1VioZ9pangFEvqc0MMx3o1eec4qBFDr_bdlrgFeUSGhQAFE0jgwFiAztwbaV0so69zdQgod0QMZ_asg.m3u8?vkey=6tst1q9ad7ewc7c1a7cd6pzmtbpbga6l", "test", ".mp4")


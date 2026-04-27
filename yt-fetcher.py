from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube" , "v3", developerKey=key)

def get_data(url, max_comments=100):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    id = params['v'][0]
    
    #fetch video title
    req_title = youtube.videos().list(part = "snippet", id=id)
    res_title = req_title.execute()
    vid_title = res_title['items'][0]['snippet']['title']
    
    #fetch comments
    comments = []
    count = 0
    next_page_token = None
    
    while count < max_comments:
        req_comments = youtube.commentThreads().list(
            part="snippet",
            videoId=id,
            textFormat="plainText",
            pageToken=next_page_token,
            maxResults=100,
            order='relevance'
        )

        res_comments = req_comments.execute()

        for item in res_comments['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment_text)
            count += 1

            if count >= max_comments:
                break

        next_page_token = res_comments.get('nextPageToken')

        if not next_page_token:
            break

    return vid_title, comments

a,b=get_data('https://www.youtube.com/watch?v=1SfnIVxYo1c',max_comments=5)
print(b)
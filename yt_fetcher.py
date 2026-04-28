from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube" , "v3", developerKey=key)

def get_data(url, max_comments=5):
    
    parsed = urlparse(url)

    if not parsed.netloc:
        return None, None, [], []
    
    if parsed.netloc == 'youtu.be':
        vid = parsed.path[1:]
    else:
        params = parse_qs(parsed.query)
        vid = params['v'][0]
        
        #fetch video title
    req_title = youtube.videos().list(part = "snippet", id=vid)
    res_title = req_title.execute()

    if not res_title['items']:
        return vid, None, [], []
        
    vid_title = res_title['items'][0]['snippet']['title']
    
    #fetch comments
    comments = []
    likes = []
    count = 0
    next_page_token = None
    
    while count < max_comments:
        req_comments = youtube.commentThreads().list(
            part="snippet",
            videoId=vid,
            textFormat="plainText",
            pageToken=next_page_token,
            maxResults=100,
            order='relevance'
        )

        res_comments = req_comments.execute()

        if not res_comments['items']:
            return vid, vid_title, [], []
        
        else:

            for item in res_comments['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                like_count = int(item['snippet']['topLevelComment']['snippet']['likeCount'])
                comments.append(comment_text)
                likes.append(like_count)
                count += 1

                if count >= max_comments:
                    break

            next_page_token = res_comments.get('nextPageToken')

            if not next_page_token:
                break

    return vid, vid_title, comments, likes


#ALSO store likeCount → lets you: filter low-quality comments + weight sentiment later
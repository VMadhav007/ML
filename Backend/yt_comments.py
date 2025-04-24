from googleapiclient.discovery import build

# Replace this with your actual YouTube API key
API_KEY = "AIzaSyAp5Uz30yIsavUtbGwWaumf-4ua4FRB-rQ"

def get_youtube_comments(video_id, max_results=10):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    
    response = request.execute()
    
    comments = []
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments

# Example Usage
video_id = input("Enter YouTube Video ID: ")  # Example: 'dQw4w9WgXcQ'
comments = get_youtube_comments(video_id)

print("\n📌 YouTube Comments:")
for idx, comment in enumerate(comments, 1):
    print(f"{idx}. {comment}")

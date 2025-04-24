from fastapi import FastAPI
from pydantic import BaseModel
from googleapiclient.discovery import build
import pickle
from nltk.stem.porter import PorterStemmer
import re
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (Allows frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all request methods
    allow_headers=["*"],  
)

# YouTube API Key (Replace with your actual key)
API_KEY = "AIzaSyAp5Uz30yIsavUtbGwWaumf-4ua4FRB-rQ"

# Load trained sentiment model and vectorizer
with open(r"E:\ML\Sentiment analysis\WEB_APP\Backend\sentiment_model.pkl", "rb") as file:
    model = pickle.load(file)

with open(r"E:\ML\Sentiment analysis\WEB_APP\Backend\vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

# Initialize Porter Stemmer
stemmer = PorterStemmer()

# Request model for receiving video URL
class VideoRequest(BaseModel):
    url: str

# Function to extract YouTube video ID from URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Function to fetch YouTube comments
def get_youtube_comments(video_id, max_results=50):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet", 
        videoId=video_id, 
        maxResults=max_results, 
        textFormat="plainText"
    )
    response = request.execute()
    
    return [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]

# Function to predict sentiment
def predict_sentiment(comment):
    stemmed_comment = " ".join([stemmer.stem(word) for word in comment.split()])
    vector = vectorizer.transform([stemmed_comment])
    prediction = model.predict(vector)
    return "Positive" if prediction[0] == 1 else "Negative"

# API Route to process YouTube video
@app.post("/analyze")
def analyze_video(data: VideoRequest):
    video_id = extract_video_id(data.url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}

    comments = get_youtube_comments(video_id)
    if not comments:
        return {"error": "No comments found"}

    results = [{"comment": c, "sentiment": predict_sentiment(c)} for c in comments]
    positive_count = sum(1 for r in results if r["sentiment"] == "Positive")
    liking_rate = (positive_count / len(comments)) * 100

    return {
        "video_id": video_id,
        "liking_rate": liking_rate,
        "total_comments": len(comments),
        "comments": results
    }

# Run the server (only if running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

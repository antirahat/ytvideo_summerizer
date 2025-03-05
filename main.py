from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    # Handle different URL formats (full URL, short URL, or direct video ID)
    if len(url.strip()) == 11:
        return url.strip()
    
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query)['v'][0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(url):
    """Get transcript from YouTube video"""
    try:
        video_id = get_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Format transcript using TextFormatter
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return formatted_transcript
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Get YouTube URL from user
    url = input("Enter YouTube video URL or video ID: ")
    
    # Get and print transcript
    transcript = get_transcript(url)
    print("\nTranscript:")
    print(transcript)

if __name__ == "__main__":
    main()
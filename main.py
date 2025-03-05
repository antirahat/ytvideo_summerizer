from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def get_video_id(url):
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

def generate_summary(transcript):
    """Generate bullet-point summary using OpenAI API"""
    try:
        # Create a prompt for the AI
        prompt = f"Please summarize the following transcript into key bullet points that capture the main topics and ideas discussed:\n\n{transcript}"
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise bullet-point summaries of video transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the summary
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def main():
    # Get YouTube URL from user
    url = input("Enter YouTube video URL or video ID: ")
    
    # Get transcript
    print("\nFetching transcript...")
    transcript = get_transcript(url)
    
    if transcript.startswith("Error"):
        print(transcript)
        return
    
    # Generate and print summary
    print("\nGenerating summary...")
    summary = generate_summary(transcript)
    print("\nVideo Summary:")
    print(summary)

if __name__ == "__main__":
    main()
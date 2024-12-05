from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video {video_id}.")
        return None
    except NoTranscriptFound:
        print(f"No transcript found for video {video_id}.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching transcript for video {video_id}: {e}")
        return None

from APIs.youtubeAPI import search_videos
from retrieval.transcriptFetch import get_video_transcript
from analysis.opinionAnalysis import analyze_opinions
from cleaning.dataCleaning import save_transcripts_opinions
import time

from datetime import datetime

def main():
    queries = [
        "The Finals Medium Meta",
        "The Finals Season 4",
        "The Finals medium class",
        "The Finals pike",
        "The Finals pike 556",
        "The Finals pike-556",
    ]
    max_results = 7
    all_data = []
    # look for videos, published after date, may change this to a command line arg
    published_after = "2024-10-10T00:00:00Z"

    for query in queries:
        print(f"\nSearching videos for query: {query}")
        videos = search_videos(query, max_results, published_after)

        for video in videos:
            video_id = video['id']['videoId']
            title = video['snippet']['title']
            description = video['snippet'].get('description', '')
            if "The Finals" not in title and "The Finals" not in description:
                print(f"Skipping video {video_id} as it does not mention 'The Finals' in title or description.")
                continue

            print(f"Processing video: {title} (ID: {video_id})")
            transcript = get_video_transcript(video_id)
            if not transcript:
                print(f"Skipping video {video_id} due to missing transcript.")
                continue
            opinions = analyze_opinions(transcript)
            all_data.append({
                "Query": query,
                "Video ID": video_id,
                "Title": title,
                "Transcript": transcript,
                "Opinions": opinions
            })
            time.sleep(3)

    save_transcripts_opinions(all_data)

if __name__ == "__main__":
    main()

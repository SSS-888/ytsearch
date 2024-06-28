import os
import subprocess
import sys

# Ensure googleapiclient is installed
try:
    import googleapiclient.discovery
except ImportError:
    print("googleapiclient not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client"])
    import googleapiclient.discovery

import streamlit as st

# Function to get the YouTube service
def get_youtube_service():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")  # Set your YouTube API key as an environment variable

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

# Function to get videos from a playlist
def get_videos_from_playlist(playlist_id):
    youtube = get_youtube_service()

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        videos.append({'id': video_id, 'title': title, 'description': description})

    return videos

# Function to search videos by topic
def search_videos(videos, topic):
    results = [video for video in videos if topic.lower() in video['title'].lower() or topic.lower() in video['description'].lower()]
    return results

# Streamlit app
def main():
    st.title("YouTube Playlist Video Search")
    st.write("Enter a YouTube playlist ID and a topic to search for videos within that playlist.")

    playlist_id = st.text_input("YouTube Playlist ID")
    topic = st.text_input("Search Topic")

    if st.button("Search"):
        if playlist_id and topic:
            videos = get_videos_from_playlist(playlist_id)
            matching_videos = search_videos(videos, topic)

            if matching_videos:
                st.write(f"Found {len(matching_videos)} matching video(s):")
                for video in matching_videos:
                    st.write(f"**Title:** {video['title']}")
                    st.write(f"**Description:** {video['description']}")
                    st.write(f"[Watch Video](https://www.youtube.com/watch?v={video['id']})")
                    st.write("---")
            else:
                st.write("No matching videos found.")
        else:
            st.write("Please enter both a playlist ID and a topic.")

if __name__ == "__main__":
    main()

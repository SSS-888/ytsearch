import streamlit as st
from googleapiclient.discovery import build

# Placeholder for actual API key (replace with yours after enabling YouTube Data API v3)
YOUR_API_KEY = "AIzaSyCZUSuITZsHhxfrI9bqoL3Au4L4aedUp3k"

def get_youtube_service():
    """
    Returns the YouTube service object for making API calls.
    """
    return build("youtube", "v3", developerKey=YOUR_API_KEY)

def get_playlist_items(youtube, playlist_id):
    """
    Retrieves all video IDs from the specified playlist.

    Args:
        youtube: The YouTube service object.
        playlist_id: The ID of the playlist.

    Returns:
        A list of video IDs.
    """
    video_ids = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50  # You can increase this if needed
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)
    return video_ids

def get_video_details(youtube, video_ids):
    """
    Retrieves video details for the given video IDs.

    Args:
        youtube: The YouTube service object.
        video_ids: A list of video IDs.

    Returns:
        A list of video dictionaries containing 'title' and 'description' fields.
    """
    video_details = []
    for i in range(0, len(video_ids), 50):  # YouTube API allows max 50 IDs per request
        request = youtube.videos().list(
            part="snippet",
            id=",".join(video_ids[i:i + 50])
        )
        response = request.execute()
        for item in response["items"]:
            video_details.append({
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"]
            })
    return video_details

def search_playlist(playlist_url, topic):
    """
    Searches a YouTube playlist for videos matching the given topic.

    Args:
        playlist_url: The URL of the YouTube playlist.
        topic: The topic to search for in video titles and descriptions.

    Returns:
        A list of video dictionaries containing 'title' and 'description' fields.
    """
    # Safety checks
    if "list=" not in playlist_url:
        return []  # Not a valid playlist URL

    playlist_id = playlist_url.split("list=")[1].split("&")[0]
    youtube = get_youtube_service()
    video_ids = get_playlist_items(youtube, playlist_id)
    video_details = get_video_details(youtube, video_ids)

    # Filter videos based on topic (case-insensitive)
    matching_videos = [
        video for video in video_details if topic.lower() in video["title"].lower() or topic.lower() in video["description"].lower()
    ]
    return matching_videos

st.title("YouTube Playlist Topic Search")

playlist_url = st.text_input("Enter YouTube Playlist URL")
topic = st.text_input("Enter Topic to Search")

if st.button("Search"):
    matching_videos = search_playlist(playlist_url, topic)

    if matching_videos:
        st.subheader("Matching Videos:")
        for video in matching_videos:
            st.write(f"- {video['title']}")
            st.write(f"  Description: {video['description']}")
    else:
        st.subheader("No Matching Videos Found")
    for video in matching_videos:
      st.write(f"- {video['snippet']['title']}")
else:
    st.subheader("No Matching Videos Found")

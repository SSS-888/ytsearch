import streamlit as st

# Dummy playlist data (simulated)
playlist_data = {
    "items": [
        {"snippet": {"resourceId": {"videoId": "VIDEO_ID_1"}, "title": "Sample Video 1", "description": "This is a sample video description"}},
        {"snippet": {"resourceId": {"videoId": "VIDEO_ID_2"}, "title": "Sample Video 2", "description": "Another video with a different description"}},
        # Add more dummy playlist items here
    ]
}

def search_playlist(playlist_url, topic):
    """
    Simulates searching a YouTube playlist for videos matching the given topic.

    Args:
        playlist_url: The URL of the YouTube playlist (not used in simulation).
        topic: The topic to search for in video titles and descriptions.

    Returns:
        A list of video dictionaries containing 'title' and 'description' fields.
    """
    # Simulate filtering based on topic (case-insensitive)
    matching_videos = [
        {
            "snippet": {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"]
            }
        } for item in playlist_data["items"]
        if topic.lower() in item["snippet"]["title"].lower() or topic.lower() in item["snippet"]["description"].lower()
    ]
    return matching_videos

def main():
    st.title("YouTube Playlist Topic Search")

    playlist_url = st.text_input("Enter YouTube Playlist URL", "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID")
    topic = st.text_input("Enter Topic to Search")

    if st.button("Search"):
        matching_videos = search_playlist(playlist_url, topic)

        if matching_videos:
            st.subheader("Matching Videos:")
            for video in matching_videos:
                st.write(f"- {video['snippet']['title']}")
        else:
            st.subheader("No Matching Videos Found")

if __name__ == "__main__":
    main()

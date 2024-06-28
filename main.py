import subprocess
import sys

# Ensure dependencies are installed
def install_dependencies():
    try:
        import googleapiclient.discovery
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client"])
    try:
        import streamlit as st
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])

install_dependencies()

import googleapiclient.discovery
import streamlit as st

# Function to get the YouTube service
def get_youtube_service():
    api_service_name = "youtube"
    api_version = "v3"
    developer_key = "AIzaSyCZUSuITZsHhxfrI9bqoL3Au4L4aedUp3k"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

# Streamlit app
def main():
    st.title("YouTube Data Viewer")
    
    service = get_youtube_service()
    
    query = st.text_input("Search YouTube", "Streamlit tutorial")
    if st.button("Search"):
        request = service.search().list(
            part="snippet",
            maxResults=5,
            q=query
        )
        response = request.execute()
        
        for item in response["items"]:
            st.write(f"Title: {item['snippet']['title']}")
            st.write(f"Description: {item['snippet']['description']}")
            st.write(f"Channel: {item['snippet']['channelTitle']}")
            st.write("----")

if __name__ == "__main__":
    main()

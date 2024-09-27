from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googleapiclient.discovery import build
import os
from config import API_KEY, PROXY, DEFAULT_CHANNEL

# Create YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(custom_url, proxies=None):
    # If the user input is a complete channel URL, extract the username part
    if 'youtube.com' in custom_url:
        if '/@' in custom_url:
            custom_url = custom_url.split('/@')[-1]
        elif '/channel/' in custom_url:
            return custom_url.split('/channel/')[-1]
    
    print(f"Querying channel ID, using query string: {custom_url}")
    
    request = youtube.search().list(
        part="id",
        type="channel",
        q=custom_url
    )
    try:
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            channel_id = response['items'][0]['id']['channelId']
            print(f"Found channel ID: {channel_id}")
            return channel_id
        else:
            print("No channel information found in API response")
    except Exception as e:
        print(f"Error querying channel ID: {str(e)}")
    
    return None

def download_subtitles(video_id, output_dir, proxies=None):
    try:
        # Get video title and publish date
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        
        if 'items' in video_response and len(video_response['items']) > 0:
            title = video_response['items'][0]['snippet']['title']
            publish_date = video_response['items'][0]['snippet']['publishedAt'][:10]  # Get publish date (YYYY-MM-DD format)
            # Create filename
            file_name = f"[{publish_date}]{title} - {video_id}.txt"
            file_path = os.path.join(output_dir, file_name)

            # Try to get Simplified Chinese subtitles
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans'], proxies=proxies)
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Save subtitles to file
            with open(file_path, "w", encoding="utf-8") as f:
                for entry in transcript:
                    # Remove time information
                    f.write(f"{entry['text']}\n")  # Only write the text part
            
            print(f"Downloaded Simplified Chinese subtitles for video {video_id}, filename: {file_name}")
    except NoTranscriptFound:
        print(f"No Simplified Chinese subtitles found for video {video_id}, trying Traditional Chinese")
        try:
            # Try to get Traditional Chinese subtitles
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hant'], proxies=proxies)
            # Create filename
            file_name = f"[{publish_date}]{title} - {video_id}_traditional.txt"
            file_path = os.path.join(output_dir, file_name)

            # Save subtitles to file
            with open(file_path, "w", encoding="utf-8") as f:
                for entry in transcript:
                    # Remove time information
                    f.write(f"{entry['text']}\n")  # Only write the text part
            print(f"Downloaded Traditional Chinese subtitles for video {video_id}, filename: {file_name}")
        except Exception as e:
            print(f"Unable to download subtitles for video {video_id}: {str(e)}")

def get_and_process_videos(channel_id, output_dir, proxies=None):
    if not channel_id:
        print("Unable to find channel ID")
        return

    next_page_token = None
    processed_count = 0
    downloaded_count = 0

    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            type="video",
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            if 'videoId' in item['id']:
                video_id = item['id']['videoId']
                processed_count += 1
                
                # Get video details
                video_response = youtube.videos().list(
                    part="contentDetails",
                    id=video_id
                ).execute()

                if 'items' in video_response:
                    duration = video_response['items'][0]['contentDetails']['duration']
                    print(f"Processing video {video_id}")
                    try:
                        # Download subtitles
                        download_subtitles(video_id, output_dir, proxies=proxies)
                        downloaded_count += 1
                        print(f"Processed {processed_count} videos, downloaded {downloaded_count} subtitles")
                    except TranscriptsDisabled:
                        print(f"Subtitles are disabled for video {video_id}, skipping")
                    except NoTranscriptFound:
                        print(f"No subtitles found for video {video_id}, skipping")
                    except Exception as e:
                        print(f"Error processing video {video_id}: {str(e)}")
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    print(f"\nProcessing complete. Processed {processed_count} videos, downloaded {downloaded_count} subtitles.")


def get_channel_details(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            return {
                'title': channel_info['snippet']['title'],
                'description': channel_info['snippet']['description'],
                'subscriber_count': channel_info['statistics']['subscriberCount'],
                'video_count': channel_info['statistics']['videoCount'],
                'view_count': channel_info['statistics']['viewCount']
            }
    except Exception as e:
        print(f"Error getting channel details: {str(e)}")
    
    return None

def main():
    if DEFAULT_CHANNEL:
        channel_url = DEFAULT_CHANNEL
        print(f"Using default channel: {channel_url}")
    else:
        channel_url = input("Please enter the YouTube channel address: ")
    
    output_dir = "subtitles"

    # Use proxy from config file
    proxies = PROXY

    channel_id = get_channel_id(channel_url, proxies=proxies)
    if not channel_id:
        print("Failed to get channel ID")
        return

    channel_details = get_channel_details(channel_id)
    if channel_details:
        print("\nChannel information:")
        print(f"Title: {channel_details['title']}")
        print(f"Description: {channel_details['description'][:100]}...")
        print(f"Subscriber count: {channel_details['subscriber_count']}")
        print(f"Video count: {channel_details['video_count']}")
        print(f"Total view count: {channel_details['view_count']}")
    else:
        print("Unable to get channel details")
        return

    # Automatically confirm download, remove user confirmation step
    print("\nAutomatically confirming subtitle download for this channel.")
    get_and_process_videos(channel_id, output_dir, proxies=proxies)

if __name__ == "__main__":
    main()

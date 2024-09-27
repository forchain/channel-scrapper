# YouTube Channel Subtitle Downloader

This Python program allows you to input a YouTube channel address and download subtitles for all videos in that channel.

[中文版README](README_CN.md)

## Features

- Retrieve all video IDs from the input YouTube channel URL
- Download subtitles for each video (if available)
- Save subtitles as text files, one file per video

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Obtain a YouTube API key:
   a. Visit [Google Developers Console](https://console.developers.google.com/)
   b. Create a new project or select an existing one
   c. In the left menu, click "APIs & Services" > "Library"
   d. Search for and enable "YouTube Data API v3"
   e. In the left menu, click "Credentials"
   f. Click "Create Credentials" > "API key"
   g. Copy the generated API key

4. Copy `config.example.py` to `config.py` and fill in your YouTube API key:
   ```python
   API_KEY = "your_api_key_here"
   ```

## Usage

1. Run the `main.py` file:

   ```
   python main.py
   ```

2. If a default channel is not set in `config.py`, you will be prompted to enter a YouTube channel URL.
3. The program will start downloading subtitles and save them in the `subtitles` directory.

## Notes

- You need a valid YouTube API key to use this program.
- Be aware of the YouTube API usage quota limits.
- Some videos may not have subtitles or subtitles may not be available; the program will skip these videos.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
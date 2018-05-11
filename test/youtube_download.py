from os.path import join, dirname
from dotenv import load_dotenv
from googleapiclient.discovery import build
import urllib
from oauth2client.tools import argparser
from pytube import YouTube
import ssl

import os

ssl._create_default_https_context = ssl._create_unverified_context
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("DEVELOPER_KEY")

YOUTUBE_API_SERVICE_NAME = os.environ.get("YOUTUBE_API_SERVICE_NAME")
YOUTUBE_API_VERSION = os.environ.get("YOUTUBE_API_VERSION")


search_list = []
video_name = []
def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=DEVELOPER_KEY)


    search_response = youtube.search().list(
        q=options.q,
        part="id, snippet",
        maxResults=options.max_results
    ).execute()

    videos = []


    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
            video_name.append(search_result["snippet"]["title"])
            search_list.append(search_result["id"]["videoId"])

    print("Videos:\n", "\n".join(videos), "\n")
    print(search_list)


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=1)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except:
        print('クソ！')


for ID in search_list:
    query = 'https://www.youtube.com/watch?v=' + ID
    yt = YouTube(query)
    yt.streams.filter(subtype='mp4').first().download("./videos")




dl_file = os.listdir(path='./videos')
for file in dl_file:

    result_file = file.replace("　", "")
    os.rename("./videos/" + file, "./videos/" + result_file)
    print(result_file)



from os.path import join, dirname
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.tools import argparser
from pytube import YouTube
import ssl
import re
import os

ssl._create_default_https_context = ssl._create_unverified_context
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("DEVELOPER_KEY")

YOUTUBE_API_SERVICE_NAME = os.environ.get("YOUTUBE_API_SERVICE_NAME")
YOUTUBE_API_VERSION = os.environ.get("YOUTUBE_API_VERSION")


class YoutubeDownloader:

    def __init__(self):

        # 動画のIDを保存
        self.search_list = []

        # 動画の名前を保存
        self.video_name = []

        # 動画の名前とID両方保存
        self.videos = []

    # youtubeの動画を検索（キーワード+件数）
    def youtube_search(self, options):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=options.q,
            part="id, snippet",
            maxResults=options.max_results
        ).execute()
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
                self.video_name.append(search_result["snippet"]["title"])
                self.search_list.append(search_result["id"]["videoId"])

        print("Videos:\n", "\n".join(self.videos), "\n")
        print(self.search_list)

    def youtube_download(self):
        for ID in self.search_list:
            query = 'https://www.youtube.com/watch?v=' + ID
            yt = YouTube(query)
            title = re.sub('　', ' ', yt.title)
            title = re.sub('/', '', title)
            check = title+'.mp4' in os.listdir('./videos')
            print(yt.title)
            if check:
                print('同じのあった！')
                continue
            print('Download中..')
            if not os.path.isdir("./videos"):
                os.mkdir('./videos')
            yt.streams.filter(subtype='mp4').first().download("./videos", title)


if __name__ == "__main__":


    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=1)
    args = argparser.parse_args()


    you = YoutubeDownloader()
    try:
        you.youtube_search(args)
    except:
        print('クソ！')

    you.youtube_download()






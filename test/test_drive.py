"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth=GoogleAuth()
gauth.CommandLineAuth()
drive=GoogleDrive(gauth)
file=drive.CreateFile()
file.SetContentFile('tes.txt')
file.Upload()
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from os.path import join, dirname
from dotenv import load_dotenv

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

drive_img = os.environ.get('drive_img')
drive_video_fate = os.environ.get('drive_video_fate')


def drive_videos_upload():

    for video_file in os.listdir(path = './videos'):

        file = drive.CreateFile(
            {
                'title' : video_file,
                'mimeType' : 'video/mp4',
                'parents' : [{'kind' : 'drive#fileLink', 'id' : drive_video_fate}]
            }
        )
        file.SetContentFile('./videos/' + video_file)
        file.Upload()


def drive_img_upload():

    for img_file in os.listdir(path = './img'):

        file = drive.CreateFile(
            {
                'title' : img_file,
                'mimeType' : 'image/png',
                'parents' : [{'kind' : 'drive#fileLink', 'id' : drive_img}]
            }
        )
        file.SetContentFile('./img/' + img_file)


def drive_makefolder(dir):

    file_metadata = {
        'name' : dir,
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = file_metadata.files().create(
        body = file_metadata,
        fields = 'id').execute()


if __name__ == "__main__":

    for dir in os.listdir(path = './img'):
        try:
            drive_makefolder(dir)
        except:
            print(dir)










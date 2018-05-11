"""
videosディレクトリにあるvideoを読み込んで,一定フレームごと.pngに切り出します.
"""


import os
import cv2

def img_from_video(cat_span, file_dir, image_dir):
    # 読み込んだビデオを画像に変換
    all_frame = 0
    save_frame = 0
    image_file = 'img_%s.png'

    # videoを読み込む
    cap = cv2.VideoCapture(file_dir)
    while cap.isOpened():

        ret, frame = cap.read()
        # 動画の色をグレーにした
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if all_frame % cat_span == 0:

            # 動画を切り出し
            cv2.imwrite(image_dir + image_file % str(save_frame).zfill(6), frame)

            print('Save', image_file % str(save_frame).zfill(6))
            save_frame += 1
        #cv2.imshow('frame', gray)
        all_frame += 1

        # 全フレームをカウントしたらbreak
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == all_frame:
            print(all_frame)
            # 動画をリフレッシュ
            cap.release()
            break




if __name__ == '__main__':

    file_list = os.listdir('./videos/')

    cat_span = 5000

    for file in file_list:

        image_dir = './img/' + file + '/'
        file_dir = './videos/' + file
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        img_from_video(cat_span, file_dir, image_dir)







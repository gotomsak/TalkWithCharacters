import os
import cv2


class VideoImg:

    def __init__(self, cat_span, image_dir, video_file):
        self.cat_span = cat_span
        self.image_dir = image_dir
        self.video_file = video_file

    def img_from_video(self):
        save_name = "result_%s.png"
        all_frame = 0
        save_frame = 0
        cap = cv2.VideoCapture(self.video_file)

        while cap.isOpened():

            ret, frame = cap.read()

            if all_frame % self.cat_span == 0:
                # 動画を切り出し
                cv2.imwrite(self.image_dir + save_name % str(save_frame).zfill(6), frame)

                print('Save', save_name % str(save_frame).zfill(6))
                save_frame += 1

            all_frame += 1

            # 全フレームをカウントしたらbreak
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == all_frame:
                print(all_frame)

                # 動画をリフレッシュ
                cap.release()
                break


class VideoImgMask(VideoImg):

    def __init__(self, cat_span, image_dir, video_file, mask, mask_name):
        super().__init__(cat_span, image_dir, video_file)
        self.mask = mask
        self.mask_name = mask_name

    def img_mask(self):
        save_name = "result_mask_%s.png"
        save_name1 = "result_mask_name_%s.png"
        cap = cv2.VideoCapture(self.video_file)
        all_frame = 0
        save_frame = 0
        while cap.isOpened():

            ret, frame = cap.read()

            if all_frame % self.cat_span == 0:

                # マスク画像の読み込み
                mask = cv2.imread(self.mask, 0)
                mask_name = cv2.imread(self.mask_name, 0)
                try:
                    # マスク処理
                    img = cv2.bitwise_and(frame, frame, mask=mask)
                    img1 = cv2.bitwise_and(frame, frame, mask=mask_name)

                    # 動画を切り出し
                    cv2.imwrite(image_dir + save_name % str(save_frame).zfill(6), img)
                    cv2.imwrite(image_dir + save_name1 % str(save_frame).zfill(6), img1)
                    print('Save', save_name % str(save_frame).zfill(6))
                    print('Save', save_name1 % str(save_frame).zfill(6))
                except:
                    print(".DS_store滅べ")

                save_frame += 1

            all_frame += 1
            # 全フレームをカウントしたらbreak
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == all_frame:
                print(all_frame)
                # 動画をリフレッシュ
                cap.release()
                break


class Binary(VideoImgMask):

    def binary_mask(self):
        cap = cv2.VideoCapture(self.video_file)
        all_frame = 0
        save_frame = 0

        # 画像ファイルの名前部
        name_file = 'thresh_name_%s.png'

        # 画像ファイルのセリフ部
        conversation_file = 'thresh_conversation_%s.png'
        while cap.isOpened():

            ret, frame = cap.read()

            if all_frame % cat_span == 0:

                # マスク画像の読み込み
                mask = cv2.imread(self.mask, 0)
                mask_name = cv2.imread(self.mask_name, 0)

                try:
                    # マスク処理
                    img = cv2.bitwise_and(frame, frame, mask=mask)
                    img1 = cv2.bitwise_and(frame, frame, mask=mask_name)

                    # グレースケール化
                    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

                    # 画像をそのまま2値化
                    ret, thresh_name = cv2.threshold(img1, 100, 255, cv2.THRESH_BINARY)

                    # 画像をグレースケールで2値化
                    ret, thresh_conversation = cv2.threshold(img_gray, 170, 255, cv2.THRESH_BINARY)

                    # 画像を保存
                    cv2.imwrite(image_dir + name_file % str(save_frame).zfill(6), thresh_name)
                    cv2.imwrite(image_dir + conversation_file % str(save_frame).zfill(6), thresh_conversation)

                    print('Save', image_dir + name_file % str(save_frame).zfill(6))
                    print('Save', image_dir + conversation_file % str(save_frame).zfill(6))

                except:
                    print(".DS_store滅べ")

                save_frame += 1

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


    mask = './img/mask.png'
    mask_name = './img/mask_name.png'
    for file in file_list:

        image_dir = './img/' + file + '/'
        video_file = './videos/' + file
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        video_img = Binary(cat_span, image_dir, video_file, mask, mask_name)
        video_img.binary_mask()


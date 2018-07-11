import os
import cv2


class VideoImg:

    save_frame = 0
    all_frame = 0

    def __init__(self, cat_span, image_dir, video_file):

        self.cat_span = cat_span
        self.image_dir = image_dir
        self.video_file = video_file

    # 動画を切り取ったものを保存
    def catting(self, frame, save_name):
        save_name = save_name % str(self.save_frame).zfill(6)
        cv2.imwrite(self.image_dir + save_name, frame)
        return save_name

    # 動画を読み込み
    def capture(self):
        return cv2.VideoCapture(self.video_file)

    def img_from_video(self):
        save_name = "result_%s.png"

        cap = self.capture()
        while cap.isOpened():

            ret, frame = cap.read()

            if self.all_frame % self.cat_span == 0:

                # 動画を切り出し
                cat = self.catting(frame, save_name)

                print('Save', cat)
                self.save_frame += 1

            self.all_frame += 1

            # 全フレームをカウントしたらbreak
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == self.all_frame:
                print(self.all_frame)

                # 動画をリフレッシュ
                cap.release()
                break


class VideoImgMask(VideoImg):

    def __init__(self, cat_span, image_dir, video_file, mask, mask_name):
        super().__init__(cat_span, image_dir, video_file)


        # マスク画像の読み込み
        self.mask = cv2.imread(mask, 0)
        self.mask_name = cv2.imread(mask_name, 0)


    def img_mask(self):
        save_name = "mask_conversation_%s.png"
        save_name1 = "mask_name_%s.png"

        cap = self.capture()

        while cap.isOpened():

            ret, frame = cap.read()

            if self.all_frame % self.cat_span == 0:

                try:
                    # マスク処理
                    img = cv2.bitwise_and(frame, frame, mask=self.mask)
                    img1 = cv2.bitwise_and(frame, frame, mask=self.mask_name)

                   # 動画を切り出し
                    result_name = self.catting(img, save_name)
                    result_conversation = self.catting(img1, save_name1)

                    print('Save', result_name)
                    print('Save', result_conversation)

                except:

                    print(".DS_store滅べ")

                    self.save_frame += 1

            self.all_frame += 1
            # 全フレームをカウントしたらbreak
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == self.all_frame:
                print(self.all_frame)
                # 動画をリフレッシュ
                cap.release()
                break


class Binary(VideoImgMask):
    def __init__(self, cat_span, image_dir, video_file, mask, mask_name,
                 thresh_start_n, thresh_end_n, thresh_start_c, thresh_end_c):

        super().__init__(cat_span, image_dir, video_file, mask, mask_name)

        self.thresh_start_n = thresh_start_n
        self.thresh_end_n = thresh_end_n
        self.thresh_start_c = thresh_start_c
        self.thresh_end_c = thresh_end_c

    def binarization(self, img, thresh_start, thresh_end):
        return cv2.threshold(img, thresh_start, thresh_end, cv2.THRESH_BINARY)

    def binary_mask(self):
        cap = cv2.VideoCapture(self.video_file)

        # 画像ファイルの名前部
        save_name = 'thresh_name_%s.png'

        # 画像ファイルのセリフ部
        save_conversation = 'thresh_conversation_%s.png'

        while cap.isOpened():

            ret, frame = cap.read()

            if self.all_frame % cat_span == 0:


                try:
                    # マスク処理
                    img = cv2.bitwise_and(frame, frame, mask=self.mask)
                    img1 = cv2.bitwise_and(frame, frame, mask=self.mask_name)

                    # グレースケール化
                    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

                    # 画像をそのまま2値化
                    ret, thresh_name = self.binarization(img1, self.thresh_start_n, self.thresh_end_n)
                    # 画像をグレースケールで2値化
                    ret, thresh_conversation = self.binarization(img_gray, self.thresh_start_c, self.thresh_end_c)

                    # 画像を保存
                    result_name = self.catting(thresh_name, save_name)
                    result_conversation = self.catting(thresh_conversation, save_conversation)

                    print('Save', result_name)
                    print('Save', result_conversation)

                except:
                    print(".DS_store滅べ")

                self.save_frame += 1

            self.all_frame += 1
            # 全フレームをカウントしたらbreak
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == self.all_frame:
                print(self.all_frame)
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
        video_img = Binary(cat_span, image_dir, video_file, mask, mask_name, 100, 255, 170, 255)
        video_img.binary_mask()


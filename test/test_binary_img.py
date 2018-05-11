import cv2
import os

# 2値化する関数(画像パス,保存先のパス,保存する画像番号)
def binary_img(img_path, binary_path, img_num):

    # 画像ファイルの名前部
    name_file = 'thresh_name_%s.png'

    # 画像ファイルのセリフ部
    conversation_file = 'thresh_conversation_%s.png'

    # 画像を読み込んでグレースケールに変換
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 画像をそのまま2値化
    ret, thresh_name = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    # 画像をグレースケールで2値化
    ret, thresh_conversation = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)


    # 画像を保存
    cv2.imwrite(binary_path + name_file % str(img_num).zfill(6), thresh_name)
    cv2.imwrite(binary_path + conversation_file % str(img_num).zfill(6), thresh_conversation)







if __name__ == "__main__":

    dir_path = "./img/【FateEXTELLA】赤セイバー・ストーリーpart18 【プレイ動画】.mp4_mask"
    binary_path = dir_path + "_binary/"
    files_path = os.listdir(dir_path)

    try:
        os.mkdir(binary_path)
    except:
        print('そのフォルダはすでに存在します.')

    for i in range(len(files_path)):
        binary_img(dir_path + '/' + files_path[i], binary_path, i)


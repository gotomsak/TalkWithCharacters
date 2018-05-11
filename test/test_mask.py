import cv2
import numpy as np
import os






def mask_processing(imgpath, maskpath, result_dir, img_num):


    save_file = 'result_%s.png'

    # 入力画像の読み込み
    img = cv2.imread(imgpath)
    print(imgpath)
    # マスク画像の読み込み
    mask = cv2.imread(maskpath, 0)


    try:
        # マスク処理
        img2 = cv2.bitwise_and(img, img, mask=mask)

        print(result_dir)
        # 出力
        cv2.imwrite(result_dir + '/' + save_file % str(img_num).zfill(6), img2)

    except:
        print(".DS_store滅べ")





if __name__ == '__main__':
    path = './img/'
    dir_name = '【FateEXTELLA】赤セイバー・ストーリーpart18 【プレイ動画】.mp4'
    #dir_name = 'test'
    maskpath = './img/mask.png'

    listdir = os.listdir(path + dir_name)
    print(listdir)
    result = []
    result_dir = path+dir_name+'_mask'

    try:
        os.mkdir(result_dir)
    except:
        print('そのフォルダはすでに存在します.')

    for i in range(len(listdir)):

        mask_processing(path + dir_name + '/' + listdir[i], maskpath, result_dir, i)




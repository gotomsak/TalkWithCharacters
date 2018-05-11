import pyocr
import pyocr.builders

from PIL import Image

import glob
import os


def image_from_text(name_img, conversation_img, character_name, save_character):

    tools = pyocr.get_available_tools()
    tool = tools[0]

    print(name_img)
    print(conversation_img)

    name_text = tool.image_to_string(Image.open(name_img), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=1))

    for i in range(len(name_text)):
        ne = 'ネ' in name_text
        ro = '口' in name_text
        ne1 = name_text.rfind('ネ')
        ro1 = name_text.rfind('口')
        print(ne,ro,ne1,ro1)
        #print(name_text[i])

        if name_text[i] == 'ネ' and name_text[i+1] == 'ロ':
            print('true')
    for i in character_name:
        print(i)
        if i in name_text:
            conversation_text = tool.image_to_string(Image.open(conversation_img), lang="jpn",
                                                     builder=pyocr.builders.TextBuilder(tesseract_layout=1))

            f = open(save_character + '.txt', 'a')

            f.write(conversation_text + "\n")

            f.close()

    #print(name_text.find())


if __name__ == "__main__":

    dir_path = './img/【FateEXTELLA】赤セイバー・ストーリーpart18 【プレイ動画】.mp4_mask_binary'
    dir_files = os.listdir(dir_path)
    save_character = 'nero'
    character_name = ['ネロ', 'ネ口']

    file_name = [os.path.basename(r) for r in glob.glob(dir_path + '/thresh_name_*')]
    #file_conversation = [os.path.basename(r) for r in glob.glob(dir_path + '/thresh_conversation_*')]


    for i in range(len(file_name)):

        image_from_text(dir_path + '/' + 'thresh_name_' + "{0:06d}.png".format(i),
                        dir_path + '/' + 'thresh_conversation_' + "{0:06d}.png".format(i),
                        character_name, save_character)



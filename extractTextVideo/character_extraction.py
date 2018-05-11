import pyocr
import pyocr.builders

from PIL import Image

import glob
import os
import re


class TesseractText:

    def __init__(self, name_img, conversation_img, character_name):
        self.name_img = name_img
        self.conversation_img = conversation_img
        self.character_name = character_name

    def image_from_text(self):

        tools = pyocr.get_available_tools()
        tool = tools[0]

        print(self.name_img)
        print(self.conversation_img)

        name_text = tool.image_to_string(Image.open(self.name_img), lang="jpn",
                                         builder=pyocr.builders.TextBuilder(tesseract_layout=1))
        for character in self.character_name:
            check = character in name_text
            if check:
                conversation_text = tool.image_to_string(Image.open(self.conversation_img), lang="jpn",
                                                         builder=pyocr.builders.TextBuilder(tesseract_layout=1))
                conversation_text = re.sub('て`', 'で', conversation_text)
                conversation_text = re.sub('`', '、', conversation_text)
                conversation_text = re.sub('て"', 'で', conversation_text)
                conversation_text = re.sub('なのて', 'なので', conversation_text)
                conversation_text = re.sub('なつた', 'なった', conversation_text)
                conversation_text = re.sub('喚ぴ', '喚び', conversation_text)

                f = open(self.character_name[0] + '.txt', 'a')

                f.write(conversation_text + "\n\n")

                f.close()

                break


if __name__ == "__main__":
    dir_path = './img'
    name = 'thresh_name_*'
    character_name_list = ['ネロ', 'ネ口']
    save_name = 'ネロ'
    for dir_name in os.listdir(dir_path):
        file_name = [os.path.basename(r) for r in glob.glob(dir_path + '/' + dir_name + '/thresh_name_*')]
        for i in range(len(file_name)):
                ts_img = TesseractText(dir_path + '/' + dir_name + '/' + 'thresh_name_' + "{0:06d}.png".format(i),
                                       dir_path + '/' + dir_name + '/' + 'thresh_conversation_' + "{0:06d}.png".format(i),
                                       character_name_list)
                ts_img.image_from_text()
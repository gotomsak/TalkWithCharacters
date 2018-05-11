import pyocr
import pyocr.builders

from PIL import Image

import glob
import os


dir_path = './img/【FateEXTELLA】赤セイバー・ストーリーpart18 【プレイ動画】.mp4_mask_binary'

tools = pyocr.get_available_tools()
tool = tools[0]

conversation_text = tool.image_to_string(Image.open(dir_path+'/thresh_name_000008.png'), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=1))
print(conversation_text)
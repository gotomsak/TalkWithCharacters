from PIL import Image
import sys
import pyocr
import pyocr.builders
import matplotlib.pyplot as plt

tools = pyocr.get_available_tools()
tools
# OCRツールをインストールされているか確認
if len(tools) == 0:
  print("No OCR tool found")
  sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

lang = langs[0]
print("Will use lang '%s'" % (lang))

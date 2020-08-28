#!/bin/python3

import sys, os
from PIL import ImageFont, Image, ImageDraw, ImageOps
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import (QIcon, QPixmap)

CLEAR = "cls" if os.name == "nt" else "clear"

class ShowApp(QWidget):
    def __init__(self, file_image):
        super().__init__()
        self.file = file_image
        self.InitUI()
        self.stop = 0
    def InitUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Meme Generator")
        self.label = QLabel(self)
        pixmap = QPixmap.fromImage(self.file)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.setFixedSize(self.size())
        self.show()
    def closeEvent(self, event):
        self.stop = 1

class Click(QWidget):
    def __init__(self, file_image):
        super().__init__()
        self.file = file_image
        self.setMouseTracking(True)
        self.InitUI()
        self.mouseX, self.mouseY = 0, 0
        self.p = 1
        self.stop = 0
    def InitUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Meme Generator")
        self.label = QLabel(self)
        pixmap = QPixmap.fromImage(self.file)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.setFixedSize(self.size())
        self.show()
    def mouseReleaseEvent(self, event):
        if self.p:
            self.mouseX, self.mouseY = float(event.x()), float(event.y())
            self.stop = 1
            self.close()
        self.p = 0

name = input("[+] Enter image file: ")
pil_image = Image.open(name)
pil_image = pil_image.convert('RGB')
tmp_image = pil_image
while 1:
    os.system(CLEAR)
    choose = input("1. White band with text\n2. Text at click positions\n3. Previsualization\n4. Restore image\n5. Save meme\n6. Abandon\n[+] Choose into the list: ")
    if choose == "6":
        exit()
    elif choose == "5":
        os.system(CLEAR)
        new_name = input("[+] Choose a name for output file: ")
        tmp_image.save(f"{new_name}.png")
        input(f"[+] Image saved as '{new_name}.png'\nENTER to exit...")
        exit()
    elif choose == "4":
        tmp_image = pil_image
    elif choose == "3":
        use_image = ImageQt(tmp_image)
        app = QApplication(sys.argv)
        ex = ShowApp(use_image)
        app.exec_()
        while not ex.__dict__["stop"]:
            pass
    elif choose == "2":
        os.system(CLEAR)
        use_image = ImageQt(tmp_image)
        app = QApplication(sys.argv)
        ex = Click(use_image)
        app.exec_()
        while not ex.__dict__["stop"]:
            pass
        pos_x, pos_y = ex.__dict__["mouseX"], ex.__dict__["mouseY"]
        font_choose = input("[+] Path to ttf font file: ")
        font_size = input("[+] Text size (default: 15): ")
        font_size = font_size if font_size != "" else "15"
        while not font_size.isnumeric():
            os.system(CLEAR)
            print("[!] Error: Please enter number...")
            font_size = input(f"\n[+] Path to ttf font file: {font_choose}\n[+] Text size (default: 15): ")
            font_size = font_size if font_size != "" else "15"
        text = input("[+] Text to show: ")
        font = ImageFont.truetype(font_choose, int(font_size))
        draw = ImageDraw.Draw(tmp_image)
        draw.text((pos_x, pos_y), text, (0, 0, 0), font=font)
    elif choose == "1":
        os.system(CLEAR)
        band_size = input("[+] White band height (default: 30): ")
        band_size = band_size if band_size != "" else "30"
        while not band_size.isnumeric():
            os.system(CLEAR)
            band_size = input("[!] Error: Please enter number...\n[+] White band height (default: 30): ")
            band_size = band_size if band_size != "" else "30"
        new_image = Image.new('RGB', (tmp_image.width, tmp_image.height + int(band_size)), (255, 255, 255))
        for y in range(pil_image.height):
            for x in range(pil_image.width):
                new_image.putpixel((x, y + int(band_size)), pil_image.getpixel((x, y)))
        font_choose = input("[+] Path to ttf font file: ")
        font_size = input("[+] Text size (default: 15): ")
        font_size = font_size if font_size != "" else "15"
        while not font_size.isnumeric():
            os.system(CLEAR)
            print("[!] Error: Please enter number...")
            font_size = input(f"\n[+] White band height (default: 30): {band_size}\n[+] Path to ttf font file: {font_choose}\n[+] Text size (default: 15): ")
            font_size = font_size if font_size != "" else "15"
        text = input("[+] Text to show: ")
        font = ImageFont.truetype(font_choose, int(font_size))
        font_width = font.font.getsize(text)[0][0]
        draw = ImageDraw.Draw(new_image)
        draw.text(((new_image.width / 2) - (font_width / 2), 1), text, (0, 0, 0), font=font)
        tmp_image = new_image
    else:
        input("\n[!] Error: Please choose into the list\nENTER to retry...")

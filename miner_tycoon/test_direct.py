#!/usr/bin/env python3
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, '/workspace/miner_tycoon')
from create_cartoons import draw_miner, SPRITE_SIZE

# 直接在一个图片上画，背景用浅蓝色
img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (200, 200, 255, 255))
draw = ImageDraw.Draw(img)

# 先画一个红色参考框
draw.rectangle([0, 0, SPRITE_SIZE-1, SPRITE_SIZE-1], outline='red')

# 调用draw_miner
draw_miner(img, 0, 0, '#FFD700', '#4169E1', 'idle')

# 保存
img.save('/workspace/miner_tycoon/test_direct.png')
print("Saved test_direct.png")

# 扫描
print("\nNon-transparent pixels:")
for y in range(0, 128, 2):
    has_pixel = False
    line = ""
    for x in range(0, 128, 4):
        p = img.getpixel((x, y))
        if p[3] > 100 and not (p[0] == 200 and p[1] == 200 and p[2] == 255):
            has_pixel = True
            if p[0] > 200 and p[1] > 200 and p[2] < 100:
                line += "Y"
            elif p[0] > 200 and p[1] > 180 and p[2] > 150:
                line += "S"
            elif p[2] > 150 and p[0] < 100:
                line += "B"
            else:
                line += "."
        else:
            line += " "
    if has_pixel:
        print(f"y={y:3d}: {line}")

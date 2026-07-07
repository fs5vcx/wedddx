#!/usr/bin/env python3
from PIL import Image

img = Image.open('/workspace/miner_tycoon/frontend/assets/sprites.png')

# 扫描第一个精灵的所有不透明像素
print("First sprite non-transparent pixels:")
for y in range(0, 128):
    has_pixel = False
    line = ""
    for x in range(0, 128, 4):
        p = img.getpixel((x, y))
        if p[3] > 100:
            has_pixel = True
            # 简单的颜色描述
            if p[0] > 200 and p[1] > 200 and p[2] < 100:
                line += "Y"  # Yellow
            elif p[0] > 200 and p[1] > 180 and p[2] > 150:
                line += "S"  # Skin
            elif p[2] > 150 and p[0] < 100:
                line += "B"  # Blue
            elif p[0] > 200 and p[1] < 100 and p[2] < 100:
                line += "R"  # Red
            elif p[0] > 200 and p[1] > 200 and p[2] > 200:
                line += "W"  # White
            else:
                line += "."
        else:
            line += " "
    if has_pixel:
        print(f"y={y:3d}: {line}")

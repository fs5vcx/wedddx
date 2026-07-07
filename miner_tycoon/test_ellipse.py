#!/usr/bin/env python3
from PIL import Image, ImageDraw

img = Image.new('RGBA', (128, 128), (200, 200, 255, 255))
draw = ImageDraw.Draw(img)

# 画一个测试椭圆
skin = (255, 218, 185)
skin_dark = (210, 170, 120)

cx = 64
cy = 48
r = 26

print(f"Drawing ellipse at ({cx}, {cy}) with r={r}")
print(f"Bounding box: [{cx-r}, {cy-r}, {cx+r}, {cy+r}]")

draw.ellipse([cx - r, cy - r, cx + r, cy + r],
             fill=skin, outline=skin_dark, width=2)

img.save('/workspace/miner_tycoon/test_ellipse.png')
print("Saved test_ellipse.png")

# 检查
for y in range(0, 128, 2):
    has_pixel = False
    line = ""
    for x in range(0, 128, 4):
        p = img.getpixel((x, y))
        if p[0] > 200 and p[1] > 180 and p[2] > 150 and p[3] > 200:
            has_pixel = True
            line += "S"
        elif p[3] > 100 and not (p[0] == 200 and p[1] == 200 and p[2] == 255):
            has_pixel = True
            line += "."
        else:
            line += " "
    if has_pixel:
        print(f"y={y:3d}: {line}")

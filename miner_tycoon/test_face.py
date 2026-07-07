#!/usr/bin/env python3
from PIL import Image, ImageDraw
import math

SPRITE_SIZE = 128

def lighten(hex_color, amount):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return (r, g, b)

def darken(hex_color, amount):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = max(0, r - amount)
    g = max(0, g - amount)
    b = max(0, b - amount)
    return (r, g, b)

def hex_to_rgb(hex_color):
    return (int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16))

img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx = SPRITE_SIZE // 2
cy = SPRITE_SIZE * 0.55
head_r = 33
head_y = cy - 35 * 1.1

skin = (255, 218, 185)
skin_dark = (222, 184, 135)
skin_shadow = (210, 170, 130)

print(f"head_cy={head_y}, head_r={head_r}")
print(f"skin color: {skin}")

# 直接在主图上画脸
for i in range(int(head_r*2)):
    ratio = i / (head_r*2)
    r = int(skin[0] + (skin_shadow[0] - skin[0]) * ratio * 0.5)
    g = int(skin[1] + (skin_shadow[1] - skin[1]) * ratio * 0.5)
    b = int(skin[2] + (skin_shadow[2] - skin[2]) * ratio * 0.5)
    y_from_center = i - head_r
    if abs(y_from_center) < head_r:
        w = 2 * math.sqrt(head_r * head_r - y_from_center * y_from_center)
        x1 = cx - w / 2
        x2 = cx + w / 2
        y_pos = head_y - head_r + i
        draw.line([(x1, y_pos), (x2, y_pos)], fill=(r, g, b))
        if i == 0:
            print(f"First line: y={y_pos}, x1={x1}, x2={x2}, color=({r},{g},{b})")

# 轮廓
draw.ellipse([cx - head_r, head_y - head_r, cx + head_r, head_y + head_r],
             outline=skin_dark, width=2)

# 眼睛
eye_y = head_y - 2
draw.ellipse([cx - 16, eye_y - 7, cx - 5, eye_y + 7], fill='white', outline=(100, 100, 100), width=1)
draw.ellipse([cx + 5, eye_y - 7, cx + 16, eye_y + 7], fill='white', outline=(100, 100, 100), width=1)
draw.ellipse([cx - 13, eye_y - 4, cx - 7, eye_y + 4], fill=(50, 50, 80))
draw.ellipse([cx + 7, eye_y - 4, cx + 13, eye_y + 4], fill=(50, 50, 80))

# 嘴巴
draw.arc([cx - 6, head_y + 8, cx + 6, head_y + 16], 0, 180, 
         fill=(180, 100, 100), width=2)

img.save('/workspace/miner_tycoon/test_face.png')
print("Saved test_face.png")

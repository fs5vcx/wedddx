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

img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (200, 200, 255, 255))  # 浅蓝色背景
draw = ImageDraw.Draw(img)

cx = SPRITE_SIZE // 2
x = 0
y = 0

helmet_color = '#FFD700'
head_r = 28
head_cy = y + 45

hc = hex_to_rgb(helmet_color)
hc_light = lighten(helmet_color, 25)
hc_dark = darken(helmet_color, 30)

print(f"hc_light: {hc_light}")
print(f"hc_dark: {hc_dark}")

helmet_bottom_y = head_cy - 8  # 头盔底部在眼睛上方
helmet_top_y = head_cy - head_r - 10
helmet_h = helmet_bottom_y - helmet_top_y

print(f"helmet_top_y: {helmet_top_y}")
print(f"helmet_bottom_y: {helmet_bottom_y}")
print(f"helmet_h: {helmet_h}")

# 直接用rectangle画一个头盔，看看颜色对不对
draw.rectangle([cx - 30, helmet_top_y, cx + 30, helmet_bottom_y], fill=hc_light, outline='black')

# 脸部
skin = (255, 218, 185)
for i in range(int(head_r * 2)):
    y_pos = head_cy - head_r + i
    y_from_center = i - head_r
    if abs(y_from_center) < head_r:
        w = 2 * math.sqrt(head_r * head_r - y_from_center * y_from_center)
        draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], fill=skin)

# 眼睛
eye_y = head_cy - 3
draw.ellipse([cx - 15, eye_y - 6, cx - 5, eye_y + 6], fill='white', outline=(80, 80, 80))
draw.ellipse([cx + 5, eye_y - 6, cx + 15, eye_y + 6], fill='white', outline=(80, 80, 80))

# 标记头盔区域
draw.rectangle([cx - 35, helmet_top_y - 2, cx + 35, helmet_bottom_y + 2], outline='red', width=1)

img.save('/workspace/miner_tycoon/test_helmet.png')
print("Saved test_helmet.png")

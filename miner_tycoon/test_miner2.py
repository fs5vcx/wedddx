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

img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (200, 200, 255, 255))
draw = ImageDraw.Draw(img)

cx = SPRITE_SIZE // 2
x = 0
y = 0

helmet_color = '#FFD700'
body_color = '#4169E1'

head_cy = y + 48
head_r = 26

skin = (255, 218, 185)
skin_dark = (210, 170, 120)

hc = hex_to_rgb(helmet_color)
hc_light = lighten(helmet_color, 20)
hc_dark = darken(helmet_color, 25)

print(f"hc: {hc}")
print(f"hc_light: {hc_light}")
print(f"hc_dark: {hc_dark}")

# 先画脸
draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
             fill=skin, outline=skin_dark, width=2)

# 画眼睛
eye_y = head_cy - 2
draw.ellipse([cx - 15, eye_y - 6, cx - 5, eye_y + 6], fill='white', outline=(70, 70, 70))
draw.ellipse([cx + 5, eye_y - 6, cx + 15, eye_y + 6], fill='white', outline=(70, 70, 70))

# 画头盔
helmet_bottom = head_cy - 10
helmet_arc_top = head_cy - head_r - 12
helmet_arc_h = helmet_bottom - helmet_arc_top

print(f"helmet_arc_top: {helmet_arc_top}")
print(f"helmet_bottom: {helmet_bottom}")
print(f"helmet_arc_h: {helmet_arc_h}")

# 画下半矩形 - 用红色边框标记
rect_top = helmet_arc_top + helmet_arc_h * 0.4
print(f"rect_top: {rect_top}")
print(f"rect coords: ({cx - head_r - 3}, {rect_top}) -> ({cx + head_r + 3}, {helmet_bottom})")

# 用半透明红色标记矩形区域
draw.rectangle([cx - head_r - 3, rect_top, cx + head_r + 3, helmet_bottom],
               fill=hc, outline='red', width=2)

# 画顶部弧形区域标记
arc_r = head_r + 3
print(f"arc_r: {arc_r}")
for i in range(int(arc_r * 0.7)):
    w = 2 * math.sqrt(arc_r * arc_r - i * i)
    y_pos = helmet_arc_top + i
    draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], fill='blue')

img.save('/workspace/miner_tycoon/test_miner2.png')
print("Saved test_miner2.png")

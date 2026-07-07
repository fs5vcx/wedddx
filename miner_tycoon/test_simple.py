#!/usr/bin/env python3
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, '/workspace/miner_tycoon')

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

def draw_miner_simple(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    
    head_cy = y + 48
    head_r = 26
    body_top = y + 74
    body_bottom = y + 108
    body_w = 42
    
    skin = (255, 218, 185)
    skin_dark = (210, 170, 120)
    
    bc = hex_to_rgb('#4169E1')
    bc_light = lighten('#4169E1', 15)
    bc_dark = darken('#4169E1', 25)
    
    # 身体
    body_h = body_bottom - body_top
    for i in range(body_h):
        ratio = i / body_h
        r = int(bc_light[0] + (bc_dark[0] - bc_light[0]) * ratio)
        g = int(bc_light[1] + (bc_dark[1] - bc_light[1]) * ratio)
        b = int(bc_light[2] + (bc_dark[2] - bc_light[2]) * ratio)
        w = body_w * (0.88 + ratio * 0.12)
        draw.line([(cx - w/2, body_top + i), (cx + w/2, body_top + i)], fill=(r, g, b))
    
    # 脸部 - 先画脸
    print(f"Drawing face at cy={head_cy}, r={head_r}")
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
                 fill=skin, outline=skin_dark, width=2)
    
    # 眼睛
    eye_y = head_cy - 2
    draw.ellipse([cx - 15, eye_y - 6, cx - 5, eye_y + 6], fill='white', outline=(70, 70, 70))
    draw.ellipse([cx + 5, eye_y - 6, cx + 15, eye_y + 6], fill='white', outline=(70, 70, 70))
    
    # 检查此时脸是否存在
    p = img.getpixel((cx, head_cy))
    print(f"Pixel at center after face: {p}")


img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (200, 200, 255, 255))
draw_miner_simple(img, 0, 0)

# 检查脸中心的像素
cx = 64
cy = 48
p = img.getpixel((cx, cy))
print(f"Final pixel at ({cx}, {cy}): {p}")

img.save('/workspace/miner_tycoon/test_simple.png')
print("Saved test_simple.png")

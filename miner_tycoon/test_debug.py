#!/usr/bin/env python3
from PIL import Image, ImageDraw
import math
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

def draw_miner_debug(img, x, y, helmet_color='#FFD700', body_color='#4169E1', pose='idle'):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    
    head_cy = y + 48
    head_r = 26
    body_top = y + 74
    body_bottom = y + 108
    body_w = 42
    
    skin = (255, 218, 185)
    skin_dark = (210, 170, 120)
    
    hc = hex_to_rgb(helmet_color)
    hc_light = lighten(helmet_color, 20)
    hc_dark = darken(helmet_color, 25)
    
    bc = hex_to_rgb(body_color)
    bc_light = lighten(body_color, 15)
    bc_dark = darken(body_color, 25)
    
    # 1. 阴影
    draw.ellipse([cx - 26, y + 112, cx + 26, y + 120], fill=(0, 0, 0, 45))
    
    # 2. 腿
    leg_top = body_bottom - 3
    draw.rectangle([cx - 15, leg_top, cx - 5, leg_top + 16], fill=bc_dark, outline=darken(body_color, 35))
    draw.rectangle([cx + 5, leg_top, cx + 15, leg_top + 16], fill=bc_dark, outline=darken(body_color, 35))
    draw.ellipse([cx - 17, leg_top + 13, cx - 3, leg_top + 21], fill=(70, 40, 25))
    draw.ellipse([cx + 3, leg_top + 13, cx + 17, leg_top + 21], fill=(70, 40, 25))
    
    # 3. 身体
    body_h = body_bottom - body_top
    for i in range(body_h):
        ratio = i / body_h
        r = int(bc_light[0] + (bc_dark[0] - bc_light[0]) * ratio)
        g = int(bc_light[1] + (bc_dark[1] - bc_light[1]) * ratio)
        b = int(bc_light[2] + (bc_dark[2] - bc_light[2]) * ratio)
        w = body_w * (0.88 + ratio * 0.12)
        draw.line([(cx - w/2, body_top + i), (cx + w/2, body_top + i)], fill=(r, g, b))
    
    draw.rounded_rectangle([cx - body_w/2, body_top, cx + body_w/2, body_bottom],
                           radius=9, outline=bc_dark, width=2)
    
    # 4. 腰带
    belt_y = body_top + 14
    draw.rectangle([cx - body_w/2, belt_y, cx + body_w/2, belt_y + 7], fill=hc)
    draw.rectangle([cx - 6, belt_y + 1, cx + 6, belt_y + 6], fill=(255, 215, 0), outline=hc_dark)
    
    # 检查点1：脸之前
    p1 = img.getpixel((cx, head_cy))
    print(f"Step 4 (after belt): face center pixel = {p1}")
    
    # 5. 脸部
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
                 fill=skin, outline=skin_dark, width=2)
    
    # 检查点2：脸之后
    p2 = img.getpixel((cx, head_cy))
    print(f"Step 5 (after face): face center pixel = {p2}")
    
    # 6. 脸部阴影
    for i in range(head_r):
        y_pos = head_cy + i
        alpha = int(30 * i / head_r)
        w = 2 * math.sqrt(head_r * head_r - i * i)
        draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], 
                  fill=(210, 170, 120, alpha))
    
    # 检查点3
    p3 = img.getpixel((cx, head_cy))
    print(f"Step 6 (after face shadow): face center pixel = {p3}")
    
    # 7. 腮红
    draw.ellipse([cx - 19, head_cy + 4, cx - 9, head_cy + 12], fill=(255, 160, 170, 160))
    draw.ellipse([cx + 9, head_cy + 4, cx + 19, head_cy + 12], fill=(255, 160, 170, 160))
    
    # 8. 眼睛
    eye_y = head_cy - 2
    draw.ellipse([cx - 15, eye_y - 6, cx - 5, eye_y + 6], fill='white', outline=(70, 70, 70))
    draw.ellipse([cx - 12, eye_y - 3, cx - 7, eye_y + 3], fill=(40, 40, 70))
    draw.ellipse([cx - 11, eye_y - 2, cx - 9, eye_y], fill='white')
    draw.ellipse([cx + 5, eye_y - 6, cx + 15, eye_y + 6], fill='white', outline=(70, 70, 70))
    draw.ellipse([cx + 7, eye_y - 3, cx + 12, eye_y + 3], fill=(40, 40, 70))
    draw.ellipse([cx + 8, eye_y - 2, cx + 10, eye_y], fill='white')
    
    # 9. 眉毛
    brow_color = (120, 70, 30)
    draw.arc([cx - 15, eye_y - 13, cx - 5, eye_y - 4], 200, 340, fill=brow_color, width=2)
    draw.arc([cx + 5, eye_y - 13, cx + 15, eye_y - 4], 200, 340, fill=brow_color, width=2)
    
    # 10. 嘴巴
    draw.arc([cx - 6, head_cy + 7, cx + 6, head_cy + 15], 0, 180, fill=(170, 80, 80), width=2)
    
    # 检查点4：头盔之前
    p4 = img.getpixel((cx, head_cy))
    print(f"Step 10 (before helmet): face center pixel = {p4}")
    
    # 11. 头盔
    helmet_bottom = head_cy - 10
    helmet_arc_top = head_cy - head_r - 12
    helmet_arc_h = helmet_bottom - helmet_arc_top
    
    rect_top = helmet_arc_top + helmet_arc_h * 0.4
    draw.rectangle([cx - head_r - 3, rect_top, cx + head_r + 3, helmet_bottom],
                   fill=hc)
    
    arc_r = head_r + 3
    for i in range(int(arc_r * 0.7)):
        w = 2 * math.sqrt(arc_r * arc_r - i * i)
        ratio = i / (arc_r * 0.7)
        r = int(hc_light[0] + (hc[0] - hc_light[0]) * ratio)
        g = int(hc_light[1] + (hc[1] - hc_light[1]) * ratio)
        b = int(hc_light[2] + (hc[2] - hc_light[2]) * ratio)
        y_pos = helmet_arc_top + i
        draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], fill=(r, g, b))
    
    draw.arc([cx - head_r - 4, helmet_arc_top - 2, cx + head_r + 4, helmet_bottom + 10],
             180, 360, fill=hc_dark, width=2)
    draw.line([cx - head_r - 4, helmet_bottom, cx + head_r + 4, helmet_bottom], 
              fill=hc_dark, width=2)
    
    # 检查点5：头盔之后
    p5 = img.getpixel((cx, head_cy))
    print(f"Step 11 (after helmet): face center pixel = {p5}")
    p5_top = img.getpixel((cx, helmet_arc_top + 5))
    print(f"  helmet top pixel (y={helmet_arc_top + 5}): {p5_top}")
    p5_mid = img.getpixel((cx, rect_top + 5))
    print(f"  helmet rect pixel (y={rect_top + 5}): {p5_mid}")
    
    # 12. 头灯
    lamp_y = helmet_arc_top + 18
    draw.ellipse([cx - 10, lamp_y - 5, cx + 10, lamp_y + 8], fill=(70, 70, 70), outline=(40, 40, 40))
    draw.ellipse([cx - 7, lamp_y - 2, cx + 7, lamp_y + 5], fill=(255, 255, 180))
    for i in range(3):
        alpha = 70 - i * 22
        r = 15 + i * 8
        draw.ellipse([cx - r, lamp_y - r + 3, cx + r, lamp_y + r + 3],
                     fill=(255, 255, 150, alpha))
    
    # 13. 头盔高光
    draw.arc([cx - 18, helmet_arc_top + 4, cx + 2, helmet_arc_top + 22], 200, 280, fill=hc_light, width=3)
    
    # 14. 手臂和镐子
    if pose == 'mining':
        arm_x = cx + 18
        arm_y = body_top + 6
        draw.line([(arm_x, arm_y), (arm_x + 22, arm_y - 22)], fill=skin, width=7)
        draw.line([(arm_x, arm_y), (arm_x + 22, arm_y - 22)], fill=skin_dark, width=2)
        pick_x = arm_x + 24
        pick_y = arm_y - 28
        draw.rectangle([pick_x - 2, pick_y - 5, pick_x + 2, pick_y + 30], fill=(120, 60, 15))
        draw.polygon([(pick_x - 15, pick_y - 10), (pick_x + 15, pick_y - 10),
                      (pick_x + 10, pick_y - 2), (pick_x - 10, pick_y - 2)],
                     fill=(180, 180, 180), outline=(90, 90, 90))
    else:
        draw.ellipse([cx - 29, body_top + 10, cx - 18, body_top + 23], fill=skin, outline=skin_dark)
        draw.ellipse([cx + 18, body_top + 10, cx + 29, body_top + 23], fill=skin, outline=skin_dark)
        if pose == 'idle':
            pick_x = cx - 34
            pick_y = body_top - 2
            draw.rectangle([pick_x - 1.5, pick_y, pick_x + 1.5, pick_y + 35], fill=(120, 60, 15))
            draw.polygon([(pick_x - 11, pick_y - 7), (pick_x + 11, pick_y - 7),
                          (pick_x + 7, pick_y), (pick_x - 7, pick_y)],
                         fill=(150, 150, 150), outline=(70, 70, 70))
    
    # 最终检查
    p_final = img.getpixel((cx, head_cy))
    print(f"\nFinal: face center pixel = {p_final}")


img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (200, 200, 255, 255))
draw_miner_debug(img, 0, 0)
img.save('/workspace/miner_tycoon/test_debug.png')
print("\nSaved test_debug.png")

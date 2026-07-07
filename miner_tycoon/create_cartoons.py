#!/usr/bin/env python3
"""
高品质卡通风格精灵图生成器
- 大头Q版角色设计
- 丰富的渐变、阴影、高光
- 详细的面部特征
- 服装纹理和细节
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import json

SPRITE_SIZE = 128
COLS = 6
ROWS = 8
OUTPUT_DIR = "/workspace/miner_tycoon/frontend/assets"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def lighten(hex_color, percent):
    r, g, b = hex_to_rgb(hex_color)
    r = min(255, r + int(255 * percent / 100))
    g = min(255, g + int(255 * percent / 100))
    b = min(255, b + int(255 * percent / 100))
    return (r, g, b)

def darken(hex_color, percent):
    r, g, b = hex_to_rgb(hex_color)
    r = max(0, r - int(255 * percent / 100))
    g = max(0, g - int(255 * percent / 100))
    b = max(0, b - int(255 * percent / 100))
    return (r, g, b)

def draw_ellipse_gradient(draw, bbox, color1, color2, direction='vertical'):
    """绘制渐变椭圆"""
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = (x2 - x1) / 2
    ry = (y2 - y1) / 2
    
    steps = 20
    for i in range(steps):
        ratio = i / steps
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        
        if direction == 'vertical':
            cur_ry = ry * (1 - ratio * 0.5)
            cur_rx = rx * (1 - ratio * 0.2)
            cur_y1 = cy - cur_ry + ratio * ry * 0.5
            cur_y2 = cy + cur_ry - ratio * ry * 0.5
        else:
            cur_rx = rx * (1 - ratio * 0.5)
            cur_x1 = cx - cur_rx + ratio * rx * 0.5
            cur_x2 = cx + cur_rx - ratio * rx * 0.5
        
        if direction == 'vertical':
            draw.ellipse([cx - cur_rx, cur_y1, cx + cur_rx, cur_y2],
                        fill=(r, g, b))
        else:
            draw.ellipse([cur_x1, cy - ry, cur_x2, cy + ry],
                        fill=(r, g, b))

def draw_character_base(img, cx, cy, scale=1.0):
    """绘制Q版角色基础：大头小身"""
    draw = ImageDraw.Draw(img)
    
    head_r = 28 * scale
    body_w = 36 * scale
    body_h = 28 * scale
    
    head_y = cy - 15 * scale
    body_y = cy + 18 * scale
    
    return {
        'head_cx': cx,
        'head_cy': head_y,
        'head_r': head_r,
        'body_x1': cx - body_w/2,
        'body_y1': body_y,
        'body_x2': cx + body_w/2,
        'body_y2': body_y + body_h,
    }

def draw_star(draw, cx, cy, outer_r, inner_r, points, color):
    """绘制星形"""
    star_points = []
    for i in range(points * 2):
        angle = i * math.pi / points - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        px = cx + math.cos(angle) * r
        py = cy + math.sin(angle) * r
        star_points.append((px, py))
    draw.polygon(star_points, fill=color)


def draw_miner(img, x, y, helmet_color='#FFD700', body_color='#4169E1', pose='idle'):
    """绘制Q版矿工角色"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    
    # 角色位置参数
    head_cy = y + 48  # 头部中心
    head_r = 26       # 头部半径
    body_top = y + 74  # 身体顶部
    body_bottom = y + 108  # 身体底部
    body_w = 42
    
    skin = (255, 218, 185)
    skin_dark = (210, 170, 120)
    
    hc = hex_to_rgb(helmet_color)
    hc_light = lighten(helmet_color, 20)
    hc_dark = darken(helmet_color, 25)
    
    bc = hex_to_rgb(body_color)
    bc_light = lighten(body_color, 15)
    bc_dark = darken(body_color, 25)
    
    # 阴影
    draw.ellipse([cx - 26, y + 112, cx + 26, y + 120], fill=(0, 0, 0, 45))
    
    # 腿
    leg_top = body_bottom - 3
    draw.rectangle([cx - 15, leg_top, cx - 5, leg_top + 16], fill=bc_dark, outline=darken(body_color, 35))
    draw.rectangle([cx + 5, leg_top, cx + 15, leg_top + 16], fill=bc_dark, outline=darken(body_color, 35))
    # 鞋子
    draw.ellipse([cx - 17, leg_top + 13, cx - 3, leg_top + 21], fill=(70, 40, 25))
    draw.ellipse([cx + 3, leg_top + 13, cx + 17, leg_top + 21], fill=(70, 40, 25))
    
    # 身体
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
    
    # 腰带
    belt_y = body_top + 14
    draw.rectangle([cx - body_w/2, belt_y, cx + body_w/2, belt_y + 7], fill=hc)
    draw.rectangle([cx - 6, belt_y + 1, cx + 6, belt_y + 6], fill=(255, 215, 0), outline=hc_dark)
    
    # 头部/脸部 - 用实心椭圆先画
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
                 fill=skin, outline=skin_dark, width=2)
    
    # 脸部阴影（下半部分）- 手动计算混合色
    for i in range(head_r):
        y_pos = head_cy + i
        w = 2 * math.sqrt(head_r * head_r - i * i)
        # 获取原始肤色
        # 阴影强度：从0到0.3
        shadow = 0.3 * i / head_r
        r = int(skin[0] * (1 - shadow) + 150 * shadow)
        g = int(skin[1] * (1 - shadow) + 110 * shadow)
        b = int(skin[2] * (1 - shadow) + 70 * shadow)
        draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], fill=(r, g, b))
    
    # 腮红 - 直接绘制混合色
    def draw_blush(draw, x, y, w, h, skin_color):
        """绘制圆形腮红"""
        blush_r = w // 2
        cx = x + w // 2
        cy = y + h // 2
        for i in range(blush_r):
            ratio = i / blush_r
            cur_w = 2 * math.sqrt(blush_r * blush_r - i * i)
            # 从边缘到中心，红色逐渐增加
            r = int(skin_color[0] * (1 - ratio * 0.5) + 255 * ratio * 0.5)
            g = int(skin_color[1] * (1 - ratio * 0.4) + 160 * ratio * 0.4)
            b = int(skin_color[2] * (1 - ratio * 0.3) + 170 * ratio * 0.3)
            draw.line([(cx - cur_w/2, cy - blush_r + i), (cx + cur_w/2, cy - blush_r + i)],
                      fill=(r, g, b))
            draw.line([(cx - cur_w/2, cy + blush_r - i), (cx + cur_w/2, cy + blush_r - i)],
                      fill=(r, g, b))
    
    draw_blush(draw, cx - 19, head_cy + 4, 10, 8, skin)
    draw_blush(draw, cx + 9, head_cy + 4, 10, 8, skin)
    
    # 眼睛
    eye_y = head_cy - 2
    # 左眼
    draw.ellipse([cx - 15, eye_y - 6, cx - 5, eye_y + 6], fill='white', outline=(70, 70, 70))
    draw.ellipse([cx - 12, eye_y - 3, cx - 7, eye_y + 3], fill=(40, 40, 70))
    draw.ellipse([cx - 11, eye_y - 2, cx - 9, eye_y], fill='white')
    # 右眼
    draw.ellipse([cx + 5, eye_y - 6, cx + 15, eye_y + 6], fill='white', outline=(70, 70, 70))
    draw.ellipse([cx + 7, eye_y - 3, cx + 12, eye_y + 3], fill=(40, 40, 70))
    draw.ellipse([cx + 8, eye_y - 2, cx + 10, eye_y], fill='white')
    
    # 眉毛
    brow_color = (120, 70, 30)
    draw.arc([cx - 15, eye_y - 13, cx - 5, eye_y - 4], 200, 340, fill=brow_color, width=2)
    draw.arc([cx + 5, eye_y - 13, cx + 15, eye_y - 4], 200, 340, fill=brow_color, width=2)
    
    # 嘴巴
    draw.arc([cx - 6, head_cy + 7, cx + 6, head_cy + 15], 0, 180, fill=(170, 80, 80), width=2)
    
    # 头盔 - 直接用弧形+矩形
    helmet_bottom = head_cy - 10  # 头盔底部线
    helmet_arc_top = head_cy - head_r - 12  # 头盔顶部
    helmet_arc_h = helmet_bottom - helmet_arc_top
    
    # 头盔主体：上半椭圆 + 下半矩形
    # 先画下半矩形
    rect_top = helmet_arc_top + helmet_arc_h * 0.4
    draw.rectangle([cx - head_r - 3, rect_top, cx + head_r + 3, helmet_bottom],
                   fill=hc)
    
    # 再画上半椭圆（用渐变感的方式）
    arc_r = head_r + 3
    arc_bottom_y = helmet_arc_top + arc_r  # 椭圆的中心y + 半径
    for i in range(int(arc_r * 0.7)):
        w = 2 * math.sqrt(arc_r * arc_r - i * i)
        ratio = i / (arc_r * 0.7)
        r = int(hc_light[0] + (hc[0] - hc_light[0]) * ratio)
        g = int(hc_light[1] + (hc[1] - hc_light[1]) * ratio)
        b = int(hc_light[2] + (hc[2] - hc_light[2]) * ratio)
        y_pos = helmet_arc_top + i
        draw.line([(cx - w/2, y_pos), (cx + w/2, y_pos)], fill=(r, g, b))
    
    # 头盔轮廓
    draw.arc([cx - head_r - 4, helmet_arc_top - 2, cx + head_r + 4, helmet_bottom + 10],
             180, 360, fill=hc_dark, width=2)
    draw.line([cx - head_r - 4, helmet_bottom, cx + head_r + 4, helmet_bottom], 
              fill=hc_dark, width=2)
    
    # 头灯
    lamp_y = helmet_arc_top + 18
    draw.ellipse([cx - 10, lamp_y - 5, cx + 10, lamp_y + 8], fill=(70, 70, 70), outline=(40, 40, 40))
    draw.ellipse([cx - 7, lamp_y - 2, cx + 7, lamp_y + 5], fill=(255, 255, 180))
    # 光晕 - 用环形线绘制
    for i in range(3):
        r = 15 + i * 8
        draw.ellipse([cx - r, lamp_y - r + 3, cx + r, lamp_y + r + 3],
                     outline=(255, 255, 150), width=1)
    
    # 头盔高光
    draw.arc([cx - 18, helmet_arc_top + 4, cx + 2, helmet_arc_top + 22], 200, 280, fill=hc_light, width=3)
    
    # 手臂和镐子
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


def draw_elevator_operator(img, x, y):
    """绘制电梯工角色"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE * 0.45
    
    base = draw_character_base(img, cx, cy, 1.1)
    
    hc = hex_to_rgb('#FF9800')
    hc_light = lighten('#FF9800', 25)
    hc_dark = darken('#FF9800', 30)
    
    bc = hex_to_rgb('#2196F3')
    bc_light = lighten('#2196F3', 20)
    bc_dark = darken('#2196F3', 25)
    
    skin = (255, 218, 185)
    skin_dark = (222, 184, 135)
    
    # 阴影
    draw.ellipse([cx - 28, base['body_y2'] + 2, cx + 28, base['body_y2'] + 10],
                 fill=(0, 0, 0, 50))
    
    # 身体
    body_gradient = Image.new('RGBA', 
                               (int(base['body_x2'] - base['body_x1']), 
                                int(base['body_y2'] - base['body_y1'])),
                               (0, 0, 0, 0))
    body_draw = ImageDraw.Draw(body_gradient)
    for i in range(int(base['body_y2'] - base['body_y1'])):
        ratio = i / (base['body_y2'] - base['body_y1'])
        r = int(bc_light[0] + (bc_dark[0] - bc_light[0]) * ratio)
        g = int(bc_light[1] + (bc_dark[1] - bc_light[1]) * ratio)
        b = int(bc_light[2] + (bc_dark[2] - bc_light[2]) * ratio)
        body_draw.line([(0, i), (body_gradient.width, i)], fill=(r, g, b))
    img.paste(body_gradient, (int(base['body_x1']), int(base['body_y1'])), body_gradient)
    
    draw.rounded_rectangle([base['body_x1'], base['body_y1'], 
                            base['body_x2'], base['body_y2']],
                           radius=8, outline=bc_dark, width=2)
    
    # 工牌
    draw.rectangle([cx - 5, base['body_y1'] + 8, cx + 10, base['body_y1'] + 16],
                   fill='white', outline=(200, 200, 200), width=1)
    
    # 脸部
    face_gradient = Image.new('RGBA', (int(base['head_r']*2), int(base['head_r']*2)), (0,0,0,0))
    face_draw = ImageDraw.Draw(face_gradient)
    for i in range(int(base['head_r']*2)):
        ratio = i / (base['head_r']*2)
        r = int(skin[0] + (210 - skin[0]) * ratio * 0.4)
        g = int(skin[1] + (170 - skin[1]) * ratio * 0.4)
        b = int(skin[2] + (130 - skin[2]) * ratio * 0.4)
        face_draw.ellipse([i*0.3, 0, base['head_r']*2 - i*0.3, base['head_r']*2],
                         fill=(r, g, b))
    img.paste(face_gradient, (int(base['head_cx'] - base['head_r']), 
                               int(base['head_cy'] - base['head_r'])), face_gradient)
    
    draw.ellipse([base['head_cx'] - base['head_r'], base['head_cy'] - base['head_r'],
                  base['head_cx'] + base['head_r'], base['head_cy'] + base['head_r']],
                 outline=skin_dark, width=2)
    
    # 腮红
    draw.ellipse([cx - 20, base['head_cy'] + 5, cx - 10, base['head_cy'] + 13],
                 fill=(255, 182, 193, 150))
    draw.ellipse([cx + 10, base['head_cy'] + 5, cx + 20, base['head_cy'] + 13],
                 fill=(255, 182, 193, 150))
    
    # 眼睛
    eye_y = base['head_cy'] - 2
    draw.ellipse([cx - 16, eye_y - 7, cx - 5, eye_y + 7], fill='white', outline=(100,100,100), width=1)
    draw.ellipse([cx + 5, eye_y - 7, cx + 16, eye_y + 7], fill='white', outline=(100,100,100), width=1)
    draw.ellipse([cx - 13, eye_y - 4, cx - 7, eye_y + 4], fill=(50, 50, 80))
    draw.ellipse([cx - 12, eye_y - 3, cx - 9, eye_y - 1], fill='white')
    draw.ellipse([cx + 7, eye_y - 4, cx + 13, eye_y + 4], fill=(50, 50, 80))
    draw.ellipse([cx + 8, eye_y - 3, cx + 11, eye_y - 1], fill='white')
    
    # 微笑
    draw.arc([cx - 7, base['head_cy'] + 6, cx + 7, base['head_cy'] + 14], 0, 180, 
             fill=(180, 100, 100), width=2)
    
    # 头盔
    helmet_bottom = base['head_cy']
    helmet_top = base['head_cy'] - base['head_r'] - 8
    helmet_h = helmet_bottom - helmet_top
    
    helmet_grad = Image.new('RGBA', (int(base['head_r']*2 + 10), int(helmet_h)), (0,0,0,0))
    helmet_draw = ImageDraw.Draw(helmet_grad)
    for i in range(int(helmet_h)):
        ratio = i / helmet_h
        r = int(hc_light[0] + (hc_dark[0] - hc_light[0]) * ratio)
        g = int(hc_light[1] + (hc_dark[1] - hc_light[1]) * ratio)
        b = int(hc_light[2] + (hc_dark[2] - hc_light[2]) * ratio)
        w = (base['head_r'] + 5) * 2 * (1 - abs(ratio - 0.3) * 0.6)
        x_offset = (helmet_grad.width - w) / 2
        helmet_draw.line([(x_offset, i), (x_offset + w, i)], fill=(r, g, b))
    img.paste(helmet_grad, (int(cx - base['head_r'] - 5), int(helmet_top)), helmet_grad)
    
    draw.arc([cx - base['head_r'] - 5, helmet_top - 2,
              cx + base['head_r'] + 5, helmet_bottom + 15],
             180, 360, fill=hc_dark, width=2)
    draw.line([cx - base['head_r'] - 5, helmet_bottom, 
               cx + base['head_r'] + 5, helmet_bottom], 
              fill=hc_dark, width=2)
    
    # 头灯
    lamp_cy = helmet_top + 18
    draw.ellipse([cx - 10, lamp_cy - 5, cx + 10, lamp_cy + 8],
                 fill=(80, 80, 80), outline=(50, 50, 50), width=1)
    draw.ellipse([cx - 7, lamp_cy - 3, cx + 7, lamp_cy + 5],
                 fill=(255, 255, 200))
    for i in range(3):
        alpha = 80 - i * 25
        r = 15 + i * 8
        draw.ellipse([cx - r, lamp_cy - r + 3, cx + r, lamp_cy + r + 3],
                     fill=(255, 255, 150, alpha))
    
    # 手部
    draw.ellipse([cx - 30, base['body_y1'] + 10, cx - 18, base['body_y1'] + 22],
                 fill=skin, outline=skin_dark, width=1)
    draw.ellipse([cx + 18, base['body_y1'] + 10, cx + 30, base['body_y1'] + 22],
                 fill=skin, outline=skin_dark, width=1)
    
    # 腿和鞋
    leg_y = base['body_y2'] - 3
    draw.rectangle([cx - 15, leg_y, cx - 5, leg_y + 15],
                   fill=bc_dark, outline=darken('#2196F3', 40), width=1)
    draw.rectangle([cx + 5, leg_y, cx + 15, leg_y + 15],
                   fill=bc_dark, outline=darken('#2196F3', 40), width=1)
    draw.ellipse([cx - 17, leg_y + 12, cx - 3, leg_y + 20], fill=(80, 50, 30))
    draw.ellipse([cx + 3, leg_y + 12, cx + 17, leg_y + 20], fill=(80, 50, 30))


def draw_ore(img, x, y, main_color='#FFD700', dark_color='#FFA000'):
    """绘制矿石宝石"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    size = 45
    
    mc = hex_to_rgb(main_color)
    dc = hex_to_rgb(dark_color)
    lc = lighten(main_color, 40)
    
    # 阴影
    draw.ellipse([cx - size + 5, cy + size - 10, cx + size - 5, cy + size],
                 fill=(0, 0, 0, 50))
    
    # 宝石主体 - 五边形
    points = [
        (cx, cy - size),
        (cx + size * 0.85, cy - size * 0.25),
        (cx + size * 0.65, cy + size * 0.8),
        (cx - size * 0.65, cy + size * 0.8),
        (cx - size * 0.85, cy - size * 0.25),
    ]
    
    # 渐变填充
    gem_img = Image.new('RGBA', (size*2, size*2), (0,0,0,0))
    gem_draw = ImageDraw.Draw(gem_img)
    for i in range(size*2):
        ratio = i / (size * 2)
        r = int(lc[0] + (dc[0] - lc[0]) * ratio)
        g = int(lc[1] + (dc[1] - lc[1]) * ratio)
        b = int(lc[2] + (dc[2] - lc[2]) * ratio)
        
        # 计算每一行的宽度
        y_pos = i - size
        if y_pos < -size * 0.25:
            # 顶部三角形部分
            t = (y_pos + size) / (size * 0.75)
            w = size * 1.7 * t
        elif y_pos < size * 0.8:
            w = size * 1.7
        else:
            t = (y_pos - size * 0.8) / (size * 0.2)
            w = size * 1.7 * (1 - t * 0.2)
        
        x1 = size - w/2
        x2 = size + w/2
        gem_draw.line([(x1, i), (x2, i)], fill=(r, g, b))
    
    img.paste(gem_img, (int(cx - size), int(cy - size)), gem_img)
    
    # 轮廓
    draw.polygon(points, outline=dc, width=3)
    
    # 切面线
    draw.line([(cx, cy - size), (cx, cy + size * 0.8)],
              fill=(255, 255, 255, 80), width=1)
    draw.line([(cx - size * 0.85, cy - size * 0.25), (cx + size * 0.85, cy - size * 0.25)],
              fill=(255, 255, 255, 80), width=1)
    
    # 高光
    highlight = Image.new('RGBA', (size, size), (0,0,0,0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.ellipse([5, 10, 30, 25], fill=(255, 255, 255, 180))
    hl_img = highlight.filter(ImageFilter.GaussianBlur(radius=2))
    img.paste(hl_img, (int(cx - size * 0.6), int(cy - size * 0.5)), hl_img)
    
    # 小高光点
    draw.ellipse([cx - 12, cy - 15, cx - 5, cy - 8], fill=(255, 255, 255, 200))
    draw.ellipse([cx + 8, cy + 5, cx + 14, cy + 10], fill=(255, 255, 255, 120))


def draw_icon_coin(img, x, y):
    """绘制金币图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    r = 42
    
    # 阴影
    draw.ellipse([cx - r + 3, cy - r + 5, cx + r + 3, cy + r + 5],
                 fill=(0, 0, 0, 60))
    
    # 金币主体渐变
    coin_img = Image.new('RGBA', (r*2, r*2), (0,0,0,0))
    coin_draw = ImageDraw.Draw(coin_img)
    for i in range(r*2):
        ratio = i / (r*2)
        y_pos = i - r
        w = 2 * math.sqrt(r*r - y_pos*y_pos) if abs(y_pos) < r else 0
        
        if ratio < 0.3:
            color = (255, 255, 180)
        elif ratio < 0.6:
            t = (ratio - 0.3) / 0.3
            color = (int(255 - 40*t), int(255 - 80*t), int(180 - 80*t))
        else:
            t = (ratio - 0.6) / 0.4
            color = (int(215 - 50*t), int(175 - 50*t), int(100 - 30*t))
        
        x1 = r - w/2
        x2 = r + w/2
        if w > 0:
            coin_draw.line([(x1, i), (x2, i)], fill=color)
    
    img.paste(coin_img, (int(cx - r), int(cy - r)), coin_img)
    
    # 外圈
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=(200, 120, 0), width=4)
    
    # 内圈
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                 outline=(230, 160, 0), width=2)
    
    # $符号
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    except:
        font = ImageFont.load_default()
    
    text = '$'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 4), text, fill=(180, 90, 0), font=font)
    
    # 高光
    hl = Image.new('RGBA', (r*2, r*2), (0,0,0,0))
    hl_draw = ImageDraw.Draw(hl)
    hl_draw.ellipse([r - 20, r - 30, r + 5, r - 15], fill=(255, 255, 255, 150))
    hl_img = hl.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(hl_img, (int(cx - r), int(cy - r)), hl_img)


def draw_icon_gem(img, x, y):
    """绘制钻石图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 阴影
    draw.ellipse([cx - 35, cy + 30, cx + 35, cy + 42],
                 fill=(0, 0, 0, 50))
    
    points = [
        (cx, cy - 45),
        (cx + 40, cy - 10),
        (cx + 25, cy + 40),
        (cx - 25, cy + 40),
        (cx - 40, cy - 10),
    ]
    
    # 渐变填充
    gem_img = Image.new('RGBA', (100, 100), (0,0,0,0))
    gem_draw = ImageDraw.Draw(gem_img)
    for i in range(100):
        ratio = i / 100
        y_pos = i - 50
        
        if y_pos < -10:
            t = (y_pos + 45) / 35
            w = 80 * t
        elif y_pos < 40:
            w = 80
        else:
            t = (y_pos - 40) / 10
            w = 80 * (1 - t * 0.4)
        
        x1 = 50 - w/2
        x2 = 50 + w/2
        
        if ratio < 0.2:
            color = (200, 240, 255)
        elif ratio < 0.5:
            t = (ratio - 0.2) / 0.3
            color = (int(200 - 50*t), int(240 - 60*t), int(255 - 50*t))
        else:
            t = (ratio - 0.5) / 0.5
            color = (int(150 - 80*t), int(180 - 100*t), int(205 - 80*t))
        
        if w > 0:
            gem_draw.line([(x1, i), (x2, i)], fill=color)
    
    img.paste(gem_img, (int(cx - 50), int(cy - 50)), gem_img)
    
    # 轮廓
    draw.polygon(points, outline=(0, 80, 160), width=3)
    
    # 切面
    draw.line([(cx, cy - 45), (cx, cy + 40)], fill=(255, 255, 255, 100), width=1)
    draw.line([(cx - 40, cy - 10), (cx + 40, cy - 10)], fill=(255, 255, 255, 100), width=1)
    draw.line([(cx - 20, cy - 10), (cx - 25, cy + 40)], fill=(0, 100, 180, 80), width=1)
    draw.line([(cx + 20, cy - 10), (cx + 25, cy + 40)], fill=(0, 100, 180, 80), width=1)
    
    # 高光
    draw.ellipse([cx - 20, cy - 25, cx - 5, cy - 12], fill=(255, 255, 255, 200))
    draw.ellipse([cx + 5, cy + 5, cx + 15, cy + 15], fill=(255, 255, 255, 100))


def draw_pickaxe(img, x, y, metal_color='#B0BEC5', handle_color='#8B4513'):
    """绘制镐子"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 阴影
    draw.ellipse([cx - 15, cy + 40, cx + 20, cy + 50], fill=(0, 0, 0, 40))
    
    # 手柄
    handle_w = 6
    handle_h = 55
    handle_x = cx - handle_w // 2
    handle_y = cy - 10
    
    # 手柄渐变
    for i in range(handle_h):
        ratio = i / handle_h
        c = lighten(handle_color, 20 - int(40 * ratio))
        draw.line([(handle_x, handle_y + i), (handle_x + handle_w, handle_y + i)], fill=c)
    draw.rectangle([handle_x, handle_y, handle_x + handle_w, handle_y + handle_h],
                   outline=darken(handle_color, 30), width=1)
    
    # 镐头
    pick_w = 45
    pick_h = 18
    pick_y = handle_y - pick_h + 5
    
    mc = hex_to_rgb(metal_color)
    mc_light = lighten(metal_color, 30)
    mc_dark = darken(metal_color, 25)
    
    # 镐头渐变
    for i in range(pick_h):
        ratio = i / pick_h
        r = int(mc_light[0] + (mc_dark[0] - mc_light[0]) * ratio)
        g = int(mc_light[1] + (mc_dark[1] - mc_light[1]) * ratio)
        b = int(mc_light[2] + (mc_dark[2] - mc_light[2]) * ratio)
        w = pick_w * (1 - abs(ratio - 0.5) * 0.3)
        x1 = cx - w // 2
        x2 = cx + w // 2
        draw.line([(x1, pick_y + i), (x2, pick_y + i)], fill=(r, g, b))
    
    # 镐头轮廓
    draw.polygon([
        (cx - pick_w//2, pick_y + pick_h//2),
        (cx - pick_w//2 + 5, pick_y),
        (cx + pick_w//2 - 5, pick_y),
        (cx + pick_w//2, pick_y + pick_h//2),
        (cx + pick_w//2 - 8, pick_y + pick_h),
        (cx - pick_w//2 + 8, pick_y + pick_h),
    ], outline=darken(metal_color, 35), width=2)
    
    # 高光
    draw.line([(cx - 15, pick_y + 3), (cx + 10, pick_y + 3)],
              fill=(255, 255, 255, 150), width=2)


def draw_icon_money(img, x, y):
    """绘制现金图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 阴影
    draw.ellipse([cx - 42, cy + 35, cx + 42, cy + 45], fill=(0, 0, 0, 40))
    
    # 钞票主体
    w, h = 80, 50
    x1, y1 = cx - w//2, cy - h//2
    
    # 渐变
    for i in range(h):
        ratio = i / h
        if ratio < 0.3:
            color = lighten('#4CAF50', 30 - int(20 * ratio / 0.3))
        else:
            t = (ratio - 0.3) / 0.7
            color = darken('#4CAF50', int(30 * t))
        draw.line([(x1, y1 + i), (x1 + w, y1 + i)], fill=color)
    
    # 边框
    draw.rounded_rectangle([x1, y1, x1 + w, y1 + h],
                           radius=5, outline=darken('#4CAF50', 40), width=2)
    
    # 内框
    draw.rounded_rectangle([x1 + 6, y1 + 6, x1 + w - 6, y1 + h - 6],
                           radius=3, outline=lighten('#4CAF50', 10), width=1)
    
    # $符号
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()
    text = '$'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 2), text, fill=(27, 94, 32), font=font)


def draw_icon_gear(img, x, y):
    """绘制设置齿轮图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    r = 38
    
    # 阴影
    draw.ellipse([cx - r + 3, cy - r + 5, cx + r + 3, cy + r + 5],
                 fill=(0, 0, 0, 50))
    
    # 齿轮齿
    teeth = 10
    outer_r = r
    inner_r = r * 0.75
    
    points = []
    for i in range(teeth * 2):
        angle = i * math.pi / teeth - math.pi / 2
        radius = outer_r if i % 2 == 0 else inner_r
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        points.append((px, py))
    
    # 齿轮主体渐变
    gear_img = Image.new('RGBA', (r*2+10, r*2+10), (0,0,0,0))
    gear_draw = ImageDraw.Draw(gear_img)
    
    center_x = r + 5
    center_y = r + 5
    for i in range(int(r*2)):
        ratio = i / (r*2)
        y_pos = i - r
        cur_r = math.sqrt(r*r - y_pos*y_pos) if abs(y_pos) < r else 0
        if cur_r > 0:
            if ratio < 0.4:
                color = lighten('#90A4AE', 20 - int(20 * ratio / 0.4))
            else:
                t = (ratio - 0.4) / 0.6
                color = darken('#90A4AE', int(25 * t))
            gear_draw.line([(center_x - cur_r, i), (center_x + cur_r, i)], fill=color)
    
    # 中心孔
    gear_draw.ellipse([center_x - r*0.35, center_y - r*0.35,
                       center_x + r*0.35, center_y + r*0.35],
                      fill=(50, 60, 70))
    
    img.paste(gear_img, (int(cx - r - 5), int(cy - r - 5)), gear_img)
    
    # 轮廓
    draw.polygon(points, outline=darken('#607D8B', 20), width=2)
    draw.ellipse([cx - r*0.35, cy - r*0.35, cx + r*0.35, cy + r*0.35],
                 outline=darken('#455A64', 10), width=2)


def draw_icon_music(img, x, y):
    """绘制音乐图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 阴影
    draw.ellipse([cx - 25, cy + 35, cx + 30, cy + 45], fill=(0, 0, 0, 40))
    
    # 音符
    note_color = hex_to_rgb('#9C27B0')
    
    # 符头1
    draw.ellipse([cx - 25, cy + 15, cx - 5, cy + 32],
                 fill=note_color, outline=darken('#9C27B0', 30), width=2)
    # 符干1
    draw.rectangle([cx - 8, cy - 25, cx - 3, cy + 18],
                   fill=note_color)
    
    # 符头2
    draw.ellipse([cx + 5, cy + 22, cx + 25, cy + 39],
                 fill=note_color, outline=darken('#9C27B0', 30), width=2)
    # 符干2
    draw.rectangle([cx + 20, cy - 15, cx + 25, cy + 25],
                   fill=note_color)
    
    # 横梁
    draw.polygon([
        (cx - 8, cy - 25),
        (cx + 25, cy - 15),
        (cx + 25, cy - 8),
        (cx - 8, cy - 18),
    ], fill=note_color)
    
    # 高光
    draw.ellipse([cx - 20, cy + 18, cx - 12, cy + 23],
                 fill=(255, 255, 255, 150))


def draw_icon_star(img, x, y):
    """绘制星星图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    r = 42
    
    # 阴影
    draw.ellipse([cx - r + 3, cy - r + 8, cx + r + 3, cy + r + 8],
                 fill=(0, 0, 0, 50))
    
    # 五角星
    points = 5
    outer_r = r
    inner_r = r * 0.45
    
    star_points = []
    for i in range(points * 2):
        angle = i * math.pi / points - math.pi / 2
        radius = outer_r if i % 2 == 0 else inner_r
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        star_points.append((px, py))
    
    # 渐变填充
    star_img = Image.new('RGBA', (r*2+10, r*2+10), (0,0,0,0))
    star_draw = ImageDraw.Draw(star_img)
    center = r + 5
    
    for i in range(int(r*2)):
        ratio = i / (r*2)
        y_pos = i - r
        
        # 计算这一行是否在星星内
        # 简化：用圆形渐变近似
        dist_from_center = abs(y_pos)
        max_w = 2 * math.sqrt(r*r - y_pos*y_pos) if abs(y_pos) < r else 0
        
        if max_w > 0:
            if ratio < 0.3:
                color = lighten('#FFD700', 30 - int(20 * ratio / 0.3))
            else:
                t = (ratio - 0.3) / 0.7
                color = darken('#FFD700', int(30 * t))
            star_draw.line([(center - max_w/2, i), (center + max_w/2, i)], fill=color)
    
    img.paste(star_img, (int(cx - r - 5), int(cy - r - 5)), star_img)
    
    draw.polygon(star_points, outline=darken('#FF8F00', 20), width=2)
    
    # 高光
    draw.ellipse([cx - 18, cy - 20, cx - 5, cy - 8],
                 fill=(255, 255, 255, 180))


def draw_icon_lock(img, x, y):
    """绘制锁图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 阴影
    draw.ellipse([cx - 30, cy + 35, cx + 30, cy + 45], fill=(0, 0, 0, 40))
    
    # 锁身
    body_w = 60
    body_h = 45
    body_x = cx - body_w // 2
    body_y = cy - 5
    
    for i in range(body_h):
        ratio = i / body_h
        if ratio < 0.3:
            color = lighten('#FFC107', 20 - int(15 * ratio / 0.3))
        else:
            t = (ratio - 0.3) / 0.7
            color = darken('#FFC107', int(25 * t))
        draw.line([(body_x, body_y + i), (body_x + body_w, body_y + i)], fill=color)
    
    draw.rounded_rectangle([body_x, body_y, body_x + body_w, body_y + body_h],
                           radius=8, outline=darken('#FF8F00', 20), width=2)
    
    # 锁梁
    beam_w = 8
    beam_r = 22
    draw.arc([cx - beam_r, cy - 35, cx + beam_r, cy + 5],
             180, 360, fill=darken('#FF8F00', 10), width=beam_w)
    
    # 锁孔
    draw.ellipse([cx - 6, cy + 5, cx + 6, cy + 15],
                 fill=darken('#FF8F00', 30))
    draw.rectangle([cx - 2, cy + 10, cx + 2, cy + 22],
                   fill=darken('#FF8F00', 30))
    
    # 高光
    draw.ellipse([cx - 20, body_y + 8, cx - 8, body_y + 15],
                 fill=(255, 255, 255, 150))


def draw_icon_check(img, x, y):
    """绘制对勾图标"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    r = 40
    
    # 阴影
    draw.ellipse([cx - r + 3, cy - r + 5, cx + r + 3, cy + r + 5],
                 fill=(0, 0, 0, 50))
    
    # 圆形背景
    circle_img = Image.new('RGBA', (r*2+10, r*2+10), (0,0,0,0))
    circle_draw = ImageDraw.Draw(circle_img)
    center = r + 5
    
    for i in range(int(r*2)):
        y_pos = i - r
        cur_r = math.sqrt(r*r - y_pos*y_pos) if abs(y_pos) < r else 0
        if cur_r > 0:
            ratio = i / (r*2)
            if ratio < 0.4:
                color = lighten('#4CAF50', 25 - int(20 * ratio / 0.4))
            else:
                t = (ratio - 0.4) / 0.6
                color = darken('#4CAF50', int(20 * t))
            circle_draw.line([(center - cur_r, i), (center + cur_r, i)], fill=color)
    
    img.paste(circle_img, (int(cx - r - 5), int(cy - r - 5)), circle_img)
    
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=darken('#2E7D32', 10), width=2)
    
    # 对勾
    draw.line([(cx - 22, cy), (cx - 5, cy + 18), (cx + 25, cy - 15)],
              fill='white', width=8)
    draw.line([(cx - 22, cy), (cx - 5, cy + 18), (cx + 25, cy - 15)],
              fill=lighten('#4CAF50', 30), width=3)


def draw_minecart(img, x, y, full=False):
    """绘制矿车"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE * 0.58
    
    # 阴影
    draw.ellipse([cx - 40, cy + 28, cx + 40, cy + 38], fill=(0, 0, 0, 50))
    
    # 车厢主体
    cart_top_w = 70
    cart_bottom_w = 55
    cart_h = 32
    cart_top_y = cy - cart_h
    
    # 车厢渐变
    cart_img = Image.new('RGBA', (80, 50), (0,0,0,0))
    cart_draw = ImageDraw.Draw(cart_img)
    
    for i in range(cart_h):
        ratio = i / cart_h
        w = cart_top_w - (cart_top_w - cart_bottom_w) * ratio
        x1 = 40 - w/2
        x2 = 40 + w/2
        if ratio < 0.4:
            color = lighten('#E53935', 20 - int(15 * ratio / 0.4))
        else:
            t = (ratio - 0.4) / 0.6
            color = darken('#E53935', int(25 * t))
        cart_draw.line([(x1, i), (x2, i)], fill=color)
    
    img.paste(cart_img, (int(cx - 40), int(cart_top_y)), cart_img)
    
    # 车厢轮廓
    draw.polygon([
        (cx - cart_top_w/2, cart_top_y),
        (cx + cart_top_w/2, cart_top_y),
        (cx + cart_bottom_w/2, cart_top_y + cart_h),
        (cx - cart_bottom_w/2, cart_top_y + cart_h),
    ], outline=darken('#C62828', 10), width=2)
    
    # 车厢顶部边框
    draw.rectangle([cx - cart_top_w/2, cart_top_y - 4,
                    cx + cart_top_w/2, cart_top_y],
                   fill=darken('#C62828', 5))
    
    # 矿石
    if full:
        ore_y = cart_top_y - 8
        for i in range(5):
            ox = cx - 25 + i * 13
            oy = ore_y - (i % 2) * 8
            size = 12
            draw.polygon([
                (ox, oy - size),
                (ox + size*0.8, oy - size*0.3),
                (ox + size*0.6, oy + size*0.5),
                (ox - size*0.6, oy + size*0.5),
                (ox - size*0.8, oy - size*0.3),
            ], fill='#FFD700', outline='#FFA000', width=1)
    
    # 轮子
    wheel_r = 12
    wheel_y = cy + 15
    
    # 左轮
    draw.ellipse([cx - 28 - wheel_r, wheel_y - wheel_r,
                  cx - 28 + wheel_r, wheel_y + wheel_r],
                 fill='#333', outline='#111', width=2)
    draw.ellipse([cx - 28 - wheel_r*0.5, wheel_y - wheel_r*0.5,
                  cx - 28 + wheel_r*0.5, wheel_y + wheel_r*0.5],
                 fill='#666')
    
    # 右轮
    draw.ellipse([cx + 28 - wheel_r, wheel_y - wheel_r,
                  cx + 28 + wheel_r, wheel_y + wheel_r],
                 fill='#333', outline='#111', width=2)
    draw.ellipse([cx + 28 - wheel_r*0.5, wheel_y - wheel_r*0.5,
                  cx + 28 + wheel_r*0.5, wheel_y + wheel_r*0.5],
                 fill='#666')


def draw_elevator_car(img, x, y, open_doors=False):
    """绘制电梯"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    w, h = 55, 80
    x1, y1 = cx - w//2, cy - h//2
    
    # 外框
    frame_img = Image.new('RGBA', (w + 10, h + 10), (0,0,0,0))
    frame_draw = ImageDraw.Draw(frame_img)
    
    for i in range(h):
        ratio = i / h
        if ratio < 0.3:
            color = lighten('#78909C', 15 - int(10 * ratio / 0.3))
        else:
            t = (ratio - 0.3) / 0.7
            color = darken('#78909C', int(20 * t))
        frame_draw.line([(0, i + 5), (w + 10, i + 5)], fill=color)
    
    img.paste(frame_img, (int(x1 - 5), int(y1 - 5)), frame_img)
    
    draw.rounded_rectangle([x1, y1, x1 + w, y1 + h],
                           radius=5, outline=darken('#546E7A', 10), width=3)
    
    if open_doors:
        # 开门 - 黑色内部
        draw.rectangle([x1 + 5, y1 + 5, x1 + w - 5, y1 + h - 5],
                       fill='#1a1a2e')
        # 左门（开着）
        draw.rectangle([x1 - 8, y1 + 3, x1 + 3, y1 + h - 3],
                       fill='#90A4AE', outline='#546E7A', width=1)
        # 右门（开着）
        draw.rectangle([x1 + w - 3, y1 + 3, x1 + w + 8, y1 + h - 3],
                       fill='#90A4AE', outline='#546E7A', width=1)
    else:
        # 关门 - 两扇门
        door_w = (w - 8) // 2
        # 左门
        for i in range(h - 10):
            ratio = i / (h - 10)
            if ratio < 0.5:
                color = lighten('#90A4AE', 10 - int(15 * ratio / 0.5))
            else:
                t = (ratio - 0.5) / 0.5
                color = darken('#90A4AE', int(15 * t))
            draw.line([(x1 + 4, y1 + 5 + i), (x1 + 4 + door_w, y1 + 5 + i)], fill=color)
        
        draw.rectangle([x1 + 4, y1 + 5, x1 + 4 + door_w, y1 + h - 5],
                       outline='#546E7A', width=1)
        # 右门
        draw.rectangle([x1 + w - 4 - door_w, y1 + 5, x1 + w - 4, y1 + h - 5],
                       fill='#90A4AE', outline='#546E7A', width=1)
        # 中间缝
        draw.line([cx, y1 + 5, cx, y1 + h - 5], fill='#455A64', width=2)
    
    # 顶部指示灯
    draw.ellipse([cx - 5, y1 - 10, cx + 5, y1],
                 fill='#FFC107', outline='#FF8F00', width=1)


def draw_tower(img, x, y, color='#42A5F5'):
    """绘制塔楼建筑"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE - 10
    
    # 阴影
    draw.ellipse([cx - 30, base_y + 2, cx + 30, base_y + 12],
                 fill=(0, 0, 0, 50))
    
    tower_w = 50
    tower_h = 75
    tower_x = cx - tower_w // 2
    tower_y = base_y - tower_h
    
    # 塔身渐变
    for i in range(tower_h):
        ratio = i / tower_h
        if ratio < 0.3:
            c = lighten(color, 20 - int(15 * ratio / 0.3))
        else:
            t = (ratio - 0.3) / 0.7
            c = darken(color, int(20 * t))
        draw.line([(tower_x, tower_y + i), (tower_x + tower_w, tower_y + i)], fill=c)
    
    # 塔身轮廓
    draw.rectangle([tower_x, tower_y, tower_x + tower_w, tower_y + tower_h],
                   outline=darken(color, 25), width=2)
    
    # 屋顶
    roof_h = 25
    draw.polygon([
        (tower_x - 5, tower_y),
        (cx, tower_y - roof_h),
        (tower_x + tower_w + 5, tower_y),
    ], fill=darken('#E53935', 10), outline='#B71C1C', width=2)
    
    # 窗户
    win_w = 22
    win_h = 16
    
    # 上窗
    win_y1 = tower_y + 12
    draw.rounded_rectangle([cx - win_w//2, win_y1, cx + win_w//2, win_y1 + win_h],
                           radius=2, fill='#FFF9C4', outline='#FBC02D', width=2)
    # 窗格
    draw.line([cx, win_y1, cx, win_y1 + win_h], fill='#FBC02D', width=1)
    draw.line([cx - win_w//2, win_y1 + win_h//2, cx + win_w//2, win_y1 + win_h//2],
              fill='#FBC02D', width=1)
    
    # 下窗
    win_y2 = tower_y + 42
    draw.rounded_rectangle([cx - win_w//2, win_y2, cx + win_w//2, win_y2 + win_h],
                           radius=2, fill='#FFF9C4', outline='#FBC02D', width=2)
    draw.line([cx, win_y2, cx, win_y2 + win_h], fill='#FBC02D', width=1)
    draw.line([cx - win_w//2, win_y2 + win_h//2, cx + win_w//2, win_y2 + win_h//2],
              fill='#FBC02D', width=1)
    
    # 底座
    draw.rectangle([tower_x - 6, base_y - 8, tower_x + tower_w + 6, base_y],
                   fill=darken(color, 15), outline=darken(color, 30), width=1)
    
    # 旗帜
    draw.rectangle([cx - 1, tower_y - roof_h - 15, cx + 1, tower_y - roof_h + 2],
                   fill='#5D4037')
    draw.polygon([
        (cx + 1, tower_y - roof_h - 13),
        (cx + 18, tower_y - roof_h - 8),
        (cx + 1, tower_y - roof_h - 3),
    ], fill='#E53935', outline='#B71C1C', width=1)


def draw_effect_mining(img, x, y, frame=1):
    """绘制采矿特效"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    if frame == 1:
        # 小星星
        colors = ['#FFD700', '#FF9800', '#FFEB3B']
        positions = [(0, -25), (-20, 10), (18, 15)]
        sizes = [12, 8, 10]
        for (px, py), color, size in zip(positions, colors, sizes):
            draw_star(draw, cx + px, cy + py, size, size*0.45, 5, hex_to_rgb(color))
    elif frame == 2:
        # 更多星星
        colors = ['#FFD700', '#FF5722', '#FFEB3B', '#FF9800', '#FFC107']
        positions = [(0, 0), (-25, -18), (22, -12), (-18, 22), (20, 20)]
        sizes = [18, 10, 12, 9, 11]
        for (px, py), color, size in zip(positions, colors, sizes):
            draw_star(draw, cx + px, cy + py, size, size*0.45, 5, hex_to_rgb(color))
    elif frame == 3:
        # 大爆炸
        for i in range(3):
            r = 35 - i * 10
            alpha = 150 - i * 40
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                         outline=(255, 235, 59, alpha), width=3)
        draw_star(draw, cx, cy, 22, 10, 5, (255, 255, 255))


def draw_effect_gold(img, x, y, frame=1):
    """绘制金币特效"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    if frame == 1:
        positions = [(0, -5), (-22, 5), (18, 10)]
        sizes = [25, 18, 20]
    else:
        positions = [(0, -15), (-25, -5), (20, 0), (-12, 20), (18, 22)]
        sizes = [22, 16, 18, 14, 12]
    
    for (px, py), size in zip(positions, sizes):
        c = cx + px
        d = cy + py
        # 金币
        draw.ellipse([c - size, d - size*0.7, c + size, d + size*0.7],
                     fill='#FFD700', outline='#FF8F00', width=2)
        # $符号
        if size > 15:
            draw.text((c - 5, d - 6), '$', fill='#B71C1C')


def draw_effect_sparkle(img, x, y):
    """绘制闪耀特效"""
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    
    # 八角星
    points = []
    for i in range(16):
        angle = i * math.pi / 8
        r = 40 if i % 2 == 0 else 12
        px = cx + math.cos(angle) * r
        py = cy + math.sin(angle) * r
        points.append((px, py))
    
    draw.polygon(points, fill=(255, 255, 255, 200))
    draw_star(draw, cx, cy, 20, 9, 5, hex_to_rgb('#FFEB3B'))


SPRITE_DEFS = [
    # 第0行 - 矿工角色
    ("miner_idle", 0, 0, lambda img, x, y: draw_miner(img, x, y, '#FFD700', '#4169E1', 'idle')),
    ("miner_mining", 0, 1, lambda img, x, y: draw_miner(img, x, y, '#FFD700', '#4169E1', 'mining')),
    ("miner_walk", 0, 2, lambda img, x, y: draw_miner(img, x, y, '#FFD700', '#4169E1', 'idle')),
    ("miner2_idle", 0, 3, lambda img, x, y: draw_miner(img, x, y, '#FF9800', '#4CAF50', 'idle')),
    ("miner2_mining", 0, 4, lambda img, x, y: draw_miner(img, x, y, '#FF9800', '#4CAF50', 'mining')),
    ("miner3_idle", 0, 5, lambda img, x, y: draw_miner(img, x, y, '#E91E63', '#795548', 'idle')),
    
    # 第1行 - 其他角色
    ("elevator_worker", 1, 0, lambda img, x, y: draw_miner(img, x, y, '#FF5722', '#2196F3', 'idle')),
    ("ground_worker", 1, 1, lambda img, x, y: draw_miner(img, x, y, '#FFC107', '#8BC34A', 'idle')),
    ("supervisor", 1, 2, lambda img, x, y: draw_miner(img, x, y, '#9C27B0', '#3F51B5', 'idle')),
    ("shopkeeper", 1, 3, lambda img, x, y: draw_miner(img, x, y, '#F44336', '#FF9800', 'idle')),
    ("engineer", 1, 4, lambda img, x, y: draw_miner(img, x, y, '#2196F3', '#607D8B', 'idle')),
    ("chef", 1, 5, lambda img, x, y: draw_miner(img, x, y, '#795548', '#FF5722', 'idle')),
    
    # 第2行 - 道具
    ("pickaxe_iron", 2, 0, lambda img, x, y: draw_pickaxe(img, x, y, '#B0BEC5', '#8B4513')),
    ("pickaxe_gold", 2, 1, lambda img, x, y: draw_pickaxe(img, x, y, '#FFD700', '#8B4513')),
    ("pickaxe_diamond", 2, 2, lambda img, x, y: draw_pickaxe(img, x, y, '#64B5F6', '#8B4513')),
    ("ore_small", 2, 3, lambda img, x, y: draw_ore(img, x + 10, y + 10, '#FFD700', '#FFA000')),
    ("gem_ruby", 2, 4, lambda img, x, y: draw_ore(img, x + 10, y + 10, '#EF5350', '#C62828')),
    ("gem_emerald", 2, 5, lambda img, x, y: draw_ore(img, x + 10, y + 10, '#66BB6A', '#2E7D32')),
    
    # 第3行 - 矿石宝石
    ("ore_gold", 3, 0, lambda img, x, y: draw_ore(img, x, y, '#FFD700', '#FFA000')),
    ("ore_copper", 3, 1, lambda img, x, y: draw_ore(img, x, y, '#FF8A65', '#E64A19')),
    ("ore_silver", 3, 2, lambda img, x, y: draw_ore(img, x, y, '#E0E0E0', '#9E9E9E')),
    ("ore_diamond", 3, 3, lambda img, x, y: draw_ore(img, x, y, '#64B5F6', '#1976D2')),
    ("ore_ruby", 3, 4, lambda img, x, y: draw_ore(img, x, y, '#EF5350', '#C62828')),
    ("ore_emerald", 3, 5, lambda img, x, y: draw_ore(img, x, y, '#66BB6A', '#2E7D32')),
    
    # 第4行 - UI图标
    ("icon_gold", 4, 0, draw_icon_coin),
    ("icon_gem", 4, 1, draw_icon_gem),
    ("icon_cash", 4, 2, draw_icon_money),
    ("icon_settings", 4, 3, draw_icon_gear),
    ("icon_music", 4, 4, draw_icon_music),
    ("icon_star", 4, 5, draw_icon_star),
    
    # 第5行 - 更多UI图标
    ("icon_lock", 5, 0, draw_icon_lock),
    ("icon_check", 5, 1, draw_icon_check),
    ("icon_pickaxe", 5, 2, lambda img, x, y: draw_pickaxe(img, x + 5, y + 10, '#B0BEC5', '#8B4513')),
    ("icon_elevator", 5, 3, lambda img, x, y: draw_elevator_car(img, x + 5, y + 5, False)),
    ("icon_factory", 5, 4, lambda img, x, y: draw_tower(img, x, y + 5, '#FF8A65')),
    ("icon_mountain", 5, 5, lambda img, x, y: None),
    
    # 第6行 - 建筑和载具
    ("tower_blue", 6, 0, lambda img, x, y: draw_tower(img, x, y, '#42A5F5')),
    ("tower_green", 6, 1, lambda img, x, y: draw_tower(img, x, y, '#66BB6A')),
    ("tower_red", 6, 2, lambda img, x, y: draw_tower(img, x, y, '#EF5350')),
    ("minecart_empty", 6, 3, lambda img, x, y: draw_minecart(img, x, y, False)),
    ("minecart_full", 6, 4, lambda img, x, y: draw_minecart(img, x, y, True)),
    ("elevator_closed", 6, 5, lambda img, x, y: draw_elevator_car(img, x, y, False)),
    
    # 第7行 - 特效
    ("effect_mining_1", 7, 0, lambda img, x, y: draw_effect_mining(img, x, y, 1)),
    ("effect_mining_2", 7, 1, lambda img, x, y: draw_effect_mining(img, x, y, 2)),
    ("effect_mining_3", 7, 2, lambda img, x, y: draw_effect_mining(img, x, y, 3)),
    ("effect_gold_1", 7, 3, lambda img, x, y: draw_effect_gold(img, x, y, 1)),
    ("effect_gold_2", 7, 4, lambda img, x, y: draw_effect_gold(img, x, y, 2)),
    ("effect_sparkle", 7, 5, draw_effect_sparkle),
]

def main():
    print("=" * 60)
    print("生成高品质卡通风格精灵图...")
    print("=" * 60)
    
    sprite_sheet = Image.new('RGBA', (COLS * SPRITE_SIZE, ROWS * SPRITE_SIZE), (0, 0, 0, 0))
    sprite_map = {}
    
    for key, row, col, draw_fn in SPRITE_DEFS:
        x = col * SPRITE_SIZE
        y = row * SPRITE_SIZE
        
        cell = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
        try:
            draw_fn(cell, 0, 0)
            sprite_sheet.paste(cell, (x, y), cell)
            status = "✓"
        except Exception as e:
            print(f"  ✗ {key}: {e}")
            status = "✗"
        
        sprite_map[key] = {
            "x": x, "y": y,
            "width": SPRITE_SIZE, "height": SPRITE_SIZE,
            "row": row, "col": col
        }
        print(f"  {status} {key}")
    
    sprite_path = os.path.join(OUTPUT_DIR, "sprites.png")
    sprite_sheet.save(sprite_path)
    print(f"\n精灵图已保存: {sprite_path}")
    print(f"尺寸: {COLS * SPRITE_SIZE} x {ROWS * SPRITE_SIZE}")
    
    map_path = os.path.join(OUTPUT_DIR, "sprites.json")
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump({
            "image": "sprites.png",
            "width": COLS * SPRITE_SIZE,
            "height": ROWS * SPRITE_SIZE,
            "sprite_size": SPRITE_SIZE,
            "cols": COLS,
            "rows": ROWS,
            "sprites": sprite_map
        }, f, indent=2, ensure_ascii=False)
    print(f"JSON映射: {map_path}")
    
    css_path = os.path.join(OUTPUT_DIR, "sprites.css")
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write("/* 游戏精灵图 CSS */\n")
        f.write(".sprite {\n")
        f.write(f"    background-image: url('sprites.png');\n")
        f.write(f"    background-size: {COLS * SPRITE_SIZE}px {ROWS * SPRITE_SIZE}px;\n")
        f.write(f"    width: {SPRITE_SIZE}px;\n")
        f.write(f"    height: {SPRITE_SIZE}px;\n")
        f.write("    display: inline-block;\n")
        f.write("}\n\n")
        
        for key, pos in sprite_map.items():
            f.write(f".sprite-{key} {{\n")
            f.write(f"    background-position: -{pos['x']}px -{pos['y']}px;\n")
            f.write("}\n\n")
    
    print(f"CSS文件: {css_path}")
    print(f"\n共生成 {len(SPRITE_DEFS)} 个精灵")
    print("=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
用PIL直接绘制游戏精灵图
生成一张包含48个精灵的PNG精灵图 + CSS映射文件
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

SPRITE_SIZE = 128
COLS = 6
ROWS = 8
OUTPUT_DIR = "/workspace/miner_tycoon/frontend/assets"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def adjust_color(hex_color, amount):
    r, g, b = hex_to_rgb(hex_color)
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    return (r, g, b)

def draw_round_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    if fill:
        draw.rounded_rectangle(xy, radius=radius, fill=fill)
    if outline:
        draw.rounded_rectangle(xy, radius=radius, outline=outline, width=width)

def draw_star(draw, cx, cy, outer_r, inner_r, points, fill):
    coords = []
    for i in range(points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        angle = (i * math.pi / points) - math.pi / 2
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        coords.append((x, y))
    draw.polygon(coords, fill=fill)

def draw_miner_idle(img, x, y, helmet_color='#FFD700', body_color='#4169E1'):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.15
    s = SPRITE_SIZE / 128
    
    body_y = base_y + 40 * s
    draw_round_rect(draw, [cx - 22*s, body_y, cx + 22*s, body_y + 36*s], 
                    radius=6*s, fill=hex_to_rgb(body_color), 
                    outline=adjust_color(body_color, -50), width=3)
    
    face_y = base_y + 12*s
    draw_round_rect(draw, [cx - 17*s, face_y, cx + 17*s, face_y + 28*s],
                    radius=7*s, fill=(255, 218, 185), outline=(222, 184, 135), width=2)
    
    draw.ellipse([cx - 7*s, face_y + 10*s, cx - 2*s, face_y + 15*s], fill=(50, 50, 50))
    draw.ellipse([cx + 2*s, face_y + 10*s, cx + 7*s, face_y + 15*s], fill=(50, 50, 50))
    
    helmet_y = base_y
    draw.pieslice([cx - 24*s, helmet_y - 4*s, cx + 24*s, helmet_y + 32*s],
                  180, 360, fill=hex_to_rgb(helmet_color), outline=adjust_color(helmet_color, -60))
    
    draw.ellipse([cx - 9*s, helmet_y + 6*s, cx + 9*s, helmet_y + 24*s],
                 fill=(255, 255, 0), outline=(255, 165, 0))
    
    belt_y = body_y + 8*s
    draw.rectangle([cx - 22*s, belt_y, cx + 22*s, belt_y + 8*s],
                   fill=hex_to_rgb('#FFD700'))

def draw_miner_mining(img, x, y, helmet_color='#FFD700', body_color='#4169E1'):
    draw_miner_idle(img, x - 5, y, helmet_color, body_color)
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2 + 15
    base_y = y + SPRITE_SIZE * 0.45
    s = SPRITE_SIZE / 128
    
    px = cx + 8*s
    py = base_y - 15*s
    draw.rectangle([px - 3*s, py, px + 3*s, py + 45*s],
                   fill=(139, 69, 19), outline=(93, 64, 55), width=2)
    
    pick_y = py - 12*s
    draw.polygon([
        (px - 22*s, pick_y),
        (px + 22*s, pick_y),
        (px + 15*s, pick_y + 14*s),
        (px - 15*s, pick_y + 14*s)
    ], fill=(192, 192, 192), outline=(112, 112, 112))

def draw_elevator_worker(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.12
    s = SPRITE_SIZE / 128
    
    body_y = base_y + 38*s
    draw_round_rect(draw, [cx - 24*s, body_y, cx + 24*s, body_y + 42*s],
                    radius=7*s, fill=hex_to_rgb('#2196F3'), outline=(13, 71, 161), width=3)
    
    face_y = base_y + 10*s
    draw.ellipse([cx - 22*s, face_y, cx + 22*s, face_y + 44*s],
                 fill=(255, 218, 185), outline=(222, 184, 135), width=2)
    
    draw.ellipse([cx - 9*s, face_y + 14*s, cx - 3*s, face_y + 20*s], fill=(50, 50, 50))
    draw.ellipse([cx + 3*s, face_y + 14*s, cx + 9*s, face_y + 20*s], fill=(50, 50, 50))
    
    helmet_y = base_y - 2*s
    draw.pieslice([cx - 26*s, helmet_y, cx + 26*s, helmet_y + 36*s],
                  180, 360, fill=hex_to_rgb('#FF9800'), outline=(230, 81, 0))
    
    draw.ellipse([cx - 10*s, helmet_y + 10*s, cx + 10*s, helmet_y + 30*s],
                 fill=(255, 235, 59))

def draw_ground_worker(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.18
    s = SPRITE_SIZE / 128
    
    body_y = base_y + 35*s
    draw_round_rect(draw, [cx - 22*s, body_y, cx + 22*s, body_y + 38*s],
                    radius=6*s, fill=hex_to_rgb('#4CAF50'), outline=(27, 94, 32), width=3)
    
    face_y = base_y + 10*s
    draw_round_rect(draw, [cx - 17*s, face_y, cx + 17*s, face_y + 26*s],
                    radius=7*s, fill=(255, 218, 185), outline=(222, 184, 135), width=2)
    
    draw.ellipse([cx - 7*s, face_y + 10*s, cx - 2*s, face_y + 15*s], fill=(50, 50, 50))
    draw.ellipse([cx + 2*s, face_y + 10*s, cx + 7*s, face_y + 15*s], fill=(50, 50, 50))
    
    helmet_y = base_y
    draw.pieslice([cx - 24*s, helmet_y - 2*s, cx + 24*s, helmet_y + 30*s],
                  180, 360, fill=hex_to_rgb('#FFC107'), outline=(255, 143, 0))

def draw_supervisor(img, x, y, suit_color='#9C27B0'):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.15
    s = SPRITE_SIZE / 128
    
    body_y = base_y + 38*s
    draw_round_rect(draw, [cx - 24*s, body_y, cx + 24*s, body_y + 42*s],
                    radius=6*s, fill=hex_to_rgb(suit_color), outline=adjust_color(suit_color, -50), width=3)
    
    draw.rectangle([cx - 14*s, body_y, cx + 14*s, body_y + 14*s], fill=(255, 248, 225))
    
    face_y = base_y + 12*s
    draw.ellipse([cx - 20*s, face_y, cx + 20*s, face_y + 40*s],
                 fill=(255, 218, 185), outline=(222, 184, 135), width=2)
    
    draw.ellipse([cx - 8*s, face_y + 14*s, cx - 3*s, face_y + 19*s], fill=(50, 50, 50))
    draw.ellipse([cx + 3*s, face_y + 14*s, cx + 8*s, face_y + 19*s], fill=(50, 50, 50))
    
    hat_y = base_y - 4*s
    draw.pieslice([cx - 22*s, hat_y, cx + 22*s, hat_y + 24*s],
                  180, 360, fill=(93, 64, 55))
    draw.rectangle([cx - 28*s, hat_y + 18*s, cx + 28*s, hat_y + 24*s], fill=(93, 64, 55))

def draw_elevator_closed(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 40*s, cy - 50*s, cx + 40*s, cy + 50*s],
                    radius=6*s, fill=hex_to_rgb('#607D8B'), outline=(55, 71, 79), width=4)
    
    draw.rectangle([cx - 34*s, cy - 44*s, cx - 2*s, cy + 44*s], fill=hex_to_rgb('#90A4AE'))
    draw.rectangle([cx + 2*s, cy - 44*s, cx + 34*s, cy + 44*s], fill=hex_to_rgb('#90A4AE'))
    
    draw.line([cx, cy - 44*s, cx, cy + 44*s], fill=(69, 90, 100), width=3)
    
    draw.ellipse([cx - 8*s, cy - 58*s, cx + 8*s, cy - 42*s],
                 fill=hex_to_rgb('#FFC107'), outline=(255, 143, 0), width=2)

def draw_elevator_open(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 40*s, cy - 50*s, cx + 40*s, cy + 50*s],
                    radius=6*s, fill=hex_to_rgb('#607D8B'), outline=(55, 71, 79), width=4)
    
    draw.rectangle([cx - 34*s, cy - 44*s, cx + 34*s, cy + 44*s], fill=(38, 50, 56))
    
    draw.rectangle([cx - 44*s, cy - 44*s, cx - 30*s, cy + 44*s], fill=hex_to_rgb('#90A4AE'))
    draw.rectangle([cx + 30*s, cy - 44*s, cx + 44*s, cy + 44*s], fill=hex_to_rgb('#90A4AE'))
    
    draw.ellipse([cx - 8*s, cy - 58*s, cx + 8*s, cy - 42*s],
                 fill=hex_to_rgb('#FFC107'))
    
    draw.ellipse([cx - 14*s, cy - 5*s, cx + 14*s, cy + 23*s], fill=(255, 218, 185))

def draw_minecart_empty(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE * 0.55
    s = SPRITE_SIZE / 128
    
    draw.polygon([
        (cx - 40*s, cy - 18*s),
        (cx - 32*s, cy + 20*s),
        (cx + 32*s, cy + 20*s),
        (cx + 40*s, cy - 18*s)
    ], fill=hex_to_rgb('#E53935'), outline=(183, 28, 28), width=3)
    
    draw.rectangle([cx - 40*s, cy - 24*s, cx + 40*s, cy - 16*s], fill=(183, 28, 28))
    
    draw.ellipse([cx - 28*s, cy + 18*s, cx - 8*s, cy + 38*s], fill=(50, 50, 50))
    draw.ellipse([cx + 8*s, cy + 18*s, cx + 28*s, cy + 38*s], fill=(50, 50, 50))
    draw.ellipse([cx - 22*s, cy + 24*s, cx - 14*s, cy + 32*s], fill=(100, 100, 100))
    draw.ellipse([cx + 14*s, cy + 24*s, cx + 22*s, cy + 32*s], fill=(100, 100, 100))

def draw_minecart_full(img, x, y):
    draw_minecart_empty(img, x, y)
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE * 0.38
    s = SPRITE_SIZE / 128
    
    for i in range(5):
        ox = cx - 28*s + i * 14*s
        oy = cy - (i % 2) * 10*s
        draw.polygon([
            (ox, oy - 14*s),
            (ox + 10*s, oy - 4*s),
            (ox + 7*s, oy + 12*s),
            (ox - 7*s, oy + 12*s),
            (ox - 10*s, oy - 4*s)
        ], fill=hex_to_rgb('#FFD700'), outline=(255, 160, 0), width=2)

def draw_pickaxe_iron(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.rectangle([cx - 5*s, cy - 15*s, cx + 5*s, cy + 50*s],
                   fill=(139, 69, 19), outline=(93, 64, 55), width=2)
    
    draw.polygon([
        (cx - 35*s, cy - 25*s),
        (cx + 35*s, cy - 25*s),
        (cx + 25*s, cy - 8*s),
        (cx - 25*s, cy - 8*s)
    ], fill=hex_to_rgb('#B0BEC5'), outline=(69, 90, 100), width=3)

def draw_pickaxe_gold(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.rectangle([cx - 5*s, cy - 15*s, cx + 5*s, cy + 50*s],
                   fill=(139, 69, 19), outline=(93, 64, 55), width=2)
    
    draw.polygon([
        (cx - 35*s, cy - 25*s),
        (cx + 35*s, cy - 25*s),
        (cx + 25*s, cy - 8*s),
        (cx - 25*s, cy - 8*s)
    ], fill=hex_to_rgb('#FFD700'), outline=(255, 143, 0), width=3)

def draw_ore(img, x, y, main_color, dark_color):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.polygon([
        (cx, cy - 42*s),
        (cx + 38*s, cy - 14*s),
        (cx + 30*s, cy + 34*s),
        (cx - 30*s, cy + 34*s),
        (cx - 38*s, cy - 14*s)
    ], fill=hex_to_rgb(main_color), outline=hex_to_rgb(dark_color), width=3)
    
    draw.ellipse([cx - 18*s, cy - 24*s, cx + 2*s, cy - 8*s],
                 fill=(255, 255, 255, 150))

def draw_icon_gold(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.ellipse([cx - 45*s, cy - 45*s, cx + 45*s, cy + 45*s],
                 fill=hex_to_rgb('#FFD700'), outline=(230, 81, 0), width=5)
    
    draw.ellipse([cx - 30*s, cy - 35*s, cx - 5*s, cy - 10*s],
                 fill=(255, 245, 157))
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(45*s))
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), '$', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 3), '$', fill=(183, 28, 28), font=font)

def draw_icon_gem(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.polygon([
        (cx, cy - 45*s),
        (cx + 42*s, cy - 12*s),
        (cx + 24*s, cy + 42*s),
        (cx - 24*s, cy + 42*s),
        (cx - 42*s, cy - 12*s)
    ], fill=hex_to_rgb('#29B6F6'), outline=(1, 87, 155), width=3)
    
    draw.line([cx, cy - 45*s, cx, cy + 42*s], fill=(255, 255, 255, 100), width=2)
    draw.line([cx - 42*s, cy - 12*s, cx + 42*s, cy - 12*s], fill=(255, 255, 255, 100), width=2)
    
    draw.ellipse([cx - 20*s, cy - 25*s, cx - 2*s, cy - 8*s],
                 fill=(255, 255, 255, 160))

def draw_icon_cash(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 50*s, cy - 30*s, cx + 50*s, cy + 30*s],
                    radius=7*s, fill=hex_to_rgb('#4CAF50'), outline=(27, 94, 32), width=4)
    
    draw_round_rect(draw, [cx - 44*s, cy - 24*s, cx + 44*s, cy + 24*s],
                    radius=5*s, fill=hex_to_rgb('#81C784'))
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(38*s))
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), '$', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 2), '$', fill=(27, 94, 32), font=font)

def draw_icon_settings(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    points = []
    for i in range(16):
        angle = (i * math.pi / 8)
        r = 45*s if i % 2 == 0 else 32*s
        px = cx + math.cos(angle) * r
        py = cy + math.sin(angle) * r
        points.append((px, py))
    draw.polygon(points, fill=hex_to_rgb('#90A4AE'), outline=(55, 71, 79), width=3)
    
    draw.ellipse([cx - 18*s, cy - 18*s, cx + 18*s, cy + 18*s], fill=(38, 50, 56))
    draw.ellipse([cx - 10*s, cy - 10*s, cx + 10*s, cy + 10*s], fill=hex_to_rgb('#607D8B'))

def draw_icon_music(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.line([cx - 12*s, cy + 35*s, cx - 12*s, cy - 25*s], fill=(74, 20, 140), width=5)
    draw.line([cx + 18*s, cy + 30*s, cx + 18*s, cy - 35*s], fill=(74, 20, 140), width=5)
    
    draw.ellipse([cx - 30*s, cy - 40*s, cx + 6*s, cy - 18*s],
                 fill=hex_to_rgb('#E1BEE7'), outline=(74, 20, 140), width=3)
    draw.ellipse([cx + 0, cy - 50*s, cx + 36*s, cy - 28*s],
                 fill=hex_to_rgb('#E1BEE7'), outline=(74, 20, 140), width=3)
    
    draw.ellipse([cx - 25*s, cy + 25*s, cx - 5*s, cy + 42*s], fill=(74, 20, 140))
    draw.ellipse([cx + 5*s, cy + 20*s, cx + 25*s, cy + 37*s], fill=(74, 20, 140))

def draw_icon_elevator(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 34*s, cy - 42*s, cx + 34*s, cy + 42*s],
                    radius=6*s, fill=hex_to_rgb('#78909C'), outline=(55, 71, 79), width=4)
    
    draw.rectangle([cx - 28*s, cy - 36*s, cx - 2*s, cy + 36*s], fill=hex_to_rgb('#B0BEC5'))
    draw.rectangle([cx + 2*s, cy - 36*s, cx + 28*s, cy + 36*s], fill=hex_to_rgb('#B0BEC5'))
    
    draw.line([cx, cy - 36*s, cx, cy + 36*s], fill=(69, 90, 100), width=2)
    
    draw.polygon([
        (cx - 12*s, cy - 52*s),
        (cx + 12*s, cy - 52*s),
        (cx, cy - 64*s)
    ], fill=hex_to_rgb('#FFC107'))

def draw_icon_factory(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.rectangle([cx - 45*s, cy - 8*s, cx + 45*s, cy + 48*s],
                   fill=hex_to_rgb('#FF8A65'), outline=(191, 54, 12), width=3)
    
    draw.rectangle([cx - 35*s, cy + 5*s, cx - 18*s, cy + 28*s], fill=hex_to_rgb('#FFAB91'))
    draw.rectangle([cx + 18*s, cy + 5*s, cx + 35*s, cy + 28*s], fill=hex_to_rgb('#FFAB91'))
    
    draw.rectangle([cx - 30*s, cy - 42*s, cx - 15*s, cy - 8*s], fill=hex_to_rgb('#E64A19'))
    draw.rectangle([cx + 15*s, cy - 42*s, cx + 30*s, cy - 8*s], fill=hex_to_rgb('#E64A19'))
    
    draw.ellipse([cx - 36*s, cy - 52*s, cx - 18*s, cy - 36*s], fill=(158, 158, 158, 150))
    draw.ellipse([cx + 18*s, cy - 52*s, cx + 36*s, cy - 36*s], fill=(158, 158, 158, 150))

def draw_icon_mountain(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.polygon([
        (cx - 55*s, cy + 42*s),
        (cx - 18*s, cy - 30*s),
        (cx + 5*s, cy + 12*s),
        (cx + 30*s, cy - 42*s),
        (cx + 55*s, cy + 42*s)
    ], fill=hex_to_rgb('#6D4C41'), outline=(62, 39, 35), width=3)
    
    draw.polygon([
        (cx - 26*s, cy - 18*s),
        (cx - 18*s, cy - 30*s),
        (cx - 10*s, cy - 18*s)
    ], fill=(236, 239, 241))
    
    draw.polygon([
        (cx + 22*s, cy - 30*s),
        (cx + 30*s, cy - 42*s),
        (cx + 38*s, cy - 30*s)
    ], fill=(236, 239, 241))
    
    draw.polygon([
        (cx - 55*s, cy + 42*s),
        (cx - 25*s, cy + 18*s),
        (cx, cy + 35*s),
        (cx + 55*s, cy + 42*s)
    ], fill=hex_to_rgb('#4CAF50'))

def draw_icon_lock(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 34*s, cy - 8*s, cx + 34*s, cy + 52*s],
                    radius=7*s, fill=hex_to_rgb('#FFC107'), outline=(255, 143, 0), width=4)
    
    draw.arc([cx - 22*s, cy - 32*s, cx + 22*s, cy + 8*s], 180, 360, fill=(255, 143, 0), width=5)
    
    draw.ellipse([cx - 8*s, cy + 16*s, cx + 8*s, cy + 32*s], fill=(255, 143, 0))
    draw.rectangle([cx - 3*s, cy + 28*s, cx + 3*s, cy + 42*s], fill=(255, 143, 0))

def draw_icon_check(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.ellipse([cx - 45*s, cy - 45*s, cx + 45*s, cy + 45*s],
                 fill=hex_to_rgb('#4CAF50'), outline=(27, 94, 32), width=3)
    
    draw.line([cx - 24*s, cy + 5*s, cx - 6*s, cy + 24*s],
              fill='white', width=8)
    draw.line([cx - 6*s, cy + 24*s, cx + 28*s, cy - 16*s],
              fill='white', width=8)

def draw_icon_star(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_star(draw, cx, cy, 45*s, 20*s, 5, hex_to_rgb('#FFD700'))
    
    draw_star(draw, cx, cy, 45*s, 20*s, 5, None)

def draw_tower(img, x, y, main_color, dark_color):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.92
    s = SPRITE_SIZE / 128
    
    tower_top = base_y - 85*s
    draw.rectangle([cx - 26*s, tower_top, cx + 26*s, base_y],
                   fill=hex_to_rgb(main_color), outline=hex_to_rgb(dark_color), width=3)
    
    draw.rectangle([cx - 32*s, tower_top - 8*s, cx + 32*s, tower_top],
                   fill=hex_to_rgb(dark_color))
    
    draw.polygon([
        (cx - 32*s, tower_top - 8*s),
        (cx, tower_top - 38*s),
        (cx + 32*s, tower_top - 8*s)
    ], fill=hex_to_rgb('#E53935'), outline=(183, 28, 28), width=2)
    
    win1_y = tower_top + 12*s
    draw_round_rect(draw, [cx - 14*s, win1_y, cx + 14*s, win1_y + 20*s],
                    radius=3*s, fill=(255, 249, 196), outline=(251, 192, 45), width=2)
    
    win2_y = tower_top + 42*s
    draw_round_rect(draw, [cx - 14*s, win2_y, cx + 14*s, win2_y + 20*s],
                    radius=3*s, fill=(255, 249, 196), outline=(251, 192, 45), width=2)
    
    draw.rectangle([cx - 2*s, tower_top - 45*s, cx + 2*s, tower_top - 15*s], fill=(93, 64, 55))
    
    draw.polygon([
        (cx, tower_top - 52*s),
        (cx + 16*s, tower_top - 46*s),
        (cx, tower_top - 40*s)
    ], fill=hex_to_rgb('#E53935'))

def draw_elevator_top(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    base_y = y + SPRITE_SIZE * 0.88
    s = SPRITE_SIZE / 128
    
    build_top = base_y - 48*s
    draw.rectangle([cx - 36*s, build_top, cx + 36*s, base_y],
                   fill=hex_to_rgb('#8D6E63'), outline=(78, 52, 46), width=3)
    
    draw.rectangle([cx - 30*s, build_top + 8*s, cx + 30*s, build_top + 18*s],
                   fill=hex_to_rgb('#A1887F'))
    draw.rectangle([cx - 30*s, build_top + 28*s, cx + 30*s, build_top + 38*s],
                   fill=hex_to_rgb('#A1887F'))
    
    draw.pieslice([cx - 22*s, build_top - 30*s, cx + 22*s, build_top + 8*s],
                  180, 360, fill=hex_to_rgb('#5D4037'), outline=(62, 39, 35), width=2)
    
    draw.ellipse([cx - 6*s, build_top - 12*s, cx + 6*s, build_top],
                 fill=(255, 235, 59))

def draw_mine_tunnel(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_round_rect(draw, [cx - 48*s, cy - 42*s, cx + 48*s, cy + 42*s],
                    radius=10*s, fill=hex_to_rgb('#5D4037'))
    
    draw_round_rect(draw, [cx - 36*s, cy - 30*s, cx + 36*s, cy + 36*s],
                    radius=8*s, fill=(38, 50, 56))
    
    draw.arc([cx - 36*s, cy - 36*s, cx + 36*s, cy + 24*s], 180, 360,
             fill=hex_to_rgb('#8D6E63'), width=5)
    draw.line([cx - 36*s, cy - 6*s, cx - 36*s, cy + 30*s], fill=hex_to_rgb('#8D6E63'), width=5)
    draw.line([cx + 36*s, cy - 6*s, cx + 36*s, cy + 30*s], fill=hex_to_rgb('#8D6E63'), width=5)
    
    draw.ellipse([cx - 6*s, cy - 22*s, cx + 6*s, cy - 10*s], fill=(255, 235, 59))

def draw_mine_lamp(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    top_y = y + SPRITE_SIZE * 0.1
    s = SPRITE_SIZE / 128
    
    draw.line([cx, top_y, cx, top_y + 25*s], fill=(93, 64, 55), width=3)
    
    lamp_cy = top_y + 45*s
    draw.ellipse([cx - 18*s, lamp_cy - 18*s, cx + 18*s, lamp_cy + 18*s],
                 fill=hex_to_rgb('#FFC107'), outline=(255, 143, 0), width=3)
    
    draw.ellipse([cx - 8*s, lamp_cy - 8*s, cx + 8*s, lamp_cy + 8*s],
                 fill=(255, 255, 200))
    
    for r in range(45, 20, -5):
        alpha = int(80 * (45 - r) / 25)
        draw.ellipse([cx - r*s, lamp_cy - r*s, cx + r*s, lamp_cy + r*s],
                     outline=(255, 235, 59, alpha), width=2)

def draw_flag_red(img, x, y):
    draw = ImageDraw.Draw(img)
    pole_x = x + SPRITE_SIZE * 0.3
    top_y = y + SPRITE_SIZE * 0.12
    s = SPRITE_SIZE / 128
    
    draw.rectangle([pole_x - 2*s, top_y, pole_x + 2*s, top_y + 65*s],
                   fill=(93, 64, 55))
    
    draw.polygon([
        (pole_x + 2*s, top_y + 2*s),
        (pole_x + 42*s, top_y + 14*s),
        (pole_x + 2*s, top_y + 30*s)
    ], fill=hex_to_rgb('#E53935'), outline=(183, 28, 28), width=2)

def draw_mining_effect_1(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_star(draw, cx, cy - 25*s, 18*s, 8*s, 5, hex_to_rgb('#FFD700'))
    draw_star(draw, cx - 25*s, cy + 12*s, 12*s, 5*s, 5, hex_to_rgb('#FF9800'))
    draw_star(draw, cx + 22*s, cy + 18*s, 14*s, 6*s, 5, hex_to_rgb('#FFEB3B'))

def draw_mining_effect_2(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw_star(draw, cx, cy, 30*s, 14*s, 5, hex_to_rgb('#FFD700'))
    draw_star(draw, cx - 30*s, cy - 18*s, 14*s, 6*s, 5, hex_to_rgb('#FF5722'))
    draw_star(draw, cx + 26*s, cy - 12*s, 16*s, 7*s, 5, hex_to_rgb('#FFEB3B'))
    draw_star(draw, cx - 18*s, cy + 24*s, 12*s, 5*s, 5, hex_to_rgb('#FFC107'))
    draw_star(draw, cx + 24*s, cy + 22*s, 13*s, 5*s, 5, hex_to_rgb('#FF9800'))

def draw_mining_effect_3(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    for r in range(55, 20, -8):
        alpha = int(200 * (55 - r) / 35)
        draw.ellipse([cx - r*s, cy - r*s, cx + r*s, cy + r*s],
                     outline=(255, 235, 59, alpha), width=3)
    
    draw_star(draw, cx, cy, 22*s, 10*s, 5, (255, 255, 255))

def draw_gold_effect_1(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    def coin(dx, dy, r):
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=hex_to_rgb('#FFD700'), outline=(230, 81, 0), width=2)
    
    coin(0, 0, 32*s)
    coin(-28*s, -18*s, 20*s)
    coin(26*s, -14*s, 24*s)

def draw_gold_effect_2(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    def coin(dx, dy, r):
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=hex_to_rgb('#FFD700'), outline=(230, 81, 0), width=2)
    
    coin(0, -12*s, 26*s)
    coin(-32*s, 6*s, 18*s)
    coin(28*s, 10*s, 22*s)
    coin(-12*s, 28*s, 16*s)
    coin(18*s, 32*s, 14*s)

def draw_sparkle_effect(img, x, y):
    draw = ImageDraw.Draw(img)
    cx = x + SPRITE_SIZE // 2
    cy = y + SPRITE_SIZE // 2
    s = SPRITE_SIZE / 128
    
    draw.polygon([
        (cx, cy - 42*s),
        (cx + 10*s, cy - 10*s),
        (cx + 42*s, cy),
        (cx + 10*s, cy + 10*s),
        (cx, cy + 42*s),
        (cx - 10*s, cy + 10*s),
        (cx - 42*s, cy),
        (cx - 10*s, cy - 10*s)
    ], fill=(255, 255, 255, 220))
    
    draw_star(draw, cx, cy, 18*s, 8*s, 5, hex_to_rgb('#FFEB3B'))

SPRITE_DEFS = [
    ("miner_idle", 0, 0, lambda img, x, y: draw_miner_idle(img, x, y)),
    ("miner_mining", 0, 1, lambda img, x, y: draw_miner_mining(img, x, y)),
    ("miner_walk", 0, 2, lambda img, x, y: draw_miner_idle(img, x, y)),
    ("miner2_idle", 0, 3, lambda img, x, y: draw_miner_idle(img, x, y, '#FF9800', '#4CAF50')),
    ("miner2_mining", 0, 4, lambda img, x, y: draw_miner_mining(img, x, y, '#FF9800', '#4CAF50')),
    ("miner3_idle", 0, 5, lambda img, x, y: draw_miner_idle(img, x, y, '#E91E63', '#795548')),
    
    ("elevator_worker_idle", 1, 0, draw_elevator_worker),
    ("elevator_worker_working", 1, 1, draw_elevator_worker),
    ("ground_worker_idle", 1, 2, draw_ground_worker),
    ("ground_worker_pushing", 1, 3, lambda img, x, y: (draw_ground_worker(img, x-8, y), draw_minecart_empty(img, x+20, y+10))),
    ("supervisor_miner", 1, 4, draw_supervisor),
    ("supervisor_elevator", 1, 5, lambda img, x, y: draw_supervisor(img, x, y, '#2196F3')),
    
    ("elevator_closed", 2, 0, draw_elevator_closed),
    ("elevator_open", 2, 1, draw_elevator_open),
    ("minecart_empty", 2, 2, draw_minecart_empty),
    ("minecart_full", 2, 3, draw_minecart_full),
    ("pickaxe_iron", 2, 4, draw_pickaxe_iron),
    ("pickaxe_gold", 2, 5, draw_pickaxe_gold),
    
    ("ore_gold", 3, 0, lambda img, x, y: draw_ore(img, x, y, '#FFD700', '#FFA000')),
    ("ore_copper", 3, 1, lambda img, x, y: draw_ore(img, x, y, '#FF8A65', '#E64A19')),
    ("ore_silver", 3, 2, lambda img, x, y: draw_ore(img, x, y, '#E0E0E0', '#9E9E9E')),
    ("ore_diamond", 3, 3, lambda img, x, y: draw_ore(img, x, y, '#64B5F6', '#1976D2')),
    ("ore_ruby", 3, 4, lambda img, x, y: draw_ore(img, x, y, '#EF5350', '#C62828')),
    ("ore_emerald", 3, 5, lambda img, x, y: draw_ore(img, x, y, '#66BB6A', '#2E7D32')),
    
    ("icon_gold", 4, 0, draw_icon_gold),
    ("icon_gem", 4, 1, draw_icon_gem),
    ("icon_cash", 4, 2, draw_icon_cash),
    ("icon_settings", 4, 3, draw_icon_settings),
    ("icon_music", 4, 4, draw_icon_music),
    ("icon_pickaxe", 4, 5, lambda img, x, y: draw_pickaxe_iron(img, x+8, y-4)),
    
    ("icon_elevator", 5, 0, draw_icon_elevator),
    ("icon_factory", 5, 1, draw_icon_factory),
    ("icon_mountain", 5, 2, draw_icon_mountain),
    ("icon_lock", 5, 3, draw_icon_lock),
    ("icon_check", 5, 4, draw_icon_check),
    ("icon_star", 5, 5, draw_icon_star),
    
    ("tower_blue", 6, 0, lambda img, x, y: draw_tower(img, x, y, '#42A5F5', '#1565C0')),
    ("tower_green", 6, 1, lambda img, x, y: draw_tower(img, x, y, '#66BB6A', '#2E7D32')),
    ("elevator_top", 6, 2, draw_elevator_top),
    ("mine_tunnel", 6, 3, draw_mine_tunnel),
    ("mine_lamp", 6, 4, draw_mine_lamp),
    ("flag_red", 6, 5, draw_flag_red),
    
    ("effect_mining_1", 7, 0, draw_mining_effect_1),
    ("effect_mining_2", 7, 1, draw_mining_effect_2),
    ("effect_mining_3", 7, 2, draw_mining_effect_3),
    ("effect_gold_1", 7, 3, draw_gold_effect_1),
    ("effect_gold_2", 7, 4, draw_gold_effect_2),
    ("effect_sparkle", 7, 5, draw_sparkle_effect),
]

def main():
    print("=" * 60)
    print("生成游戏精灵图...")
    print("=" * 60)
    
    sprite_sheet = Image.new('RGBA', (COLS * SPRITE_SIZE, ROWS * SPRITE_SIZE), (0, 0, 0, 0))
    sprite_map = {}
    
    for key, row, col, draw_fn in SPRITE_DEFS:
        x = col * SPRITE_SIZE
        y = row * SPRITE_SIZE
        
        cell = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
        draw_fn(cell, 0, 0)
        
        sprite_sheet.paste(cell, (x, y), cell)
        
        sprite_map[key] = {
            "x": x, "y": y,
            "width": SPRITE_SIZE, "height": SPRITE_SIZE,
            "row": row, "col": col
        }
        print(f"  ✓ {key} -> ({row}, {col})")
    
    sprite_path = os.path.join(OUTPUT_DIR, "sprites.png")
    sprite_sheet.save(sprite_path)
    print(f"\n精灵图已保存: {sprite_path}")
    print(f"尺寸: {COLS * SPRITE_SIZE} x {ROWS * SPRITE_SIZE}")
    
    import json
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

#!/usr/bin/env python3
"""
游戏精灵图生成器
- 使用AI生成所有游戏图片资源
- 合并成一张PNG精灵图
- 生成CSS映射文件
"""

import os
import requests
import time
from PIL import Image
from io import BytesIO
import json

BASE_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
OUTPUT_DIR = "/workspace/miner_tycoon/frontend/assets"
SPRITE_SIZE = 128
COLS = 6
ROWS = 8

os.makedirs(OUTPUT_DIR, exist_ok=True)

SPRITE_DEFS = [
    {"key": "miner_idle", "prompt": "2D cartoon cute miner character idle pose yellow hard hat blue overalls holding pickaxe side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 0},
    {"key": "miner_mining", "prompt": "2D cartoon cute miner character mining action swinging pickaxe yellow hard hat blue overalls side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 1},
    {"key": "miner_walk", "prompt": "2D cartoon cute miner character walking pose yellow hard hat blue overalls side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 2},
    {"key": "miner2_idle", "prompt": "2D cartoon cute miner character idle pose orange hard hat green overalls holding shovel side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 3},
    {"key": "miner2_mining", "prompt": "2D cartoon cute miner character digging action orange hard hat green overalls side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 4},
    {"key": "miner3_idle", "prompt": "2D cartoon cute miner character idle pose red hard hat brown overalls holding pickaxe side view chibi style transparent background game sprite", "size": "square_hd", "row": 0, "col": 5},

    {"key": "elevator_worker_idle", "prompt": "2D cartoon cute elevator operator worker idle orange hard hat blue uniform standing front view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 0},
    {"key": "elevator_worker_working", "prompt": "2D cartoon cute elevator operator worker pushing buttons orange hard hat blue uniform front view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 1},
    {"key": "ground_worker_idle", "prompt": "2D cartoon cute ground worker idle green shirt yellow hard hat standing side view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 2},
    {"key": "ground_worker_pushing", "prompt": "2D cartoon cute ground worker pushing mine cart green shirt yellow hard hat side view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 3},
    {"key": "supervisor_miner", "prompt": "2D cartoon cute mining supervisor manager with clipboard suit and hard hat side view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 4},
    {"key": "supervisor_elevator", "prompt": "2D cartoon cute elevator supervisor manager with clipboard suit and hard hat front view chibi style transparent background game sprite", "size": "square_hd", "row": 1, "col": 5},

    {"key": "elevator_closed", "prompt": "2D cartoon mine elevator cage with closed doors metal frame side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 0},
    {"key": "elevator_open", "prompt": "2D cartoon mine elevator cage with open doors metal frame side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 1},
    {"key": "minecart_empty", "prompt": "2D cartoon empty mine cart red metal with wheels side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 2},
    {"key": "minecart_full", "prompt": "2D cartoon mine cart full of gold ore red metal with wheels side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 3},
    {"key": "pickaxe_iron", "prompt": "2D cartoon iron pickaxe mining tool wooden handle side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 4},
    {"key": "pickaxe_gold", "prompt": "2D cartoon golden pickaxe mining tool shiny wooden handle side view chibi style transparent background game asset", "size": "square_hd", "row": 2, "col": 5},

    {"key": "ore_gold", "prompt": "2D cartoon gold ore chunk shiny yellow rock chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 0},
    {"key": "ore_copper", "prompt": "2D cartoon copper ore chunk orange brown rock chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 1},
    {"key": "ore_silver", "prompt": "2D cartoon silver ore chunk shiny gray rock chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 2},
    {"key": "ore_diamond", "prompt": "2D cartoon diamond gem blue crystal shiny chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 3},
    {"key": "ore_ruby", "prompt": "2D cartoon ruby gem red crystal shiny chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 4},
    {"key": "ore_emerald", "prompt": "2D cartoon emerald gem green crystal shiny chibi style transparent background game asset", "size": "square_hd", "row": 3, "col": 5},

    {"key": "icon_gold", "prompt": "2D cartoon gold coin icon with dollar sign shiny chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 0},
    {"key": "icon_gem", "prompt": "2D cartoon blue diamond gem icon shiny crystal chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 1},
    {"key": "icon_cash", "prompt": "2D cartoon green cash money bill icon chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 2},
    {"key": "icon_settings", "prompt": "2D cartoon gear settings icon gray metal chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 3},
    {"key": "icon_music", "prompt": "2D cartoon music note icon colorful chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 4},
    {"key": "icon_pickaxe", "prompt": "2D cartoon pickaxe icon mining tool chibi style transparent background game UI icon", "size": "square_hd", "row": 4, "col": 5},

    {"key": "icon_elevator", "prompt": "2D cartoon elevator icon lift chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 0},
    {"key": "icon_factory", "prompt": "2D cartoon factory building icon chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 1},
    {"key": "icon_mountain", "prompt": "2D cartoon mountain peak icon with snow chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 2},
    {"key": "icon_lock", "prompt": "2D cartoon padlock lock icon metal chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 3},
    {"key": "icon_check", "prompt": "2D cartoon green checkmark badge chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 4},
    {"key": "icon_star", "prompt": "2D cartoon golden star icon shiny chibi style transparent background game UI icon", "size": "square_hd", "row": 5, "col": 5},

    {"key": "tower_blue", "prompt": "2D cartoon blue mining tower building with red roof and window side view chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 0},
    {"key": "tower_green", "prompt": "2D cartoon green mining tower building with red roof and window side view chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 1},
    {"key": "elevator_top", "prompt": "2D cartoon mine elevator top building with red roof side view chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 2},
    {"key": "mine_tunnel", "prompt": "2D cartoon mine tunnel with wooden support beams side view chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 3},
    {"key": "mine_lamp", "prompt": "2D cartoon hanging mine lamp with warm yellow light glow chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 4},
    {"key": "flag_red", "prompt": "2D cartoon red flag on pole chibi style transparent background game asset", "size": "square_hd", "row": 6, "col": 5},

    {"key": "effect_mining_1", "prompt": "2D cartoon mining spark effect frame 1 stars and sparks chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 0},
    {"key": "effect_mining_2", "prompt": "2D cartoon mining spark effect frame 2 explosion stars chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 1},
    {"key": "effect_mining_3", "prompt": "2D cartoon mining spark effect frame 3 burst sparkles chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 2},
    {"key": "effect_gold_1", "prompt": "2D cartoon gold coin collect effect frame 1 shiny chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 3},
    {"key": "effect_gold_2", "prompt": "2D cartoon gold coin collect effect frame 2 sparkle chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 4},
    {"key": "effect_sparkle", "prompt": "2D cartoon sparkle effect star glitter chibi style transparent background game effect", "size": "square_hd", "row": 7, "col": 5},
]


def generate_image(prompt, size="square_hd"):
    """调用AI生成图片，等待生成完成"""
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{BASE_URL}?prompt={encoded_prompt}&image_size={size}"
    
    placeholder_signatures = [
        "The image is generating",
        "Please refresh",
        "generating",
    ]
    
    for main_attempt in range(5):
        try:
            print(f"  请求生成... (第 {main_attempt+1} 轮)")
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                try:
                    img = Image.open(BytesIO(response.content))
                    if is_placeholder(img, placeholder_signatures):
                        print(f"  图片还在生成中，等待 10 秒后重试...")
                        time.sleep(10)
                        continue
                    return img
                except:
                    pass
            else:
                print(f"  请求失败: {response.status_code}")
        except Exception as e:
            print(f"  错误: {e}")
        time.sleep(3)
    return None


def is_placeholder(img, signatures):
    """检测图片是否是生成中的占位符"""
    try:
        img_small = img.resize((50, 50))
        pixels = list(img_small.getdata())
        avg_brightness = sum(sum(p[:3]) for p in pixels) / len(pixels) / 3
        
        if avg_brightness > 220:
            return True
            
        if img.width < 100 or img.height < 100:
            return True
            
        return False
    except:
        return True


def make_transparent(img, bg_tolerance=30):
    """尝试将图片背景设为透明"""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    
    corners = [
        data[0],
        data[img.width - 1],
        data[img.width * (img.height - 1)],
        data[img.width * img.height - 1]
    ]
    
    avg_r = sum(c[0] for c in corners) / 4
    avg_g = sum(c[1] for c in corners) / 4
    avg_b = sum(c[2] for c in corners) / 4
    
    for pixel in data:
        r, g, b, a = pixel
        if (abs(r - avg_r) < bg_tolerance and 
            abs(g - avg_g) < bg_tolerance and 
            abs(b - avg_b) < bg_tolerance):
            new_data.append((r, g, b, 0))
        else:
            new_data.append(pixel)
    
    img.putdata(new_data)
    return img


def main():
    print("=" * 60)
    print("游戏精灵图生成器")
    print("=" * 60)
    
    total = len(SPRITE_DEFS)
    print(f"\n共需生成 {total} 张图片")
    print(f"精灵图尺寸: {COLS * SPRITE_SIZE} x {ROWS * SPRITE_SIZE}")
    print()
    
    sprite_sheet = Image.new('RGBA', (COLS * SPRITE_SIZE, ROWS * SPRITE_SIZE), (0, 0, 0, 0))
    sprite_map = {}
    failed = []
    
    for i, sprite in enumerate(SPRITE_DEFS):
        key = sprite["key"]
        row = sprite["row"]
        col = sprite["col"]
        
        print(f"[{i+1}/{total}] 生成: {key}")
        
        img = generate_image(sprite["prompt"], sprite["size"])
        
        if img:
            img = make_transparent(img)
            img = img.resize((SPRITE_SIZE, SPRITE_SIZE), Image.LANCZOS)
            
            x = col * SPRITE_SIZE
            y = row * SPRITE_SIZE
            sprite_sheet.paste(img, (x, y), img)
            
            sprite_map[key] = {
                "x": x, "y": y,
                "width": SPRITE_SIZE, "height": SPRITE_SIZE,
                "row": row, "col": col
            }
            print(f"  ✓ 成功 -> 位置 ({row}, {col})")
        else:
            failed.append(key)
            print(f"  ✗ 失败")
        
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"生成完成! 成功: {total - len(failed)}/{total}")
    if failed:
        print(f"失败: {failed}")
    
    sprite_path = os.path.join(OUTPUT_DIR, "sprites.png")
    sprite_sheet.save(sprite_path)
    print(f"\n精灵图已保存: {sprite_path}")
    
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
    print(f"映射文件已保存: {map_path}")
    
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
    
    print(f"CSS文件已保存: {css_path}")
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, '/workspace/miner_tycoon')
from create_cartoons import draw_miner, SPRITE_SIZE

img = Image.new('RGBA', (SPRITE_SIZE * 2, SPRITE_SIZE), (200, 200, 255, 255))
draw = ImageDraw.Draw(img)

# 左边一个用draw_miner
draw_miner(img, 0, 0, '#FFD700', '#4169E1', 'idle')

# 右边直接画一个矩形测试
draw.rectangle([SPRITE_SIZE + 20, 20, SPRITE_SIZE + 100, 100], fill=(255, 215, 0), outline='black')

img.save('/workspace/miner_tycoon/test_miner.png')
print("Saved test_miner.png")

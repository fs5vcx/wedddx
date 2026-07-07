#!/usr/bin/env python3
from PIL import Image

img = Image.open('/workspace/miner_tycoon/frontend/assets/sprites.png')

# 扫描第一个精灵，找到肤色像素
print("Scanning first sprite for skin color...")
for y in range(0, 128, 5):
    for x in range(0, 128, 5):
        p = img.getpixel((x, y))
        # 肤色大概是 R>200, G>180, B>150
        if p[0] > 200 and p[1] > 180 and p[2] > 150 and p[3] > 200:
            print(f"  Skin at ({x}, {y}): {p}")

print("\nScanning for yellow/gold color...")
for y in range(0, 128, 3):
    for x in range(0, 128, 3):
        p = img.getpixel((x, y))
        # 金色大概是 R>200, G>180, B<100
        if p[0] > 200 and p[1] > 180 and p[2] < 100 and p[3] > 200:
            print(f"  Gold at ({x}, {y}): {p}")

print("\nScanning for white color...")
for y in range(0, 128, 5):
    for x in range(0, 128, 5):
        p = img.getpixel((x, y))
        if p[0] > 240 and p[1] > 240 and p[2] > 240 and p[3] > 200:
            print(f"  White at ({x}, {y}): {p}")

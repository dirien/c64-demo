#!/usr/bin/env python3
"""Convert PNG to C64 sprite data (24x21 pixels, 63 bytes)"""

from PIL import Image

# Load image
img = Image.open('avatar-on-white.png')

# Convert to RGBA to properly detect non-white pixels
img = img.convert('RGBA')

# Get the bounding box of non-white content
# Find actual logo bounds (non-white pixels)
pixels = img.load()
min_x, min_y, max_x, max_y = img.width, img.height, 0, 0
for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = pixels[x, y]
        # Check if pixel is NOT white/near-white
        if r < 250 or g < 250 or b < 250:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

# Crop to content
if max_x > min_x and max_y > min_y:
    img = img.crop((min_x, min_y, max_x + 1, max_y + 1))

# Resize to fit in 24x21 while maintaining aspect ratio
img.thumbnail((24, 21), Image.Resampling.LANCZOS)

# Create a 24x21 canvas (white background)
canvas = Image.new('RGBA', (24, 21), (255, 255, 255, 255))
x_offset = (24 - img.width) // 2
y_offset = (21 - img.height) // 2
canvas.paste(img, (x_offset, y_offset), img if img.mode == 'RGBA' else None)

# Convert: any non-white pixel becomes a sprite pixel
pixels = canvas.load()
sprite_data = []

print("# C64 Sprite data - Pulumi logo (24x21 pixels)")
print("SPRITE_DATA = [")

for y in range(21):
    row_bytes = []
    for byte_idx in range(3):  # 3 bytes per row
        byte_val = 0
        for bit in range(8):
            x = byte_idx * 8 + bit
            if x < 24:
                r, g, b, a = pixels[x, y]
                # Non-white pixel = sprite pixel (threshold for anti-aliasing)
                if r < 245 or g < 245 or b < 245:
                    byte_val |= (1 << (7 - bit))
        row_bytes.append(byte_val)

    # Print as binary for visual clarity
    print(f"    0b{row_bytes[0]:08b}, 0b{row_bytes[1]:08b}, 0b{row_bytes[2]:08b},  # Row {y+1}")
    sprite_data.extend(row_bytes)

print("]")

# Also show ASCII art preview
print("\n# ASCII preview:")
for y in range(21):
    line = ""
    for x in range(24):
        r, g, b, a = pixels[x, y]
        line += "█" if (r < 245 or g < 245 or b < 245) else "."
    print(f"# {line}")

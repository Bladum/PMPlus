"""
Simple Sprite Sheet Splitter for XCOM units

Cuts units.png into individual 16x16 pixel sprites with 1 pixel offset
and 2 pixel spacing between units.
"""

from PIL import Image
import os

# Set the specific parameters for units.png
INPUT_FILE = r"C:\Users\TomaszBłądkowski\Videos\MOJE\XCOM\mods\xcom\gfx\units\units.png"
OUTPUT_DIR = r"C:\Users\TomaszBłądkowski\Videos\MOJE\XCOM\mods\xcom\gfx\units\split"
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
OFFSET_X = 1
OFFSET_Y = 1
SPACING = 2
PREFIX = "unit_"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    # Open the sprite sheet
    sheet = Image.open(INPUT_FILE)

    # Get sheet dimensions
    sheet_width, sheet_height = sheet.size

    # Calculate number of sprites in each row and column
    col_count = (sheet_width - OFFSET_X) // (SPRITE_WIDTH + SPACING)
    row_count = (sheet_height - OFFSET_Y) // (SPRITE_HEIGHT + SPACING)

    print(f"Found approximately {col_count}x{row_count} sprites in sheet")

    # Counter for naming files sequentially
    count = 1

    # Extract each sprite
    for row in range(row_count):
        for col in range(col_count):
            # Calculate the position of the current sprite
            left = OFFSET_X + col * (SPRITE_WIDTH + SPACING)
            upper = OFFSET_Y + row * (SPRITE_HEIGHT + SPACING)
            right = left + SPRITE_WIDTH
            lower = upper + SPRITE_HEIGHT

            # Extract the sprite
            sprite = sheet.crop((left, upper, right, lower))

            # Save the sprite with a formatted name (e.g., unit_001.png)
            output_filename = f"{PREFIX}{count:03d}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            sprite.save(output_path)

            print(f"Saved {output_filename} ({left},{upper} -> {right},{lower})")
            count += 1

    print(f"Successfully extracted {count-1} sprites from {INPUT_FILE}")

except Exception as e:
    print(f"Error splitting sprite sheet: {e}")


import os
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

# Constants
CELL_SIZE = 20
PADDING = 10
FONT_SIZE = 12

def load_game_states(folder_path):
    game_states = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                game_states[filename] = json.load(file)
    return game_states

def hex_darken(hex_color, factor=0.6):
    """Darken a hex color string (e.g., "#00FF00") by a factor."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return (r, g, b)

def draw_board(board, heuristic_value, filename, folder_path):
    height = board['height']
    width = board['width']
    img_width = width * CELL_SIZE + 2 * PADDING
    img_height = height * CELL_SIZE + 2 * PADDING + FONT_SIZE + PADDING

    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Draw food
    for food in board['food']:
        x, y = food['x'], food['y']
        y = height - 1 - y  # Flip Y-axis
        draw.ellipse([
            x * CELL_SIZE + PADDING,
            y * CELL_SIZE + PADDING,
            (x + 1) * CELL_SIZE + PADDING,
            (y + 1) * CELL_SIZE + PADDING
        ], fill='green')

    # Draw snakes
    for snake in board['snakes']:
        color = snake['customizations']['color']
        rgb_body = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # Convert "#RRGGBB" to (R, G, B)
        for i, segment in enumerate(snake['body']):
            x, y = segment['x'], segment['y']
            y = height - 1 - y  # Flip Y-axis

            rect = [
                x * CELL_SIZE + PADDING,
                y * CELL_SIZE + PADDING,
                (x + 1) * CELL_SIZE + PADDING,
                (y + 1) * CELL_SIZE + PADDING
            ]
            if i == 0:  # Head
                head_color = hex_darken(color)
                draw.rectangle(rect, fill=head_color, outline='black')
            else:
                draw.rectangle(rect, fill=rgb_body)

    # Draw border around board
    draw.rectangle(
        [PADDING, PADDING, width * CELL_SIZE + PADDING - 1, height * CELL_SIZE + PADDING - 1],
        outline="black",
        width=2
    )

    # Draw heuristic value
    draw.text(
        (PADDING, height * CELL_SIZE + 2 * PADDING),
        f"Heuristic: {heuristic_value}",
        font=font,
        fill='black'
    )

    # Save the image
    name = filename.split('.')[0]
    image.save(os.path.join(folder_path, name + ".png"))
    return image

def main(folder_path):
    game_states = load_game_states(folder_path)
    for filename, state in game_states.items():
        heuristic_value = state.get('heuristic_value', 'N/A')
        draw_board(state['board'], heuristic_value, filename, folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render Battlesnake boards from JSON files.")
    parser.add_argument("folder", help="Path to the folder containing game state JSON files")
    args = parser.parse_args()
    main(args.folder)

import os
from collections import deque
from PIL import Image, ImageDraw, ImageFont
import re

def parse_filename(filename):
    name = os.path.splitext(filename)[0]
    if "_" not in name:
        return None
    parts = name.split("_")
    if len(parts) < 2:
        return None
    try:
        depth = int(parts[0])
    except ValueError:
        return None
    action_str = parts[1]
    actions = action_str.split('-') if action_str else []
    return depth, actions

def build_tree_structure(image_files):
    tree = {}
    nodes = {}
    file_set = set(image_files)
    possible_actions = ["down", "up", "left", "right"]

    # Find root file, which should be "{depth}___.png"
    
    root_filename = None
    for filename in file_set:
        if re.match(r'^\d+__\.png$', filename):
            root_filename = filename
            break

    if root_filename is None:
        raise ValueError("No root file matching pattern '<depth>___.png' found in image_files")



    # Start BFS from root
    queue = deque()
    root_depth = int(root_filename.split("_")[0])
    root_actions = []
    root_id = f"{root_depth}_"
    nodes[root_id] = root_filename
    tree["root"] = [(root_id, "root")]
    queue.append((root_depth, root_actions))

    while queue:
        depth, actions = queue.popleft()
        current_actions_str = "-".join(actions)
        current_id = f"{depth}_{current_actions_str}_" if current_actions_str else f"{depth}_"

        for action in possible_actions:
            new_actions = actions + [action]
            new_actions_str = "-".join(new_actions)
            new_depth = depth - 1  # Depth decreases as we move from root
            new_filename = f"{new_depth}_{new_actions_str}_.png"
            new_id = f"{new_depth}_{new_actions_str}_"

            if new_filename in file_set:
                tree.setdefault(current_id, []).append((new_id, action))
                nodes[new_id] = new_filename
                queue.append((new_depth, new_actions))

    return tree, nodes

def create_composite_image(tree, nodes, folder, spacing=(40, 80)):
    from math import atan2, cos, sin, pi

    def draw_arrow(draw, x0, y0, x1, y1, label=None):
        draw.line((x0, y0, x1, y1), fill="black", width=2)

        # Arrowhead
        angle = atan2(y1 - y0, x1 - x0)
        arrow_length = 10
        arrow_angle = pi / 6  # 30 degrees

        x2 = x1 - arrow_length * cos(angle - arrow_angle)
        y2 = y1 - arrow_length * sin(angle - arrow_angle)
        x3 = x1 - arrow_length * cos(angle + arrow_angle)
        y3 = y1 - arrow_length * sin(angle + arrow_angle)

        draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill="black")

        # Label
        if label:
            mx, my = (x0 + x1) // 2, (y0 + y1) // 2
            draw.text((mx + 5, my - 10), label, fill="black", font=font)

    # Load images to determine exact sizes
    images = {}
    for node_id, filename in nodes.items():
        img = Image.open(os.path.join(folder, filename))
        images[node_id] = img

    # Layout by depth
    levels = {}
    for node_id in nodes:
        depth = int(node_id.split("_")[0])
        levels.setdefault(depth, []).append(node_id)

    max_width = max(len(n) for n in levels.values())
    img_w, img_h = next(iter(images.values())).size  # assume consistent size
    space_x, space_y = spacing

    canvas_width = max_width * (img_w + space_x)
    canvas_height = (max(levels.keys()) + 1) * (img_h + space_y)

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Font
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    positions = {}

    # Place images without resizing
    for depth in sorted(levels):
        nodes_at_level = levels[depth]
        x_offset = (canvas_width - len(nodes_at_level) * (img_w + space_x)) // 2
        for i, node_id in enumerate(nodes_at_level):
            x = x_offset + i * (img_w + space_x)
            y = depth * (img_h + space_y)
            canvas.paste(images[node_id], (x, y))
            
            # Draw border around the image
            node_has_children = node_id in tree
            border_color = "black" if node_has_children else "red"

            # Draw border around the image
            draw.rectangle(
                [x, y, x + img_w - 1, y + img_h - 1],
                outline=border_color,
                width=2
            )

            positions[node_id] = (x + img_w // 2, y + img_h // 2)

    # Draw arrows
    for parent, children in tree.items():
        if parent == "root":
            continue
        for child_id, action in children:
            if parent not in positions or child_id not in positions:
                continue
            x0, y0 = positions[parent]
            x1, y1 = positions[child_id]

            # Offset arrows from image edges (center → edge)
            dx, dy = x1 - x0, y1 - y0
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx /= dist
                dy /= dist
                offset = img_h // 2 - 5
                x0 += int(dx * offset)
                y0 += int(dy * offset)
                x1 -= int(dx * offset)
                y1 -= int(dy * offset)

            draw_arrow(draw, x0, y0, x1, y1, label=action)

    return canvas



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to folder with PNGs")
    parser.add_argument("--output", default="tree_output.png", help="Output image file")
    args = parser.parse_args()

    files = sorted([f for f in os.listdir(args.folder) if f.endswith(".png")])
    tree, nodes = build_tree_structure(files)
    print(tree)
    print(nodes)
    final_image = create_composite_image(tree, nodes, args.folder)
    final_image.save(args.output)
    print(f"Saved composite to {args.output}")

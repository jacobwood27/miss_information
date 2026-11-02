import json
import cairo
import os

# Load the JSON data
with open('sheet.json', 'r') as f:
    questions = json.load(f)

# Directory for background images
background_images_dir = 'images/questions'  # Update this path

def draw_text_with_background(ctx, text, x, y, max_width, font_size, padding=10, bg_color=(0, 0, 0, 0.6), text_color=(1, 1, 1), shadow_color=(0, 0, 0, 0.5), corner_radius=10):
    ctx.set_font_size(font_size)
    words = text.split()
    lines = []
    line = ''

    # Wrap text
    for word in words:
        test_line = f"{line} {word}".strip()
        (xbearing, ybearing, width, height, xadvance, yadvance) = ctx.text_extents(test_line)
        if width > max_width:
            lines.append(line)
            line = word
        else:
            line = test_line
    lines.append(line)

    # Calculate background rectangle size
    line_height = font_size * 1.5
    text_width = max(ctx.text_extents(line)[4] for line in lines)
    text_height = line_height * len(lines)
    bg_width = text_width + padding * 2
    bg_height = text_height + padding * 2

    # Draw rounded rectangle background
    ctx.set_source_rgba(*bg_color)
    draw_rounded_rectangle(ctx, x - padding, y - padding, bg_width, bg_height, corner_radius)
    ctx.fill()

    # Draw text shadow
    ctx.set_source_rgba(*shadow_color)
    y_offset = y
    for line in lines:
        ctx.move_to(x + 2, y_offset + line_height * 0.8 + 2)  # Shadow offset
        ctx.show_text(line)
        y_offset += line_height

    # Draw text
    ctx.set_source_rgb(*text_color)
    y_offset = y
    for line in lines:
        ctx.move_to(x, y_offset + line_height * 0.8)
        ctx.show_text(line)
        y_offset += line_height

def draw_rounded_rectangle(ctx, x, y, width, height, radius):
    ctx.arc(x + width - radius, y + radius, radius, -0.5 * 3.14, 0)
    ctx.arc(x + width - radius, y + height - radius, radius, 0, 0.5 * 3.14)
    ctx.arc(x + radius, y + height - radius, radius, 0.5 * 3.14, 3.14)
    ctx.arc(x + radius, y + radius, radius, 3.14, 1.5 * 3.14)
    ctx.close_path()

# Create card images for the first 3 questions
for i, q in enumerate(questions[:3]):
    background_image_path = os.path.join(background_images_dir, f'{q["id"]}.png')

    if not os.path.exists(background_image_path):
        print(f"Background image {background_image_path} not found. Skipping card {i+1}.")
        continue

    background_image = cairo.ImageSurface.create_from_png(background_image_path)
    card = cairo.ImageSurface(cairo.FORMAT_ARGB32, background_image.get_width(), background_image.get_height())
    ctx = cairo.Context(card)

    # Draw background image
    ctx.set_source_surface(background_image, 0, 0)
    ctx.paint()

    # Set up text properties
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    # Draw the question with background and shadow
    question_x, question_y = 50, 50
    max_width = card.get_width() - 100  # Margins
    draw_text_with_background(ctx, q["question"], question_x, question_y, max_width, 40, padding=20, bg_color=(0, 0, 0, 0.7), text_color=(1, 1, 1), shadow_color=(0, 0, 0, 0.5), corner_radius=10)

    # Draw the range with background and shadow
    range_text = q.get("range1", "")
    range_x, range_y = 50, card.get_height() - 100
    draw_text_with_background(ctx, range_text, range_x, range_y, max_width, 30, padding=15, bg_color=(0, 0, 0, 0.7), text_color=(1, 1, 1), shadow_color=(0, 0, 0, 0.5), corner_radius=10)

    # Save the card
    card_output_path = f'card_{i+1}.png'
    card.write_to_png(card_output_path)
    print(f"Card {i+1} created successfully and saved as {card_output_path}.")

print("First 3 cards created successfully.")

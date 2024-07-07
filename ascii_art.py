import argparse
from PIL import Image, ImageDraw, ImageFont
from colorama import Fore, Style, Back, init

# Initialize colorama
init(autoreset=True)

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255

def get_pixel_matrix(img, height):
    img.thumbnail((200, height))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]

def get_intensity(p):
    return 0.21*p[0] + 0.72*p[1] + 0.07*p[2]

def convert_to_ascii(pixels_matrix, ascii_chars):
    ascii_matrix = []
    for row in pixels_matrix:
        ascii_row = []
        for p in row:
            intensity = get_intensity(p)
            ascii_char = ascii_chars[int(intensity/MAX_PIXEL_VALUE * (len(ascii_chars) - 1))]
            ascii_row.append((ascii_char, p))
        ascii_matrix.append(ascii_row)
    return ascii_matrix

def get_color_escape_code(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def print_ascii_matrix(ascii_matrix):
    for row in ascii_matrix:
        line = []
        for char, color in row:
            r, g, b = color
            color_code = get_color_escape_code(r, g, b)
            line.append(color_code + char * 2)
        print("".join(line))
    print(Style.RESET_ALL)

def save_ascii_image(ascii_matrix, output_path, font_path=None, font_size=10, bg_color="darkgray"):
    # Calculate image size
    img_width = len(ascii_matrix[0]) * font_size // 2
    img_height = len(ascii_matrix) * font_size

    # Convert bg_color to RGB
    if bg_color == "darkgray":
        bg_color_rgb = (52, 52, 51)  # Dark Gray
    elif bg_color == "black":
        bg_color_rgb = (0, 0, 0)
    else:
        bg_color_rgb = (255, 255, 255)  # Default to white if not specified
    
    # Create a new image with the specified background color
    img = Image.new('RGB', (img_width, img_height), bg_color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Load a font
    font = ImageFont.load_default()
    if font_path:
        font = ImageFont.truetype(font_path, font_size)

    # Draw each character with its corresponding color
    y = 0
    for row in ascii_matrix:
        x = 0
        for char, color in row:
            r, g, b = color
            draw.text((x, y), char, fill=(r, g, b), font=font)
            x += font_size // 2
        y += font_size
    
    img.save(output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate ASCII art from an image file.")
    parser.add_argument("filepath", type=str, help="Path to the image file")
    parser.add_argument("--height", type=int, default=1000, help="Height of the ASCII art (default: 1000)")
    parser.add_argument("--output", type=str, help="Path to save the ASCII art as an image file")
    parser.add_argument("--font", type=str, help="Path to a TTF font file to use")
    parser.add_argument("--fontsize", type=int, default=10, help="Font size for the ASCII art image")
    parser.add_argument("--bgcolor", type=str, default="darkgray", help="Background color for the ASCII art image (default: darkgray)")

    args = parser.parse_args()

    img = Image.open(args.filepath)
    pixels = get_pixel_matrix(img, args.height)

    ascii_matrix = convert_to_ascii(pixels, ASCII_CHARS)
    print_ascii_matrix(ascii_matrix)

    if args.output:
        save_ascii_image(ascii_matrix, args.output, args.font, args.fontsize, args.bgcolor)

if __name__ == "__main__":
    main()

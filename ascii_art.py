from PIL import Image
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

filepath = "./ascii-pineapple.jpg"

img = Image.open(filepath)
pixels = get_pixel_matrix(img, 1000)

ascii_matrix = convert_to_ascii(pixels, ASCII_CHARS)
print_ascii_matrix(ascii_matrix)

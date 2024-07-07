from PIL import Image
ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255
im = Image.open("ascii-pineapple.jpg")
height = 1000
im.thumbnail((height, 200))
pixels = list(im.getdata())
pixel_matrix = [pixels[i:i+im.width] for i in range(0, len(pixels), im.width)]
brightness_matrix = []

for x in range(len(pixel_matrix)):
    brightness_row = []
    for y in range(len(pixel_matrix[x])):
        pixel = pixel_matrix[x][y]
        brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
        brightness_row.append(brightness)
    brightness_matrix.append(brightness_row)
    
def brightness_to_ascii(brightness):
    ascii_index = brightness * (len(ASCII_CHARS) - 1) // MAX_PIXEL_VALUE
    return ASCII_CHARS[ascii_index]

# Convert the brightness matrix to ASCII characters
ascii_matrix = []

for row in brightness_matrix:
    ascii_row = [brightness_to_ascii(brightness) for brightness in row]
    ascii_matrix.append(ascii_row)

# Print the ASCII art
for row in ascii_matrix:
    print("".join(row))
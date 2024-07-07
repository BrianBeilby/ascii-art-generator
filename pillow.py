from PIL import Image
im = Image.open("ascii-pineapple.jpg")
height = 1000
im.thumbnail((height, 200))
pixels = list(im.getdata())
pixel_matrix = [pixels[i:i+im.width] for i in range(0, len(pixels), im.width)]

for x in range(len(pixel_matrix)):
    for y in range(len(pixel_matrix[x])):
        pixel = pixel_matrix[x][y]
        brightness = (pixel[0] + pixel[1] + pixel[2]) / 3
        print(brightness)
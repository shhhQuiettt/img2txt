from PIL import Image, ImageEnhance
from numpy import round
from math import floor

#font Libertum mono

SCALE = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
MAX_RESOLUTION = (300,300)

def px2char(p): #return corresponded char of given pixel

    n = len(SCALE)
    sc = int(round((p/255)*(n-1)))
    return SCALE[sc]

def preproces(img):#prepare image to processing
    (width, height) = img.size

    if width > MAX_RESOLUTION[0]:
        img = img.resize((MAX_RESOLUTION[0], int((MAX_RESOLUTION[0]/width)*height)))
    if height > MAX_RESOLUTION[1]:
        img = img.resize((int((MAX_RESOLUTION[1]/height) * width), MAX_RESOLUTION[1]))

    enhancer = ImageEnhance.Sharpness(img)
    factor = 36
    img =enhancer.enhance(factor)
    img.show()
    img2letters(img, f"./out2.txt")

    return img

def img2letters(img, path):
    width, height = img.size
    px = img.load()
    file = open(path, "w")
    for y in range(height):
        for x in range(width):
            file.write(px2char(px[x, y]))
        file.write("\n")

    file.close()

src = f"./images/image2.jpg"
img = Image.open(src).convert("L") #open in graySCALE
img = preproces(img)
print("Process complete")

img.close()

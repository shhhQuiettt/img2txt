from PIL import Image, ImageEnhance
from numpy import round
import sys
import os

#font Libertum mono

arg = sys.argv


S_PATH = arg[1]
filename, ext = os.path.splitext(S_PATH)

# D_PATH= arg[2]
arg = arg[2:]

print(arg)
SCALE = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """

if "--scale" in arg:
    m_r = arg[arg.index("--scale")+1].split('x')
    for i in range(2):
        if m_r[i] == 'X':
            m_r[i] = None
        else:
            m_r[i] = int(m_r[i])
        MAX_RESOLUTION = tuple(m_r)

else:
    MAX_RESOLUTION = (None,256)

print(MAX_RESOLUTION)
# S_PATH = f"./images/crew.jpg"
# D_PATH = f"./outs/crewtxttxt"

def px2char(p): #return corresponded char of given pixel
    n = len(SCALE)
    sc = int(round((p/255)*(n-1)))
    return SCALE[sc]

def preproces(img):#prepare image to processing
    width , height = img.size
    img = img.resize((int(1.41*width),height))

    width, height = img.size
    if MAX_RESOLUTION[0] != None and width > MAX_RESOLUTION[0]:
        img = img.resize((MAX_RESOLUTION[0], int((MAX_RESOLUTION[0]/width)*height)))

    width, height = img.size
    if MAX_RESOLUTION[1] != None and height > MAX_RESOLUTION[1]:
        img = img.resize((int((MAX_RESOLUTION[1]/height) * width), MAX_RESOLUTION[1]))

    enhancer = ImageEnhance.Sharpness(img)
    factor = 25
    img =enhancer.enhance(factor)
   # img.show()


    return img

def img2letters(img, filename): #create out file with letter instead of pixels
    width, height = img.size

    px = img.load()
    file = open(filename+".txt", "w")
    for y in range(height):
        for x in range(width):
            if (x%2 == 0 and y%2 ==0) or (x%2==1 and y%2 ==1):
              #  last = px2char(px[x, y])
              #  file.write(last)
                file.write(px2char(px[x,y]))
            else:
                file.write(px2char(px[x, y]))

        file.write("\n")
    file.close()

img = Image.open(S_PATH).convert("L") #open in graySCALE
img = preproces(img)    #resizing, sharpness
img2letters(img, filename) #main action

print("Process complete")

img.close()

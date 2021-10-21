from PIL import Image
import time
import os

mypath = os.getcwd() + "\\maze_v2_food.png"
print(mypath)

img = Image.open(mypath)
width, height = img.size
pix = img.load()

positions = []

for x in range(width):
    for y in range(height):
        #print(pix[x, y])
        if pix[x, y][0:3] == (250, 185, 176):
            positions.append([x, y])
print(len(positions))
for x in positions:
    print(str(x) + ",")

#24
#6
#4
#6
#26
#6
#6
#20
#22
#24
#12
#18
#12
#20
#8
#26

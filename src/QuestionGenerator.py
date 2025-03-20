from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import Maths
import math

def question1(): 
    n1 = random.randint(1,6)
    n2 = random.randint(1,6)
    R, a = Maths.Rcos(n1, n2)
    a = f'{R}cos(x + {round(a,3)})'
    pos1 = [104, 6, n1]
    pos2 = [165, 6, n2]
    generate_image('1', 15, pos1, pos2)
    return a

def question2():
    n1 = random.randint(2000, 2020)
    n2 = n1 + random.randint(1, 15)
    n3 = random.randint(30, 99)
    n4 = random.randint(10, (n3 - 5))
    min_n5 = max(n3 - n4 + 1, n4 + 1)
    n5 = random.randint(min_n5, n3 - 1)
    pos1 = [345, 54, n1]
    pos2 = [595, 179, n1]
    pos3 = [178, 345, n2]
    pos4 = [425, 136, n3] 
    pos5 = [464, 136, n4]
    pos6 = [310, 344, n5]
    generate_image('2', 15, pos1, pos2, pos3, pos4, pos5, pos6)
    a = int(n3 - n4)
    result = (math.log((n3 - n5)/n4)/(n2-n1))
    b = round(result, -int(math.floor(math.log10(abs(result)))) + 2)
    return a, b

def generate_image(image, fontsize, *pos):
    img = Image.open(f'Questions/{image}.png')
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', fontsize)
    imgdraw = ImageDraw.Draw(img)
    for i in pos:
        imgdraw.text((i[0], i[1]), str(i[2]), font=imgfont, fill = (0, 0, 0))
    img.show()
    img.save('edited.png')




a, b = question2()
print(a, b)



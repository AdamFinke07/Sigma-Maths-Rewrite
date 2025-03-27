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

def question3(): 
    AB = random.randint(10, 30)
    AC = random.randint(10, 30)
    AD = random.randint(10, 30)
    BE = random.randint(10, 30)
    BG = random.randint(10, 30)
    CE = random.randint(10, 30)
    CF = random.randint(10, 30)
    DF = random.randint(10, 30)
    DI = random.randint(10, 30)
    EF = random.randint(10, 30)
    EG = random.randint(10, 30)
    EH = random.randint(10, 30)
    FH = random.randint(10, 30)
    FI = random.randint(10, 30)
    GJ = random.randint(10, 30)
    HI = random.randint(10, 30)
    HJ = random.randint(10, 30)
    IJ = random.randint(10, 30)
    pos1 = [120, 110, AB] #AB
    pos2 = [135, 162, AC] #AC
    pos3 = [116, 227, AD] #AD
    pos4 = [219, 109, BE] #BE
    pos5 = [298, 58, BG] #BG
    pos6 = [240, 145, CE] #CE
    pos7 = [225, 205, CF] #CF
    pos8 = [229, 237, DF] #DF
    pos9 = [308, 277, DI] #DI
    pos10 = [315, 186, EF] #EF
    pos11 = [385, 110, EG] #EG
    pos12 = [376, 146, EH] #EH
    pos13 = [376, 210, FH] #FH
    pos14 = [377, 237, FI] #FI
    pos15 = [509, 110, GJ] #GJ
    pos16 = [450, 215, HI] #HI
    pos17 = [500, 163, HJ] #HJ
    pos18 = [509, 232, IJ] #IJ
    graph = {
    'A': {'B': AB, 'C': AC, 'D': AD},
    'B': {'A': AB, 'E': BE, 'G': BG},
    'C': {'A': AC, 'E': CE, 'F': CF},
    'D': {'A': AD, 'F': DF, 'I': DI},
    'E': {'B': BE, 'C': CE, 'F': EF, 'G': EG, 'H': EH},
    'F': {'C': CF, 'D': DF, 'E': EF, 'H': FH, 'I': FI},
    'G': {'B': BG, 'E': EG, 'J': GJ},
    'H': {'E': EH, 'F': FH, 'I': HI, 'J': HJ},
    'I': {'D': DI, 'F': FI, 'H': HI, 'J': IJ},
    'J': {'G': GJ, 'H': HJ, 'I': IJ}
    }
    a, b = Maths.dijkstra(graph, 'A', 'J')
    generate_image('3', 15, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10, pos11, pos12, pos13, pos14, pos15, pos16, pos17, pos18)
    return a, b

def generate_image(image, fontsize, *pos):
    img = Image.open(f'Questions/{image}.png')
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', fontsize)
    imgdraw = ImageDraw.Draw(img)
    for i in pos:
        imgdraw.text((i[0], i[1]), str(i[2]), font=imgfont, fill = (0, 0, 0))
    img.show()
    img.save('edited.png')




a, b = question3()
print(a, b)



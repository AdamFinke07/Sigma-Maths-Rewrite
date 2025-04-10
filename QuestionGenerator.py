from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import Maths
import math
import json
import matplotlib.pyplot as plt
import numpy as np

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

def generate_question(question_id):
    # Load and parse questions.json
    with open('Questions/questions.json') as f:
        questions = json.load(f)['questions']
    
    # Find the question data
    for category in questions:
        if question_id in questions[category]:
            question = questions[category][question_id]
            break
    else:
        raise ValueError(f"Question {question_id} not found")

    # Generate random variables
    variables = {}
    for var in question['variables']:
        if var['type'] == 'random':
            variables[var['name']] = random.randint(var['min'], var['max'])
    
    # Calculate answer
    answer_steps = question['answer']
    for step in answer_steps:
        if step['calc'] == 'function':
            # Get function inputs
            inputs = [variables[x] if x in variables else x for x in step['input']]
            
            # Call function
            if step['funcname'].startswith('Maths.'):
                func = getattr(Maths, step['funcname'].split('.')[1])
            else:
                func = globals()[step['funcname']]
            
            # Store outputs
            results = func(*inputs)
            if not isinstance(results, tuple):
                results = (results,)
            for var, result in zip(step['output'], results):
                variables[var] = result
                
        elif step['calc'] == 'answer':
            if step['type'] == 'fstring':
                final_answer = step['output'].format(**variables)

    # Generate image
    img = Image.open(f"Questions/{question['image']}")
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', question['fontsize'])
    imgdraw = ImageDraw.Draw(img)
    
    # Add text to positions
    for pos in question['positions']:
        x, y, var = pos
        value = variables[var]
        imgdraw.text((x, y), str(value), font=imgfont, fill=(0, 0, 0))
    
    img.show()
    img.save('edited.png')
    
    return final_answer

def generate_quadratic_graph():
    # Generate random coefficients (all integers)
    a = random.randint(1, 5)  # Ensure a is positive
    b = random.randint(-10, 10)
    c = random.randint(0, 20)  # Start with positive c
    
    # Create x values for the full curve
    x_full = np.linspace(-10, 10, 400)
    y_full = a * x_full**2 + b * x_full + c
    
    # Check if the minimum value is below 0
    min_y = min(y_full)
    if min_y < 0:
        # Shift the function up by the absolute value of the minimum, rounded up to nearest integer
        shift = math.ceil(abs(min_y))
        c += shift
        y_full = a * x_full**2 + b * x_full + c
    
    # Create x values for the shaded region
    x_shade = np.linspace(0, 2, 100)
    y_shade = a * x_shade**2 + b * x_shade + c
    
    # Create the plot
    plt.figure(figsize=(8, 6))
    
    # Plot the full curve
    plt.plot(x_full, y_full, 'b-', linewidth=2)
    
    # Fill the area under the curve between x=0 and x=2
    plt.fill_between(x_shade, y_shade, 0, 
                    color='blue', alpha=0.3)
    
    # Add grid and axes
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=1)
    
    # Add vertical lines at integration limits that stop at the curve
    y_at_0 = a * 0**2 + b * 0 + c
    y_at_2 = a * 2**2 + b * 2 + c
    
    plt.plot([0, 0], [0, y_at_0], 'g--', linewidth=2)
    plt.plot([2, 2], [0, y_at_2], 'g--', linewidth=2)
    
    # Set axis limits and ticks
    plt.xlim(-10, 10)
    plt.xticks(range(-10, 11, 2))
    
    y_max = math.ceil(max(y_full))
    plt.ylim(0, y_max)
    
    # Calculate step size to show at most 10 numbers
    step = max(1, math.ceil(y_max / 10))
    plt.yticks(range(0, y_max + 1, step))
    
    # Remove all labels and titles except integration limits
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('')
    plt.ylabel('')
    plt.title('')
    
    # Add labels for integration limits
    plt.text(0, -0.5, '0', ha='center', va='top')
    plt.text(2, -0.5, '2', ha='center', va='top')
    
    # Save the plot
    plt.savefig('graph.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return a, b, c, Maths.integrate([a, b, c], 0, 2)
  
a, b, c, integral = generate_quadratic_graph()
print(a, b, c, integral)


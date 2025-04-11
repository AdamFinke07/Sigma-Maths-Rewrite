from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import Maths
import math
import json
import matplotlib.pyplot as plt
import numpy as np
import sigfig as sf
import builtins



def generate_image(image, fontsize, *pos):
    img = Image.open(f'{image}.png')
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', fontsize)
    imgdraw = ImageDraw.Draw(img)
    for i in pos:
        imgdraw.text((i[0], i[1]), str(i[2]), font=imgfont, fill = (0, 0, 0))
    img.show()
    img.save('edited.png')

def generate_question(question_id):
    # Load and parse questions.json
    with open('Questions.json') as f:
        questions = json.load(f)['questions']
    
    # Find the question data
    if question_id in questions:
        question = questions[question_id]
    else:
        raise ValueError(f"Question {question_id} not found")

    # Generate random variables
    variables = {}
    for var in question['variables']:
        if var['type'] == 'random':
            # Handle expressions in min/max
            min_val = var['min']
            max_val = var['max']
            
            # If min/max is a string expression, evaluate it
            if isinstance(min_val, str):
                # Replace √ with math.sqrt
                min_val = min_val.replace('√', 'math.sqrt')
                min_val = eval(min_val, {'math': math, **variables})
            if isinstance(max_val, str):
                # Replace √ with math.sqrt
                max_val = max_val.replace('√', 'math.sqrt')
                max_val = eval(max_val, {'math': math, **variables})
            
            # Generate random value between min and max
            if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
                if isinstance(min_val, int) and isinstance(max_val, int):
                    variables[var['name']] = random.randint(min_val, max_val)
                else:
                    variables[var['name']] = random.uniform(min_val, max_val)
            else:
                raise ValueError(f"Invalid min/max values for variable {var['name']}")
                
        elif var['type'] == 'randomaddition':
            # Add a random number between 1 and 15 to n1
            variables[var['name']] = variables['n1'] + random.randint(1, 15)
        elif var['type'] == 'graph':
            # Use the graph directly from the variables section
            graph = var['graph']
            # Replace the edge names with their actual values
            for node in graph:
                for neighbor in graph[node]:
                    edge_name = graph[node][neighbor]
                    if edge_name in variables:
                        graph[node][neighbor] = variables[edge_name]
            variables[var['name']] = graph

    # Calculate answer
    answer_steps = question['answer']
    final_answer = None
    
    for step in answer_steps:
        if step['calc'] == 'function':
            # Get function inputs
            inputs = []
            for x in step['input']:
                if x in variables:
                    inputs.append(variables[x])
                elif isinstance(x, str):
                    # Remove quotes if present
                    if x.startswith("'") and x.endswith("'"):
                        x = x[1:-1]
                    # If it's an expression, evaluate it with math module available
                    if any(c in x for c in ['+', '-', '*', '/']):
                        inputs.append(eval(x, {'math': math, **variables}))
                    else:
                        inputs.append(x)
                else:
                    inputs.append(x)
            
            # Get the function
            try:
                if step['funcname'].startswith('Maths.'):
                    func = getattr(Maths, step['funcname'].split('.')[1])
                elif step['funcname'].startswith('math.'):
                    func = getattr(math, step['funcname'].split('.')[1])
                elif step['funcname'].startswith('sf.'):
                    func = getattr(sf, step['funcname'].split('.')[1])
                elif step['funcname'] in globals():
                    func = globals()[step['funcname']]
                elif hasattr(builtins, step['funcname']):
                    func = getattr(builtins, step['funcname'])
                else:
                    raise ValueError(f"Function {step['funcname']} not found")
            except Exception as e:
                raise ValueError(f"Error getting function {step['funcname']}: {str(e)}")
            
            # Call the function
            try:
                results = func(*inputs)
                if not isinstance(results, tuple):
                    results = (results,)
                for var, result in zip(step['output'], results):
                    variables[var] = result
            except Exception as e:
                raise ValueError(f"Error calling function {step['funcname']}: {str(e)}")
                
        elif step['calc'] == 'answer':
            if step['type'] == 'fstring':
                # For Rcos answers, extract the numeric values
                if 'R' in variables and 'a' in variables:
                    final_answer = f"{variables['R']} {round(variables['a'], 3)}"
                else:
                    final_answer = step['output'].format(**variables)
            elif step['type'] == 'tuple':
                final_answer = tuple(str(variables[var]) for var in step['output'])
            elif step['type'] == 'multiple':
                # Handle multiple answers for answerbox questions
                final_answer = {}
                for box in question['answerbox']:
                    label = box['label']
                    answer_var = box['answer']
                    value = variables[answer_var]
                    if isinstance(value, float):
                        final_answer[label] = f"{value:.3f}"
                    else:
                        final_answer[label] = str(value)

    # Generate image
    try:
        img = Image.open(f'Questions/{question["image"]}')
    except FileNotFoundError:
        # If image not found in Questions folder, try root directory
        img = Image.open(question['image'])
        
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', question['fontsize'])
    imgdraw = ImageDraw.Draw(img)
    
    # Add text to positions
    for pos in question['positions']:
        x, y, var = pos
        value = variables[var]
        # Format the value appropriately for display
        if isinstance(value, float):
            # For floats, round to 3 decimal places
            display_value = f"{value:.3f}"
        else:
            display_value = str(value)
        imgdraw.text((x, y), display_value, font=imgfont, fill=(0, 0, 0))
    
    # Save the image but don't show it
    img.save('edited.png')
    
    if final_answer is None:
        raise ValueError("No answer was generated for the question")
    
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


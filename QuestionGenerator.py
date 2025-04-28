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
import io
from enum import Enum
from typing import Any, Union, List

# Global buffer for the graph
graph_buffer = None
# Global buffer for the edited image
edited_image_buffer = None

class VariableType(Enum):
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    LIST = "list"
    GRAPH = "graph"

class Variable:
    def __init__(self, name: str, value: Any, var_type: VariableType):
        self.name = name
        self.value = value
        self.type = var_type

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Variable({self.name}, {self.value}, {self.type})"

    @property
    def is_list(self) -> bool:
        return self.type == VariableType.LIST

    @property
    def is_graph(self) -> bool:
        return self.type == VariableType.GRAPH

    @property
    def is_numeric(self) -> bool:
        return self.type in (VariableType.INTEGER, VariableType.FLOAT)

def question4():
    a = random.randint(-10, -1)
    b = random.randint(10, 20)
    c = random.randint(10, 20)
    d,p,q = Maths.complete_square(a,b,c)
    roots = Maths.roots([a, b, c])
    answer1a = d
    answer1b = p
    answer1c = q
    answer2 = f'({p}, {-q})'
    answer3 = (p * -q) - Maths.integrate([a, b, c], 0, p)
    print(answer1a, answer1b, answer1c, answer2, answer3)
    plot([a, b, c], [q], x_range=((roots[0] - 1), (roots[len(roots)-1] + 1)), y_range=(-3, (q + 5)), shaded_region=[[[int(a), b, c], [q]], 'green', ('x', 0, -p)])
    generate_image(4, 15, (169, 297, 425, 325), (376, 49, f'{a}x² + {b}x + {c}'))
    
def plot(*coefficients, x_range=(-10, 10), y_range=None, points=1000, shaded_region=None):
    """
    Plot one or more polynomial functions given their coefficients.
    
    Args:
        *coefficients: One or more lists of polynomial coefficients [a_n, a_{n-1}, ..., a_1, a_0]
            for polynomial a_n*x^n + a_{n-1}*x^{n-1} + ... + a_1*x + a_0
        x_range (tuple): Tuple of (min_x, max_x) for the x-axis range
        y_range (tuple): Tuple of (min_y, max_y) for the y-axis range. If None, it will be auto-scaled
        points (int): Number of points to plot
        shaded_region (list): List defining a shaded region in format [boundaries, color, cutoff]
            - boundaries: List of two coefficient lists [coeff1, coeff2]
            - color: Optional color for the shading (defaults to semi-transparent blue)
            - cutoff: Optional tuple of (axis, min_value, max_value) to limit the shaded region, 
                     e.g. ('x', 0, 5) for x between 0 and 5
    """
    global graph_buffer
    
    # Convert x_range to floats
    x_range = (float(x_range[0]), float(x_range[1]))
    x = np.linspace(x_range[0], x_range[1], points)
    
    plt.figure()
    colors = ['b', 'r', 'g', 'm', 'c', 'y']  # Different colors for different functions
    
    # Plot x-axis (y=0) and y-axis (x=0)
    plt.axhline(y=0, color='black', linewidth=1)  # x-axis
    plt.axvline(x=0, color='black', linewidth=1)  # y-axis
    
    # Plot the functions
    for i, coeff in enumerate(coefficients):
        # Convert coefficients to floats
        coeff = [float(c) for c in coeff]
        y = np.polyval(coeff, x)
        color = colors[i % len(colors)]  # Cycle through colors if there are more functions than colors
        plt.plot(x, y, color=color, label=f'Function {i+1}')
    
    # Add shaded region if specified
    if shaded_region:
        boundaries, *rest = shaded_region
        color = rest[0] if rest else 'blue'
        cutoff = rest[1] if len(rest) > 1 else None
        alpha = 0.3  # Default transparency
        
        coeff1, coeff2 = boundaries
        # Convert coefficients to floats
        coeff1 = [float(c) for c in coeff1]
        coeff2 = [float(c) for c in coeff2]
        y1 = np.polyval(coeff1, x)
        y2 = np.polyval(coeff2, x)
        
        if cutoff:
            axis, min_val, max_val = cutoff
            if axis == 'x':
                # Ensure values are floats
                min_val = float(min_val)
                max_val = float(max_val)
                mask = (x >= min_val) & (x <= max_val)
                plt.fill_between(x[mask], y1[mask], y2[mask], color=color, alpha=alpha)
            elif axis == 'y':
                min_val = float(min_val)
                max_val = float(max_val)
                mask = (y1 >= min_val) & (y2 >= min_val) & (y1 <= max_val) & (y2 <= max_val)
                plt.fill_between(x[mask], y1[mask], y2[mask], color=color, alpha=alpha)
        else:
            plt.fill_between(x, y1, y2, color=color, alpha=alpha)
    
    if y_range is not None:
        y_range = (float(y_range[0]), float(y_range[1]))
        plt.ylim(y_range)
    
    plt.grid(False)
    
    # Save the plot to the global buffer
    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    graph_buffer.seek(0)

def generate_image(question, variables):
    """Generate and save the question image."""
    global edited_image_buffer
    
    try:
        img = Image.open(f'Questions/{question["image"]}')
    except FileNotFoundError:
        img = Image.open(question['image'])
        
    imgfont = ImageFont.truetype('Fonts/OpenSans-Medium.ttf', question['fontsize'])
    imgdraw = ImageDraw.Draw(img)
    
    # Add text to positions
    for pos in question['positions']:
        x, y, var = pos
        value = variables[var].value
        if isinstance(value, float):
            display_value = f"{value:.3f}"
        else:
            display_value = str(value)
        imgdraw.text((x, y), display_value, font=imgfont, fill=(0, 0, 0))
    
    # Add graph if we have one in the buffer
    if graph_buffer is not None and 'graph' in question:
        # Get graph position from graph section
        x, y, width, height = question['graph']['position']
        
        # Get the graph from the buffer
        graph = Image.open(graph_buffer)
        # Resize graph to fit specified dimensions
        graph = graph.resize((width, height))
        # Paste graph onto main image
        img.paste(graph, (x, y))
    
    # Save the image to buffer
    edited_image_buffer = io.BytesIO()
    img.save(edited_image_buffer, format='PNG')
    edited_image_buffer.seek(0)
    
    return edited_image_buffer

def generate_question(question_id):
    """
    Generates a question based on the given question ID from Questions.json.
    
    Args:
        question_id (str): The ID of the question to generate
        
    Returns:
        tuple: (dict, BytesIO) The answer(s) to the generated question and the image buffer
                      
    Raises:
        ValueError: If the question ID is not found or if no answer is generated
        FileNotFoundError: If the question image file is not found
    """
    # Load and parse questions.json
    with open('Questions.json') as f:
        questions = json.load(f)['questions']
    
    # Find the question data
    if question_id not in questions:
        raise ValueError(f"Question {question_id} not found")
    question = questions[question_id]

    # Generate variables
    variables = generate_variables(question['variables'])
    
    # Calculate answer
    final_answer = calculate_answer(question['answer'], variables, question['answerbox'])
    
    # Generate graph if specified
    if 'graph' in question:
        generate_graph_plot(question['graph'], variables)
    
    # Generate image
    image_buffer = generate_image(question, variables)
    
    return final_answer, image_buffer

def generate_variables(variables_spec):
    """Generate variables based on their specifications."""
    variables = {}
    for var in variables_spec:
        if var['type'] == 'random':
            value = generate_random(var['min'], var['max'], variables)
            var_type = VariableType.INTEGER if isinstance(value, int) else VariableType.FLOAT
            variables[var['name']] = Variable(var['name'], value, var_type)
        elif var['type'] == 'randomaddition':
            value = variables['n1'].value + random.randint(1, 15)
            variables[var['name']] = Variable(var['name'], value, VariableType.INTEGER)
        elif var['type'] == 'graph':
            value = generate_graph(var['graph'], variables)
            variables[var['name']] = Variable(var['name'], value, VariableType.GRAPH)
        elif var['type'] == 'fstring':
            value = generate_fstring(var['input'], variables)
            variables[var['name']] = Variable(var['name'], value, VariableType.STRING)
        elif var['type'] == 'list':
            value = [variables[v].value for v in var['variables']]
            variables[var['name']] = Variable(var['name'], value, VariableType.LIST)
    return variables

def generate_random(min_val, max_val, variables):
    """Generate a random value between min and max."""
    if isinstance(min_val, str):
        min_val = eval(min_val, {'math': math, **{k: v.value for k, v in variables.items()}})
    if isinstance(max_val, str):
        max_val = eval(max_val, {'math': math, **{k: v.value for k, v in variables.items()}})
    
    if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
        if isinstance(min_val, int) and isinstance(max_val, int):
            return random.randint(min_val, max_val)
        return random.uniform(min_val, max_val)
    raise ValueError(f"Invalid min/max values: {min_val}, {max_val}")

def generate_graph(graph_spec, variables):
    """Generate a graph with edge weights from variables."""
    graph = graph_spec.copy()
    for node in graph:
        for neighbor in graph[node]:
            edge_name = graph[node][neighbor]
            if edge_name in variables:
                graph[node][neighbor] = variables[edge_name].value
    return graph

def generate_fstring(components, variables):
    """Generate a formatted string from components."""
    result = ""
    for component in components:
        if component[0] == 'variable':
            result += str(variables[component[1]].value)
        elif component[0] == 'string':
            result += component[1]
    return result

def calculate_answer(answer_steps, variables, answerbox):
    """Calculate the answer based on the answer steps."""
    for step in answer_steps:
        if step['calc'] == 'function':
            inputs = process_function_inputs(step['input'], variables)
            func = get_function(step['funcname'])
            results = call_function(func, inputs, step['output'], variables)
        elif step['calc'] == 'answer':
            if step['type'] == 'multiple':
                return generate_multiple_answer(answerbox, variables)
            elif step['type'] == 'fstring':
                value = generate_fstring(step['input'], variables)
                variables[step['output'][0]] = Variable(step['output'][0], value, VariableType.STRING)
            elif step['type'].startswith('f'):
                format_str = step['type'][1:]
                value = eval(format_str, {'math': math, **{k: v.value for k, v in variables.items()}})
                variables[step['output'][0]] = Variable(step['output'][0], value, VariableType.STRING)
    
    raise ValueError("No answer was generated for the question")

def process_function_inputs(inputs, variables):
    """Process function inputs into their final form."""
    processed_inputs = []
    # If inputs is a string, treat it as a single variable reference
    if isinstance(inputs, str):
        if inputs in variables:
            return [variables[inputs].value]
        else:
            raise ValueError(f"Variable {inputs} not found")
    
    # Otherwise process as a list of inputs
    for x in inputs:
        if isinstance(x, str):
            if x in variables:
                processed_inputs.append(variables[x].value)
            elif x.startswith("'") and x.endswith("'"):
                processed_inputs.append(x[1:-1])
            elif x.startswith('[') and x.endswith(']'):
                list_content = x[1:-1]
                list_vars = [var.strip() for var in list_content.split(',') if var.strip()]
                processed_inputs.append([variables[var].value for var in list_vars])
            elif any(c in x for c in ['+', '-', '*', '/']):
                processed_inputs.append(eval(x, {'math': math, **{k: v.value for k, v in variables.items()}}))
            else:
                # Try to convert to float/int if it's a numeric string
                try:
                    if '.' in x:
                        processed_inputs.append(float(x))
                    else:
                        processed_inputs.append(int(x))
                except ValueError:
                    processed_inputs.append(x)
        else:
            processed_inputs.append(x)
    return processed_inputs

def process_list_literal(list_str, variables):
    """Process a list literal string into a list of values."""
    list_content = list_str[1:-1]
    list_vars = [var.strip() for var in list_content.split(',') if var.strip()]
    return [variables[var].value for var in list_vars]

def get_function(funcname):
    """Get a function by its name."""
    try:
        match funcname.split('.'):
            case ['Maths', func_name]:
                return getattr(Maths, func_name)
            case ['math', func_name]:
                return getattr(math, func_name)
            case ['sf', func_name]:
                return getattr(sf, func_name)
            case [func_name]:
                if func_name in globals():
                    return globals()[func_name]
                elif hasattr(builtins, func_name):
                    return getattr(builtins, func_name)
                raise ValueError(f"Function {func_name} not found")
            case _:
                raise ValueError(f"Invalid function name format: {funcname}")
    except Exception as e:
        raise ValueError(f"Error getting function {funcname}: {str(e)}")

def call_function(func, inputs, output_vars, variables):
    """Call a function and store its results."""
    try:
        # Special handling for Maths.roots
        if func.__name__ == 'roots':
            if len(inputs) != 1:
                raise ValueError(f"Maths.roots expects exactly one list argument, got {len(inputs)}")
            if not isinstance(inputs[0], list):
                raise ValueError(f"Maths.roots expects a list argument, got {type(inputs[0])}")
            results = func(inputs[0])
        else:
            results = func(*inputs)
            
        if not isinstance(results, tuple):
            results = (results,)
            
        # Store results in variables
        for var, result in zip(output_vars, results):
            if isinstance(result, list):
                var_type = VariableType.LIST
            elif isinstance(result, (int, float)):
                var_type = VariableType.FLOAT if isinstance(result, float) else VariableType.INTEGER
            elif isinstance(result, str):
                var_type = VariableType.STRING
            elif isinstance(result, dict):
                var_type = VariableType.GRAPH
            else:
                var_type = VariableType.STRING
                
            variables[var] = Variable(var, result, var_type)
            
        return results
    except Exception as e:
        raise ValueError(f"Error calling function {func.__name__}: {str(e)}")

def generate_multiple_answer(answerbox, variables):
    """Generate the final answer for multiple answer boxes."""
    final_answer = {}
    for box in answerbox:
        label = box['label']
        answer_var = box['answer']
        value = variables[answer_var].value
        if isinstance(value, float):
            final_answer[label] = f"{value:.3f}"
        else:
            final_answer[label] = str(value)
    return final_answer

def generate_graph_plot(graph_spec, variables):
    """Generate a graph plot based on the graph specification."""
    # Extract coefficients for each function
    coefficients = []
    for coeff_group in graph_spec['coefficients']:
        coeff_values = []
        for var in coeff_group:
            if var in variables:
                coeff_values.append(variables[var].value)
            else:
                coeff_values.append(float(var))
        coefficients.append(coeff_values)
    
    # Calculate dynamic ranges if needed
    x_range = graph_spec['x_range']
    y_range = graph_spec['y_range']
    
    # If x_range is a string expression, evaluate it
    if isinstance(x_range, str):
        x_range = eval(x_range, {'math': math, **{k: v.value for k, v in variables.items()}})
    # If x_range is a list with expressions, evaluate them
    elif isinstance(x_range, list) and len(x_range) == 2:
        min_x, max_x = x_range
        if isinstance(min_x, str):
            min_x = eval(min_x, {'math': math, **{k: v.value for k, v in variables.items()}})
        if isinstance(max_x, str):
            max_x = eval(max_x, {'math': math, **{k: v.value for k, v in variables.items()}})
        x_range = (min_x, max_x)
    
    # If y_range is a string expression, evaluate it
    if isinstance(y_range, str):
        y_range = eval(y_range, {'math': math, **{k: v.value for k, v in variables.items()}})
    # If y_range is a list with expressions, evaluate them
    elif isinstance(y_range, list) and len(y_range) == 2:
        min_y, max_y = y_range
        if isinstance(min_y, str):
            min_y = eval(min_y, {'math': math, **{k: v.value for k, v in variables.items()}})
        if isinstance(max_y, str):
            max_y = eval(max_y, {'math': math, **{k: v.value for k, v in variables.items()}})
        y_range = (min_y, max_y)
    
    # Process shaded region if specified
    shaded_region = None
    if 'shaded_region' in graph_spec:
        region_spec = graph_spec['shaded_region']
        # Get the boundary functions
        boundary1 = [variables[var].value for var in region_spec[0]]
        boundary2 = [variables[var].value for var in region_spec[1]]
        color = region_spec[2]
        cutoff = region_spec[3]
        
        # Process cutoff values
        axis, min_val, max_val = cutoff
        if isinstance(min_val, str):
            min_val = eval(min_val, {'math': math, **{k: v.value for k, v in variables.items()}})
        if isinstance(max_val, str):
            max_val = eval(max_val, {'math': math, **{k: v.value for k, v in variables.items()}})
        
        shaded_region = [[boundary1, boundary2], color, [axis, float(min_val), float(max_val)]]
    
    # Generate the plot
    plot(*coefficients, 
         x_range=x_range, 
         y_range=y_range, 
         shaded_region=shaded_region)

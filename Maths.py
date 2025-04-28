import math
from fractions import Fraction
import numpy as np

sqrtsymbol = '√'

def Rcos(a, b):
    """
    Converts a linear combination of cosine and sine into Rcos(x + α) form.
    
    Args:
        a (float): Coefficient of cos(x)
        b (float): Coefficient of sin(x)
        
    Returns:
        tuple: (R, α) where:
            R is the amplitude (√(a² + b²))
            α is the phase shift (arctan(b/a))
    """
    R = surd(a**2 + b**2)
    a = math.atan(b/a)
    return R, a

def surd(a):
    """
    Simplifies a square root expression to its simplest form.
    
    Args:
        a (float): The number to simplify
        
    Returns:
        float or str: If the square root is a perfect square, returns the integer value.
                     Otherwise returns a string in the form 'ksqrt(n)' where k is the
                     integer part and n is the remaining square root.
    """
    exact = math.sqrt(a)
    integer = 1
    root = 1
    if exact % 1 == 0:
        return exact
    else:
        factors = primefactors(a)
        for i in factors:
            count = factors.count(i)
            if count > 0 and count % 2 == 0:
                for j in range(0, count):
                    factors.remove(i)
                integer = integer * i ** (count / 2)
            elif count > 2:
                for j in range (0, (count - 1)):
                    factors.remove(i)
                integer = integer * i ** ((count - 1) / 2)
        for i in factors:
            root = root * i
        if integer == 1:
            return f'sqrt({root})'
        else:
            return f'{int(integer)}sqrt({root})'

def primefactors(n, divisor=2):
    """
    Recursively finds all prime factors of a number.
    
    Args:
        n (int): The number to factorize
        divisor (int): Current divisor to check (starts at 2)
        
    Returns:
        list: List of prime factors, including duplicates
    """
    if n <= 1:
        return []
        
    if n % divisor == 0:
        return [divisor] + primefactors(n // divisor, divisor)
    else:
        return primefactors(n, divisor + 1)

def complete_square(a, b, c):
    """
    Completes the square for a quadratic expression ax^2 + bx + c.
    Returns the expression in the form a(x + p)^2 + q, with simplified fractions.
    
    Args:
        a (float): Coefficient of x^2
        b (float): Coefficient of x
        c (float): Constant term
        
    Returns:
        tuple: (a, p, q) where the completed square form is a(x + p)^2 + q
        p and q are returned as simplified fractions when possible
        
    Raises:
        ValueError: If coefficient 'a' is zero
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero")
    
    # Convert inputs to fractions for exact arithmetic
    a_frac = Fraction(a).limit_denominator()
    b_frac = Fraction(b).limit_denominator()
    c_frac = Fraction(c).limit_denominator()
    
    # Calculate p and q as fractions
    p = b_frac / (2 * a_frac)
    q = c_frac - (b_frac**2) / (4 * a_frac)
    
    # Return a as float, p and q as simplified fractions
    return float(a), p, q

def dijkstra(graph, start, end):
    """
    Finds the shortest path between two nodes in a weighted graph using Dijkstra's algorithm.
    
    Args:
        graph (dict): The graph represented as a dictionary where keys are nodes and
                     values are dictionaries of neighboring nodes and their edge weights
        start (str): The starting node
        end (str): The destination node
        
    Returns:
        tuple: (path_string, distance) where:
            path_string: String representation of the path (e.g., 'ABCEJ')
            distance: Total distance of the shortest path
            
    Note:
        The graph should be a dictionary where each node maps to a dictionary of
        its neighbors and their edge weights. For example:
        {
            'A': {'B': 10, 'C': 15},
            'B': {'A': 10, 'D': 5},
            ...
        }
    """
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    paths = {node: [] for node in graph}
    paths[start] = [start]
    unvisited = set(graph.keys())
    
    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        
        if distances[current] == float('infinity'):
            break
            
        unvisited.remove(current)
        
        for neighbor, weight in graph[current].items():
            if neighbor in unvisited:
                new_distance = distances[current] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    paths[neighbor] = paths[current] + [neighbor]
    
    path_string = ''.join(paths[end])
    distance = int(distances[end])
    
    return path_string, distance

def integrate(coefficients, lower_limit, upper_limit):
    """
    Calculates the definite integral of a polynomial function.
    
    Args:
        coefficients (list): List of coefficients in descending order of power
            e.g., [a, b, c] for ax^2 + bx + c
        lower_limit (float): Lower limit of integration
        upper_limit (float): Upper limit of integration
        
    Returns:
        float: The value of the definite integral
        
    Note:
        The integral is calculated using the power rule:
        ∫x^n dx = (x^(n+1))/(n+1)
    """
    coeffs = coefficients[::-1]
    
    # Calculate the integral at upper limit
    upper_result = 0
    for i, coeff in enumerate(coeffs):
        power = i + 1
        upper_result += coeff * (upper_limit ** power) / power
    
    # Calculate the integral at lower limit
    lower_result = 0
    for i, coeff in enumerate(coeffs):
        power = i + 1
        lower_result += coeff * (lower_limit ** power) / power
    
    # Return the definite integral
    return upper_result - lower_result

def merge_sort(arr):
    """
    Sorts a list using merge sort algorithm.
    
    Args:
        arr (list): List to be sorted
        
    Returns:
        list: Sorted list in ascending order
    """
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """
    Merges two sorted lists into one sorted list.
    
    Args:
        left (list): First sorted list
        right (list): Second sorted list
        
    Returns:
        list: Merged sorted list
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def roots(coefficients):
    """
    Finds the roots of a polynomial equation and returns them in ascending order.
    
    Args:
        coefficients (list): List of coefficients in descending order of power
            e.g., [a, b, c] for ax^2 + bx + c
            
    Returns:
        list: Roots of the polynomial in ascending order
        
    Note:
        Uses numpy's roots function to find the roots and custom merge sort to sort them.
        Complex roots are converted to real numbers if their imaginary part is negligible.
    """
    # Find roots using numpy
    roots_list = np.roots(coefficients)
    
    # Convert complex roots to real if imaginary part is negligible
    real_roots = []
    for root in roots_list:
        if abs(root.imag) < 1e-10:
            real_roots.append(root.real)
    
    # Sort roots using merge sort
    return merge_sort(real_roots)





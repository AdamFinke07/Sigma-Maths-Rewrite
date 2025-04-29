import math
from fractions import Fraction
import numpy as np

sqrtsymbol = '√'

def Rcos(a, b):
    R = surd(a**2 + b**2)
    a = math.atan(b/a)
    return R, a

def surd(a):
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
    if n <= 1:
        return []
        
    if n % divisor == 0:
        return [divisor] + primefactors(n // divisor, divisor)
    else:
        return primefactors(n, divisor + 1)

def complete_square(a, b, c):
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero")
    
    a_frac = Fraction(a).limit_denominator()
    b_frac = Fraction(b).limit_denominator()
    c_frac = Fraction(c).limit_denominator()
    
    p = b_frac / (2 * a_frac)
    q = c_frac - (b_frac**2) / (4 * a_frac)
    
    return float(a), p, q

def dijkstra(graph, start, end):
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
    coeffs = coefficients[::-1]
    
    upper_result = 0
    for i, coeff in enumerate(coeffs):
        power = i + 1
        upper_result += coeff * (upper_limit ** power) / power
    
    lower_result = 0
    for i, coeff in enumerate(coeffs):
        power = i + 1
        lower_result += coeff * (lower_limit ** power) / power
    
    return upper_result - lower_result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
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
    roots_list = np.roots(coefficients)
    
    real_roots = []
    for root in roots_list:
        if abs(root.imag) < 1e-10:
            real_roots.append(root.real)
    
    return merge_sort(real_roots)





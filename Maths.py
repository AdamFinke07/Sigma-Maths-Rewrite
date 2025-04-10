import math

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

        

def primefactors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

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




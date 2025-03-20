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
            return f'{sqrtsymbol}({root})'
        else:
            return f'{int(integer)}{sqrtsymbol}({root})'

        

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

                



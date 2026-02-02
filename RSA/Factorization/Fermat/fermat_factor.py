import math

def fermat_factor(n, max_iter=1000000):
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for i in range(max_iter):
        b2 = a*a - n
        b = math.isqrt(b2)
        if b*b == b2:
            return a - b, a + b
        a += 1
    return None

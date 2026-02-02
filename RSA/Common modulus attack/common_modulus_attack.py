from Crypto.Util.number import inverse, long_to_bytes

def common_modulus_attack(n,e1,c1,e2,c2):
    
    def extended_gcd(a, b):
        if b == 0:
            return (1, 0)
        else:
            x1, y1 = extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return (x, y)

    x, y = extended_gcd(e1, e2)
    if x < 0:
        c1 = inverse(c1, n)
        x = -x
    if y < 0:
        c2 = inverse(c2, n)
        y = -y

    m = (pow(c1, x, n) * pow(c2, y, n)) % n
    print(long_to_bytes(m))
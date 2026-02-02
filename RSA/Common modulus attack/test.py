from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd
from common_modulus_attack import common_modulus_attack

# gen
flag = "flag{mod_n_math_leaks_secrets_watch_the_remainder}"
m = bytes_to_long(flag.encode())
e1, e2 = 65537, 17
assert gcd(e1, e2) == 1
while True:
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e1, phi) != 1 or gcd(e2, phi) != 1:
        continue
    if m >= n:
        continue
    if gcd(m, n) != 1:
        continue
    break

c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

# solve

common_modulus_attack(n,e1,c1,e2,c2)
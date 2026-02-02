from Crypto.Util.number import inverse, getPrime, bytes_to_long, long_to_bytes
from sympy import nextprime
import os
from fermat_factor import fermat_factor

# gen
flag = "h4tum{fermat_f4ctor_close_pr1mes_break_rsa}"
m = bytes_to_long(flag.encode())

p = getPrime(512)
diff = (2**135)*int.from_bytes(os.urandom(16), 'big')
q = nextprime(p - diff)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = inverse(e, phi)
ciphertext = pow(m, e, n)

# solve
p, q = fermat_factor(n)
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(ciphertext, d, n)
print(long_to_bytes(m))
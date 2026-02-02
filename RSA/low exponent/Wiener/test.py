from Crypto.Util.number import inverse, getPrime, bytes_to_long, long_to_bytes
from wiener_attack import wiener_attack

# gen
flag = "flag{continued_fracts_snitch_on_small_d}"
m = bytes_to_long(flag.encode())
p = getPrime(512)
q = getPrime(512)
n = p * q
phi = (p - 1) * (q - 1)
d = getPrime(30)
e = inverse(d, phi)
ciphertext = pow(m, e, n)

# solve
d = wiener_attack(e,n)
m = pow(ciphertext, d, n)
print(long_to_bytes(m))

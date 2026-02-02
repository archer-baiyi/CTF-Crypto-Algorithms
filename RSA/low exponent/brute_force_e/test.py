from Crypto.Util.number import inverse, getPrime, bytes_to_long
from bf_e import bf_e

flag = "flag{small_e3_cub3rt_attack_needs_p4dding}"
m = bytes_to_long(flag.encode())

p = getPrime(512)
q = getPrime(512)
n = p * q
phi = (p - 1) * (q - 1)
e = 3
d = inverse(e, phi)

assert pow(m,e) >= n
ciphertext = pow(m, e, n)

bf_e(n,e,ciphertext)
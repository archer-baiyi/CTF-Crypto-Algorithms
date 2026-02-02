from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes

def bf_e(n, e, ciphertext,max = 100000):
    for i in range(0, max):
        modified_c = ciphertext + i * n
        m_root, exact = iroot(modified_c, e)
        if exact:
            print(f"found: i = {i}")
            print("message:", long_to_bytes(m_root))
            break
    else:
        print("not found")
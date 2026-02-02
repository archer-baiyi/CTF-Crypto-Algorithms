import math

def continued_fraction(numerator, denominator):
    """Generate the continued fraction expansion of numerator/denominator."""
    cf = []
    while denominator:
        a = numerator // denominator
        cf.append(a)
        numerator, denominator = denominator, numerator - a * denominator
    return cf


def convergents_from_cf(cf):
    """Generate convergents (k, d) from a continued fraction sequence cf."""
    n0, d0 = cf[0], 1
    yield (n0, 1)
    if len(cf) == 1:
        return
    n1 = cf[1] * cf[0] + 1
    d1 = cf[1]
    yield (n1, d1)
    for i in range(2, len(cf)):
        ni = cf[i] * n1 + n0
        di = cf[i] * d1 + d0
        yield (ni, di)
        n0, d0, n1, d1 = n1, d1, ni, di


def is_perfect_square(x):
    """Check whether x is a perfect square."""
    if x < 0:
        return False
    s = math.isqrt(x)
    return s * s == x


def wiener_attack(e, n):
    """
    Attempt to recover the RSA private exponent d using Wiener's attack.

    Args:
        e: Public exponent
        n: Modulus

    Returns:
        If successful, returns the private exponent d; otherwise returns None.
    """
    cf = continued_fraction(e, n)
    for k, d in convergents_from_cf(cf):
        if k == 0:
            continue

        # Check whether (e*d - 1) is divisible by k to derive phi
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k

        # Discriminant of x^2 - (n - phi + 1)x + n = 0
        s = n - phi + 1
        discr = s * s - 4 * n

        if discr >= 0 and is_perfect_square(discr):
            t = math.isqrt(discr)

            # Recover p and q
            p = (s + t) // 2
            q = (s - t) // 2
            if p * q == n:
                return d

    return None

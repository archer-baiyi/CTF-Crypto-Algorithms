from sage.all import *
from time import perf_counter

# ------------------------------------------------------------
# Multipoint polynomial evaluation attack core:
#   - Build points u_i = r^(e * i * D) in Z/NZ
#   - Build polynomial f(x) = ∏_{j=0}^{D-1} (r^(e*j) * x - r) in (Z/NZ)[x]
#   - Build a product tree M over (x - u_i)
#   - Recursively reduce f modulo subtree products to evaluate f(u_i)
#   - At each leaf, compute gcd(f(u_i), N) to extract a non-trivial factor
# ------------------------------------------------------------

def factor_N_via_multipoint_eval(N: int, e: int, D: int = 2**20, seed=None):
    """
    Factor RSA modulus N using the multipoint polynomial evaluation approach.

    Parameters
    ----------
    N : int
        RSA modulus.
    e : int
        RSA public exponent.
    D : int
        Number of points / degree parameter (typically a power of 2).
    seed : int | None
        Optional seed for Sage's RNG (for reproducibility).

    Returns
    -------
    (p, q) : tuple(int, int)
        Non-trivial factors of N such that p*q == N.

    Raises
    ------
    RuntimeError
        If no factor is found.
    """
    if seed is not None:
        set_random_seed(seed)

    t0 = perf_counter()

    # Work in Z/NZ and its polynomial ring.
    R = Zmod(N)
    P = PolynomialRing(R, 'x')
    x = P.gen()

    t1 = perf_counter()
    print(f"[time] init rings: {t1 - t0:.3f}s")

    # Choose a random element r in Z/NZ.
    r = R.random_element()

    t2 = perf_counter()
    print(f"[time] choose r: {t2 - t1:.3f}s")

    # Precompute points u_i = r^(e * i * D) for i=1..D using a recurrence.
    step = r ** (e * D)
    acc = R(1)
    u = []
    for _ in range(D):
        acc *= step
        u.append(acc)

    t3 = perf_counter()
    print(f"[time] build points u (D={D}): {t3 - t2:.3f}s")

    # Build polynomial f(x) = ∏_{j=0}^{D-1} (r^(e*j) * x - r).
    r_e = r ** e
    coef = R(1)
    f = P(1)
    for _ in range(D):
        coef *= r_e
        f *= (coef * x - r)

    t4 = perf_counter()
    print(f"[time] build polynomial f (degree~{D}): {t4 - t3:.3f}s")

    # Build product tree M for (x - u_i).
    # M is stored top-down by reversing the list of levels.
    M = [[x - ui for ui in u]]
    while len(M[-1]) > 2:
        M.append([M[-1][i] * M[-1][i + 1] for i in range(0, len(M[-1]), 2)])
    M.reverse()

    t5 = perf_counter()
    print(f"[time] build product tree M: {t5 - t4:.3f}s")

    # Exception used to early-exit recursion when a factor is found.
    class FoundFactor(Exception):
        def __init__(self, p):
            self.p = p

    def eval_find_factor(poly, start, length, o=0, k=0):
        """
        Evaluate poly at points u[start : start+length] using the product tree M.
        At leaves (length == 1), compute gcd(poly(u_i), N) to detect a factor.
        """
        if length == 1:
            val = int(poly(u[start]))
            g = gcd(val, N)
            if g != 1 and g != N:
                raise FoundFactor(g)
            return

        half = length // 2

        # Reduce polynomial modulo left/right subtree products.
        left_poly = poly % M[k][o]
        right_poly = poly % M[k][o + 1]

        # Recurse into both halves.
        eval_find_factor(left_poly, start, half, 2 * o, k + 1)
        eval_find_factor(right_poly, start + half, half, 2 * o + 2, k + 1)

    # Run evaluation and stop as soon as a non-trivial gcd is found.
    try:
        eval_find_factor(f, 0, D)
        raise RuntimeError("Could not factor N with this run (try again with a new r).")
    except FoundFactor as ex:
        p = int(ex.p)

    t6 = perf_counter()
    print(f"[time] multipoint eval + gcd scan (early exit): {t6 - t5:.3f}s")
    print(f"[time] total: {t6 - t0:.3f}s")

    q = N // p
    if p * q != N:
        raise RuntimeError("Recovered factor does not multiply back to N.")
    return (min(p, q), max(p, q))


# -----------------------------
# Example usage:
# -----------------------------
# N = <rsa modulus as int>
# e = <public exponent as int>
# p, q = factor_N_via_multipoint_eval(N, e, D=2**20)
# print("p =", p)
# print("q =", q)
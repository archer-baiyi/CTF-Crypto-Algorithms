# CTF Crypto Algorithms

CTF（网络安全竞赛）密码学方向常用算法以及论文汇总。

A Collection of Common Algorithms and Research Papers for CTF Cryptography Challenges.



## RSA

### RSA-CRT

#### Small CRT Exponent Attack

实现并优化了论文《Fast Variants of RSA》中用于证明Lemma的多点多项式求值分解算法：

> **引理**： \>设 $\langle N, e' \rangle$ 为一个 RSA 公钥，其中 $N = pq$。设 $d \in \mathbb{Z}$ 为对应的 RSA 私钥指数，满足 $d \equiv r_1 \pmod{p - 1}$ 且 $d \equiv r_2 \pmod{q - 1}$，其中 $r_1 < r_2$。如果 $r_1$ 的长度为 $m$ 比特，且我们假设 $r_1 \not\equiv r_2 \pmod{2^{m/2}}$。那么，在给定 $\langle N, e' \rangle$ 的情况下，攻击者可以在 $O(\sqrt{r_1} \log r_1)$ 的时间内恢复私钥 $d$。

，并通过代码级改进降低了运行时间与内存开销

---

Implemented and optimized the multipoint polynomial evaluation factorization algorithm used to prove the Lemma in the paper *Fast Variants of RSA*:

**Lemma.** Let $\langle N, e' \rangle$ be an RSA public key with $N = pq$. Let $d \in \mathbb{Z}$ be the corresponding RSA private exponent satisfying $d = r_1 \pmod{p - 1}$ and $d = r_2 \pmod{q - 1}$ with $r_1 < r_2$. If $r_1$ is $m$ bits long we assume that $r_1 \neq r_2 \pmod{2^{m/2}}$. Then given $\langle N, e' \rangle$ an adversary can expose the private key $d$ in time $O(\sqrt{r_1} \log r_1)$.

, reducing runtime and memory overhead through code-level improvements.


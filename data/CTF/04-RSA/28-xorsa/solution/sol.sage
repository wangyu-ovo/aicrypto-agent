from Crypto.Util.number import *
from tqdm import tqdm

def solve(tp, tq, cnt):
    print(f"\rSearched index: {cnt}/{known} Queue size: {len(ans)}", end="")
    if cnt == known:
        ans.append((tp, tq))
        return
    b = hint[cnt]
    w = 2**(1024 - cnt - 1)
    tp0, tq0, tp1, tq1 = tp, tq, tp + w, tq + w
    if b == "0": # 00 or 11
        tn0, tm0 = tp0 * tq0, (tp0 + w - 1) * (tq0 + w - 1)
        tn1, tm1 = tp1 * tq1, (tp1 + w - 1) * (tq1 + w - 1)
        if tn0 <= n <= tm0:
            solve(tp0, tq0, cnt+1)
        if tn1 <= n <= tm1:
            solve(tp1, tq1, cnt+1)
    else: # 01 or 10
        tn0, tm0 = tp0 * tq1, (tp0 + w - 1) * (tq1 + w - 1)
        tn1, tm1 = tp1 * tq0, (tp1 + w - 1) * (tq0 + w - 1)
        if tn0 <= n <= tm0:
            solve(tp0, tq1, cnt+1)
        if tn1 <= n <= tm1:
            solve(tp1, tq0, cnt+1)


bits, extra = 1024, 75
known = 1024 - (bits // 2 - extra)


from helper import *
hint = partial_p_q
hint <<= (bits // 2 - extra)
hint = format(hint, "01024b")[:known]

ans = []
solve(0, 0, 0)

PR.<x> = PolynomialRing(Zmod(n))
for p_high, _ in tqdm(ans):    
    f = p_high + x
    roots = f.small_roots(beta=0.4, X=2**(1024-known))
    if roots:
        break
p = int(f(roots[0]))
flag = pow(c, pow(e, -1, p-1), p)
print(long_to_bytes(int(flag)))
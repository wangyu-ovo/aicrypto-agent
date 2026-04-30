load('./solvelinmod.py')

from helper import *


def cusp_log(P, G, p):
    gx, gy = G
    px, py = P
    d = ( pow(gx * pow(gy, -1, p), -1, p) * (px * pow(py, -1, p)) ) % p
    return d

G = points[0]
logs = [cusp_log(P, G, p) for P in points]

xs = [var(f"x_{i}") for i in range(len(points))]
eq = (sum(x*i for x, i in zip(xs, logs)) == cusp_log(s, G, p))
bounds = {x: 1024 for x in xs}
sol = solve_linear_mod([(eq, p)], bounds)
print(b"lactf{" + bytes([i%256 for i in sol.values()]) + b"}")
# lactf{im_w4y_t00_br0k3!}
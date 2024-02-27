# from utilities_parsing import *

def OptStrategy(F, G):
    # Initialize arrays
    jF = len(F)
    jG = len(G)
    Lv = [[0] * jG for _ in range(jF)]
    Rv = [[0] * jG for _ in range(jF)]
    Hv = [[0] * jG for _ in range(jF)]
    Lw = [0] * jG
    Rw = [0] * jG
    Hw = [0] * jG
    STR = [[0] * jG for _ in range(jF)]

#     # Postorder traversal
#     for v in range(jF):
#         for w in range(jG):
#             if is_leaf_node(w):
#                 Lw[w] = Rw[w] = Hw[w] = 0
#             if is_leaf_node(v):
#                 Lv[v][w] = Rv[v][w] = Hv[v][w] = 0

#             # Compute costs
#             C = (jF * jA(G[w]) + Hv[v][w], γH(F))
#             C += (jG * jA(F[v]) + Hw[w], γH(G))
#             C += (jF * jF(G[w], ΓL(G)) + Lv[v][w], γL(F))
#             C += (jG * jF(F[v], ΓL(F)) + Lw[w], γL(G))
#             C += (jF * jF(G[w], ΓR(G)) + Rv[v][w], γR(F))
#             C += (jG * jF(F[v], ΓR(F)) + Rw[w], γR(G))

#             # Find minimum cost
#             cmin, γmin = min(C, key=lambda x: x[0])

#             # Set strategy
#             STR[v][w] = γmin

#             # Update arrays
#             if v is not root:
#                 Lv[p(v)][w] += Lcmin v[v][w] if v in γL(Fp(v)) else 0
#                 Rv[p(v)][w] += Rcmin v[v][w] if v in γR(Fp(v)) else 0
#                 Hv[p(v)][w] += H cmin v[v][w] if v in γH(Fp(v)) else 0
#             if w is not root:
#                 Lw[p(w)] += Lcmin w[w] if w in γL(Gp(w)) else 0
#                 Rw[p(w)] += Rcmin w[w] if w in γR(Gp(w)) else 0
#                 Hw[p(w)] += Hcmin w[w] if w in γH(Gp(w)) else 0

#     return STR

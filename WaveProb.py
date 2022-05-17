import math
import pandas as pd
import matplotlib.pyplot as plt
from mathconversions import c
from mathconversions import s
from mathconversions import ch
from mathconversions import sh

def waveprob(u_g0,freq,H,V,beta,t,L):

    om = 2 * math.pi * freq
    i = (-1) ** (1 / 2)
    Vs = V * (1 + 2 * beta * i) ** (1 / 2)
    q = om / Vs
    D = om * H / Vs
    A = D.real
    B = D.imag
    E = c(A) * ch(B) - i * s(A) * sh(B)
    u_ff0 = u_g0 / E
    L_0 = []
    u = []
    legend = []
    L_max = L*100
    T = (1/freq)*t
    for L in range(L_max):
        l = L / 100
        F = q * l
        G = F.real
        H = F.imag
        I = c(G) * ch(H) - i * s(G) * sh(H)
        J = c(om * T)+i*s(om * T)
        u_zzt = u_ff0 * I * J
        u_zzt = u_zzt.real

        L_0.append(-l)
        u.append(u_zzt)
        legend.append('1D-Wave')

    Wave = pd.DataFrame({'Depth':L_0,'Displacement':u,'legend':legend})

    return Wave




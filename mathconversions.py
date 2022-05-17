import math
def dg_rad(phi_dg):
    phi_r = phi_dg *(math.pi/180)
    return phi_r

def rad_dg(phi_dg):
    phi = phi_r /(math.pi/180)
    return phi

def s(x):
    s = math.sin(x)
    return s
def sh(x):
    sh = math.sinh(x)
    return sh
def c(x):
    c= math.cos(x)
    return c
def ch(x):
    ch = math.cosh(x)
    return ch
def s2(x):
    s2 = (math.sin(x))**2
    return s2
def c2(x):
    c2 = (math.cos(x))**2
    return c2
def bs(x):
    bs = math.asin(x)
    return bs
def t(x):
    t = math.tan(x)
    return t
def t2(x):
    t2 = math.tan(x)**2
    return t2
def bt(x):
    bt = math.atan(x)
    return bt
def bt2(x):
    bt2 = math.atan(x)**2
    return bt2
def ac(x):
    ac = math.acos(x)
    return ac
def cot(x):
    cot = 1/math.tan(x)
    return cot
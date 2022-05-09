import math
from mathconversions import s
from mathconversions import c
from mathconversions import s2
from mathconversions import c2
from mathconversions import bs
from mathconversions import t
from mathconversions import t2
from mathconversions import bt
from mathconversions import bt2
from mathconversions import ac

#Simplified Rankine
def KASR(phi):
    ka = (1-s(phi))/(1+s(phi))
    return ka

def KPSR(phi):
    kp = (1+s(phi))/(1-s(phi))
    return kp

#General Rankine
def KAGR(phi,beta,eta):

    phi_a = (bs(s(beta) / s(phi))) - beta + 2 * eta
    ka = (c(beta - eta) * (1 + s2(phi) - 2 * s(phi) * c(phi_a)) ** (1 / 2)) / (
                c2(eta) * (c(beta) + (s2(phi) - s2(beta)) ** (1 / 2)))
    return ka

def KPGR(phi,beta,eta):

    phi_p = (bs(s(beta) / s(phi))) + beta - 2 * eta
    kp = (c(beta - eta) * (1 + s2(phi) + 2 * s(phi) * c(phi_p)) ** (1 / 2)) / (
            c2(eta) * (c(beta) - (s2(phi) - s2(beta)) ** (1 / 2)))
    return kp

#Coulomb
def KAC(phi,beta,eta,delta):

    try:
        ka = (c2(phi - eta)) / (c2(eta) * c(eta + delta) * (1 + (
                (s(phi + delta) * s(phi - beta)) / (
                c(eta + delta) * c(eta - beta))) ** (1 / 2)) ** 2)
    except ZeroDivisionError:
        ka = 0
    return ka

def KPC(phi,beta,eta,delta):

    try:
        kp = (c2(phi + eta)) / (c2(eta) * c(eta - delta) * (1 - (
                (s(phi + delta) * s(phi + beta)) / (
                c(eta - delta) * c(eta - beta))) ** (1 / 2)) ** 2)
    except ZeroDivisionError:
        kp = 50
    if kp >50:
        kp = 50

    return kp

#Caquot and Kerisel
def ck_calc(x,y):
    ck_15 = [0.78, 0.80, 0.83, 0.85, 0.88, 0.91, 0.93, 0.96]
    ck_20 = [0.68, 0.72, 0.75, 0.79, 0.82, 0.86, 0.90, 0.94]
    ck_25 = [0.57, 0.62, 0.67, 0.71, 0.76, 0.81, 0.86, 0.91]
    ck_30 = [0.47, 0.52, 0.57, 0.63, 0.69, 0.75, 0.81, 0.88]
    ck_35 = [0.36, 0.42, 0.48, 0.54, 0.60, 0.67, 0.75, 0.84]
    ck_40 = [0.26, 0.32, 0.38, 0.44, 0.51, 0.59, 0.68, 0.78]

    table = [ck_15, ck_20, ck_25, ck_30, ck_35, ck_40]
    if y >= 0.7:
        y = 0.7
    else:
        y = y
    if x >= 40:
        x=40
    if x < 15:
        x=15
    x = x



    X_1 = math.floor(x / 5) - 3
    X_2 = math.ceil(x / 5) - 3
    Y_1 = math.floor(y * 10)
    Y_2 = math.ceil(y * 10)



    x_1 = table[X_1][Y_1]
    x_2 = table[X_1][Y_2]
    y_1 = table[X_2][Y_1]
    y_2 = table[X_2][Y_2]

    try:
        x_i = x_1 + (x_2 - x_1) / ((Y_2 / 10) - (Y_1 / 10)) * (y - (Y_1 / 10))
        y_i = y_1 + (y_2 - y_1) / ((Y_2 / 10) - (Y_1 / 10)) * (y - (Y_1 / 10))
    except ZeroDivisionError:
        x_i = x_1
        y_i = y_1
    try:
        ck = x_i + (y_i - x_i) / (((X_2 + 3) * 5) - ((X_1 + 3) * 5)) * (x - ((X_1 + 3) * 5))
    except ZeroDivisionError:
        ck = x_i
    return ck


def KPCK(phi,beta,eta,delta):
    try:
        kp_c = (c2(phi + eta)) / (c2(eta) * c(eta - delta) * (1 - (
                (s(phi + delta) * s(phi + beta)) / (
                c(eta - delta) * c(eta - beta))) ** (1 / 2)) ** 2)
    except ZeroDivisionError:
        kp_c = 1000
    f = ck_calc(phi,delta/phi)
    kp = kp_c * f
    if kp > 50:
        kp = 50
    return kp

#Lancellotta
def KAL(phi,delta):

    theta_ka = (1 / 2) * bs(s(delta) / (s(phi))) - delta

    ka = (c(delta) / (1 + s(phi))) * (c(delta) - (s2(phi) - s2(delta)) ** (1 / 2)) * math.e ** (
                -2 * theta_ka * t(phi))
    return ka

def KPL(phi,delta):
    theta_kp = (1 / 2) * bs(s(delta) / s(phi)) + delta

    kp = (c(delta) / (1 - s(phi))) * (c(delta) + (s2(phi) - s2(delta)) ** (1 / 2)) * math.e ** (
            2 * theta_kp * t(phi))
    return kp

#Paik and Salgado
def KAPS(phi,delta):

    N = (1 + s(phi)) / (1 - s(phi))

    if (((N - 1) ** 2) - (4 * N * t2(delta)) ** 2) < 0:
        theta = 0
    else:
        theta = bt(((N - 1) + (((N - 1) ** 2) - (4 * N * t2(delta)) ** 2) ** (1 / 2)) / (2 * t(delta)))

    if theta == 0:
        ka = 0
    else:
        ka = (3 * (N * c2(theta) + s2(theta))) / (3 * N - (N - 1) * c2(theta))

    return ka

#Muller Breslau

def KAMB(phi,delta):
    ka = c2(phi) / ((1 + ((s(phi) * s(delta + phi)) / (c(delta))) ** (1 / 2)) ** 2)
    return ka

def KPMB(phi,delta):
    kp = c2(phi) / ((1 - ((s(phi) * s(delta + phi)) / (c(delta))) ** (1 / 2)) ** 2)
    return kp

#Kötter

def KAK(phi,delta):
    aa = (ac(s(delta) / s(phi)) - phi + delta) * (1 / 2)
    ka = ((1 - s(phi) * s(2 * aa + phi)) / (1 + s(phi))) * math.e ** (
                ((-math.pi / 2) + phi + 2 * aa) * t(phi))
    return ka

def KPK(phi,delta):
    ap = (ac(s(delta) / s(phi)) + phi - delta) * (1 / 2)
    kp = ((1 - s(phi) * s(2 * ap + phi)) / (1 + s(phi))) * math.e ** (
                ((math.pi / 2) + phi + 2 * ap) * t(phi))

    return kp
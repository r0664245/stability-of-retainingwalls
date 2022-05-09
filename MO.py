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
from mathconversions import cot

#Classic Monobe-Okabe

def th(kh,kv):
    th = bt(kh/(1-kv))
    return th
    
def moa(phi,delta,beta,eta,theta):
    if (phi-theta-beta)<0:
        k_ae = 0
    else:
        k_ae = c2(phi - theta - eta) / (c(theta) * c2(eta) * c(delta + eta + theta) * (1 + (
                (s(phi + delta) * s(phi - theta - beta)) / (
                c(delta + eta + theta) * c(beta - eta))) ** (1 / 2)) ** 2)

    return k_ae

def mop(phi,delta,beta,eta,theta):

    if (phi + beta - theta) < 0:
        k_pe = 0
    else:
        try:
            k_pe = c2(phi - theta + eta) / (c(theta) * c2(eta) * c(delta - eta + theta) * (1 - (
                    (s(phi + delta) * s(phi - theta + beta)) / (
                    c(delta - eta + theta) * c(beta - eta))) ** (1 / 2)) ** 2)
        except ZeroDivisionError:
            k_pe = 50
        if k_pe > 50:
            k_pe = 50
        else:
            k_pe = k_pe

    return k_pe

def Pae(gamma,H,kv,Kae):
    Pae = (1/2)*gamma*(1-kv)*Kae*H**2
    return Pae

def L(Pae,Pad,H):
    L = (Pae*(H/3)+Pad*0.6*H)/Pae
    return L

#comparing upwards and downwards seicmic forces
def compare(mo_u,mo_d):
    if mo_u == 0:
        R = 0
    else:
        if mo_d == 0:
            R = 0
        else:
            R = (mo_d - mo_u)/mo_u
    return R

#adaptation by Abodium Ismail Lawal
def A(phi,alpha,delta):
    A = (cot(phi + alpha)-t(delta))/(cot(alpha)*(1+cot(phi+alpha))*t(phi))
    return A

def B(phi,alpha,kh,kv):
    B = ((1-kv)-cot(phi+alpha)*kh)/((1+cot(phi+alpha))*t(phi))
    return B

def a(delta,theta,phi):
    a = c(delta)*c(theta)*s(phi+delta)*c(phi-theta)
    return a

def b(delta,theta,phi):
    b = c(delta)*c(theta)*s(phi*delta)*s(theta-phi)
    return b

def C(delta,theta,phi):
    C = c(theta)*c(delta)*s(theta-phi)*c(phi+delta)
    return C

def alpha(a,b,c):
    alpha = bt((b+((b**2)-a*c)**(1/2))/a)
    return alpha

def SV_AIL(A,B,gamma,kp,L,H):
    SV_AIL = ((B*gamma*kp)/(A*kp-2))*(L-(H**(2-A*kp))*L**(A*kp-1))
    if SV_AIL < 0:
        SV_AIL = 0
    return SV_AIL

def SH_AIL(SV_AIL,kp):
    SH_AIL = SV_AIL*kp
    return SH_AIL

def P_AIL(gamma,H,kv,delta,alpha,phi,theta):
    P_AIL = (1/2)*gamma*(H**2)*(1-kv)*((c(delta)*c(alpha)*s(phi+alpha-theta))/(c(delta)*s(alpha)*c(phi+alpha+delta)))
    return P_AIL

def H_AIL(H,phi,alpha,delta,kp):
    H_AIL = (2/3)*((c(phi)*c(phi+alpha+delta)*kp)/(c(phi)*c(phi+alpha+delta)*kp+c(delta)*cot(alpha)*s(2*phi+alpha)))
    return H_AIL

#adaptation by Mylonakis, Kloukinas, Papantonopoulos

def KEA_MKP(eta,beta,theta,phi,delta,d1_s,d2,theta_e):
    KEA_MKP = ((c(eta-beta)*c(beta+theta))/(c(theta)*c(delta)*c2(eta)))*((1-s(phi)*c(d2-delta))/(1+s(phi)*c(d1_s+(beta+theta))))*math.e**(-2*theta_e*t(phi))
    return KEA_MKP

def KEP_MKP(eta,beta,theta,phi,delta,d1_s,d2,theta_e):
    KEP_MKP = ((c(eta - beta) * c(beta + theta)) / (c(theta) * c(delta) * c2(eta))) * (
                (1 + s(phi) * c(d2 + delta)) / (1 - s(phi) * c(d1_s - (beta + theta)))) * math.e ** (
                          2 * theta_e * t(phi))
    return KEP_MKP

def d1(beta,phi):
    d1 = bs(s(beta)/s(phi))
    return d1

def d1_s(beta,phi,theta):
    if phi > beta + theta:
        d1_s = bs(s(beta+theta)/s(phi))
    else : d1_s = math.pi/2
    return d1_s

def d2(delta,phi):
    d2 = bs(s(delta)/s(phi))
    return d2

def theta_EA(d1_s,d2,delta,beta,eta,theta):
    theta_EA = (1/2)*(d2-(d1_s+delta)+beta-2*eta-theta)
    return theta_EA

def theta_EP(d1_s,d2,delta,beta,eta,theta):
    theta_EP = (1/2)*(d2+(d1_s+delta)+beta-2*eta-theta)
    return theta_EP

def Keq(k,eta,beta):
    keq = k*((c(eta))/(c(eta-beta)))
    return keq


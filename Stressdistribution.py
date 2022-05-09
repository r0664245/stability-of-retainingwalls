import math
from mathconversions import t

def sigma_v(H,gamma):
    sigma_v = H*gamma
    return sigma_v

def sigma_ha(ka,sigma_v):
    sigma_ha = ka*sigma_v
    return sigma_ha

def sigma_hp(kp,sigma_v):
    sigma_hp = kp*sigma_v
    return sigma_hp

def sigma_v_ps(ka,gamma,H,h,delta,phi):
    sigma_v = ((gamma * (H)) / (1 - ka * t(delta) * t((math.pi / 4) + phi / 2))) * (
                (1 - ((h) / (H))) ** (ka * t(delta) * t(( math.pi / 4) + phi / 2)) - (
                    1 - ((h) / (H))))
    return sigma_v

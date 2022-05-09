from mathconversions import t

def FKA(ka,H,gamma):
    F = (1 / 2) * ka * gamma * H ** 2
    return F

def FKP(kp,H,gamma):
    F = (1 / 2) * kp * gamma * H ** 2
    return F

def KAW(ka,delta,N):
    kaw = (ka/(1-ka*t(delta)*N**(1/2)))*((2/1+ka*t(delta)*N*(1/2))-1)

    return kaw


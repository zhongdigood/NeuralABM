def fcn(dis, vel, SC_Damper, Cstress, Cstrain):
    import numpy as np
    k1 = SC_Damper[0]  # 20000
    k2 = SC_Damper[1]  # 1000
    k3 = SC_Damper[1]  # 1000
    ActF = SC_Damper[2]  # 10000
    ResF = SC_Damper[3]  # 4000
    c = SC_Damper[4]  # 40
    gap = SC_Damper[5]  # 1.5

    if dis <= -gap:
        dis=dis + gap
    elif dis >= gap:
        dis=dis-gap
    else:
        dis=0;

    Tstrain = dis
    dStrain = Tstrain - Cstrain
    ActDef = ActF / k1
    ResDef = ResF / k1
    TupperStressPos = ActF + (Tstrain - ActDef) * k2
    TlowerStressPos = ResF + (Tstrain - ResDef) * k3
    TupperStressNeg = (Tstrain + ActDef) * k2 - ActF
    TlowerStressNeg = (Tstrain + ResDef) * k3 - ResF  
    Tstress = Cstress + k1 * dStrain

    if Tstrain > ResDef:
        if Tstress > TupperStressPos:
            Tstress = TupperStressPos
        elif Tstress < TlowerStressPos:
            Tstress = TlowerStressPos
        else:
            Tstress = Cstress + k1 * dStrain

    elif Tstrain < - ResDef:
        if Tstress < TupperStressNeg:
            Tstress = TupperStressNeg
        elif Tstress > TlowerStressNeg:
            Tstress = TlowerStressNeg
        else:
            Tstress = Cstress + k1 * dStrain
    else:
        Tstress = k1 * Tstrain

    f = Tstress + vel * c
    return Tstress, Tstrain, f

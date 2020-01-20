import math
import numpy as np

#---------------------------------------------------------
# Inputs
#---------------------------------------------------------

P = float(input('Axial Force (P) = '))
M = float(input('Moment (M) = '))
fck = float(input('Characteristic strength of Concrete (fck)= '))
s_f = float(input('Size of Weld for flange(s_f) = '))
s_w = float(input('Size of Weld for web(s_w) = '))
gamma_mo = float(input('gamma_mo ='))
gamma_mb = float(input('gamma_mb ='))
tau_bd = float(input('tau_bd ='))
Es = float(input('Modulus of elasticity (Es) = '))

# Base plate and anchor details
L = float(input('Length of base plate (L) = '))
B = float(input('width of base plate (B) = '))
c = float(input('Projection of base plate(c) = '))
a = float(input('End distance of anchor bolt (a) = '))
d = float(input('Diameter of anchor bolt (d) = '))

# Section details
D = float(input('Depth of Section (D) = '))
bf = float(input('Width of Section (bf) = '))
t_f = float(input('Thickness of flange(t_f) = '))
t_w = float(input('Thickness of web(t_w) = '))
A_cs = float(input('Cross section of section = '))
f_y = float(input('yield strength of plate(f_y) = '))
fu = float(input('ultimate strength(fu) = '))

e = M/P*1000
print('Eccentricity =',e)

def find_case():
    if M == 0:
        print ('Only axial load condition occurred')
    elif M > 0:
        if e < L / 6:
            print ('e < L/6 No Tension occured in base plate.')
        elif e == L/6 :
            return ('We design as L =6*e, Therefore no tension condition occured.')
        elif L / 6 < e < L / 3:
            print ('L/6 < e < L/3 Small Tension occured in base plate.')
        elif e > L / 3:
            print ('e > L/3 Large Tension occured in base plate.')
        else:
            print ('Eccentricity beyond the edges of base plate.')
    else:
        return

find_case()

#--------------------------------------
# Finding length of compressive area
#-------------------------------------
f = (L/2) - a
print (f)
Ec = 5000 *math.sqrt(fck)
n = Es/Ec

print (n)

As = (math.pi/4) * d**2 *2

K0 = 1
K1 = 3*(e-(D/2))
K2 = (6*n*As*(f+e))/B
K3 = -K2*((D/2)+f)
print(K1, K2, K3)

coeff = [K0, K1, K2, K3 ]

"""
Solving cubical equation :
 Y**3 +K1*Y**2 +K2*Y +K3 =0
 were, K1, K2, K3 is coefficient given by 'Omer Blodgett'
"""
def length_comp():
    Y = np.roots(coeff)
    Y = (np.max(Y))
    Y = math.ceil(Y.real)
    return Y

print (length_comp())

#--------------------------------------
# Finding tension
#-------------------------------------
"""
Tension calculated on anchor Bolt,
Reference : Omer Blodgett
"""
def finding_tension():
    Pt = - P*(((D/2)-(length_comp()/3)-e)/(((D/2)-(length_comp()/3)+f)))
    return Pt
print(finding_tension())

#------------------------------------
# Design of anchor of bolt
#-----------------------------------
Anb = 0.78*(math.pi/4)*d**2
def tensile_cap():
    global T
    T = (0.9*Anb*fu)/gamma_mb
    N = math.ceil(finding_tension()/T)
    if N < 2 :
        return 2
    elif N >= 2 :
        return N
print(tensile_cap())

def length_bolt():
    k =15.5
    l1 = (d*f_y)/(4* tau_bd*gamma_mo)
    l2 = ((T)/(k*math.sqrt(fck)))**(1/1.5)
    l= max(l1,l2)
    return l
print( length_bolt())

#-------------------------------------
# maximum stress
#-----------------------------------

def max_stress():
    p_max = (2*(P +finding_tension())*1000)/(length_comp()*B)
    if p_max < (0.45*fck):
        return p_max
    elif p_max > 0.45 *fck :
        return 'it is not safe, therefore increasing width of base plate '
    else :
        return

print (max_stress())

#-----------------------------------------
# Thickness of base plate
#---------------------------------------

# p-max at critical section

def thick_plate() :
    y = float((max_stress() * (length_comp() - c)) / length_comp())
    M_x = ((y* c**2)/2) + (2*(max_stress()-y)*c**2)/6
    t_p = math.sqrt((M_x * gamma_mo * 6) / (1.2 * f_y))
    return math.ceil(t_p)
print(thick_plate())

#-------------------------------------
# Design of Weld
#-------------------------------------

# Axial load on flange and web
def total_load():
    """
       Axial load shared by flange,
       = (P * 2 * Area of flange)/(Cross sectional area of I-section)
    """
    p_moment = float((M * 1000) / (D - t_f))
    A_f = bf * t_f
    p_force = float((P* 2* A_f)/A_cs)
    p_flange = p_force / 2
    global p_web
    p_web = P - p_force
    return (p_flange + p_moment)
print('Axial load shared by flange =',total_load())


# Effective length of weld for flange
def length_eff_f():
    """
    [Reference: IS:800-2007, cl.no.10.5.7.1.1., Pg.No.79]

    Strength of fillet weld per mm length,
            = (l_w * t_t * fu)/(sqrt(3) * gamma_mw)
     """

    l_w = 1
    t_t = 0.7 * s_f
    q = float((l_w*t_t*fu)/(math.sqrt(3)*gamma_mb))
    global l_eff_f
    l_eff_f = (total_load() * 1000) / q
    return l_eff_f
print ('Effective length of weld for flange= ',length_eff_f())


# Available length for weld on each flange
def length_fla():
    if M > 0:
        L_a = bf + (bf - t_w)

        if L_a > l_eff_f:
            return 'It is safe. Hence provide length =',L_a
        elif L_a < l_eff_f:
            return 'It is not safe. Hence, extra plate is provided to the flange.',l_eff_f
        else:
            return()

print (length_fla())


# Effective length of weld for web
def length_eff_w():
    """
    [Reference: IS:800-2007, cl.no.10.5.7.1.1., Pg.No.79]

        Strength of fillet weld per mm length,
            = (l_w * t_t * fu)/(sqrt(3) * gamma_mw)
    """
    if M > 0:
        l_w = 1
        t_t = 0.7 * s_w
        q = float((l_w*t_t*fu)/(math.sqrt(3)*gamma_mb))
        global l_eff_w
        l_eff_w = float((p_web * 1000) / q)
        return l_eff_w
print ('Strength per mm length =',length_eff_w())


# Available length of weld for web
def length_web():
    if M > 0:
        L_a1 = float((2 * (D - (2 * t_f))))
        if L_a1 > l_eff_w:
            return 'It is safe. Hence provide lenght =',L_a1
        elif L_a1 < l_eff_w:
            return 'It is not safe. Hence, extra plate is provided to the web.',l_eff_w
        else:
            return
print (length_web())

import math

# ------------------------------------------------------------
# Base Plate No Tension Condition with Moment and Axial Force
# ------------------------------------------------------------

# Dictionary of grade of concrete
bearing_str = {'M10': (0.45 * 10), 'M15': (0.45 * 15), 'M20': (0.45 * 20), 'M25': (0.45 * 25), 'M30': (0.45 * 30),
               'M35': (0.45 * 35),
               'M40': (0.45 * 40), 'M45': (0.45 * 45), 'M50': (0.45 * 50), 'M55': (0.45 * 55), 'M60': (0.45 * 60),
               'M65': (0.45 * 65),
               'M70': (0.45 * 70), 'M75': (0.45 * 75), 'M80': (0.45 * 80)}
print(bearing_str.keys())
print(bearing_str['M20'])

# ----------------------------------------------------------
# Inputs
# ---------------------------------------------------------

P = float(input('Axial Force (P) = '))
M = float(input('Moment (M) = '))
fck = float(input('Characteristic strength of Concrete (fck)= '))
s_f =float(input('Size of Weld for flange(s_f) = '))
s_w =float(input('Size of Weld for web(s_w) = '))
gamma_mo =1.1 #float(input('gamma_mo ='))
gamma_mw =1.25 #float(input('gamma_mw ='))

# Section details
D = float(input('Depth of Section (D) = '))
bf = float(input('Width of Section (bf) = '))
t_f =float(input('Thickness of flange(t_f) = '))
t_w = float(input('Thickness of web(t_w) = '))
A_cs =float(input('Cross section of section = '))
f_y =250 #   float(input('yield strength of plate(f_y) = '))
fu =410 #float(input('ultimate strength = '))

# ---------------------------------------------------
# Estimation of Area
# ---------------------------------------------------

e = (M / P) * 1000
print('Eccentricity(e)= ', e)


# Minimum required area
def area_req():
    if M == 0:
        A_req = float((P / (0.45 * fck)))
        c = 1
        x = c ** 2 * 4
        y = c * 2 * (D + (2 * bf) - t_w)
        z = (bf * D) - (D * (bf - t_w)) + (2 * t_f * (bf - t_w)) - A_req * 1000
        global C
        C = math.ceil((-y + math.sqrt((y ** 2) - (4 * x * z))) / (2 * x))
        print ('Effective projection of Base plate from side of section =', C)
    else:
        print ('No requirement of calculating area, calculate L & B')


"""
(Ref : IS 800 : 2007, cl no. 7.4.3)

Effective bearing area, 
A_req = (bf +2c)*(D +2c)-[(D-2*(t_f+c))*(bf-t_w)]
simplify above equation we get,
 A_req*1000 =[C**2 * 4] + [C * 2*(D+(2*bf)-t_w)] + [(bf*D)-(D*(bf-t_w))+(2*t_f*(bf-t_w))]

Finding out Value of C from quadratic equation by standard formula as below,
   C = (-b+math.sqrt((b**2)-(4*a*c)))/(2*a)
   where, a = x ; b = y ; c = z 
   C = projection of base plate
   assume  C (unknown)= 1 for simplification in x,y,z
"""
area_req()

# -------------------------------------------------
# Length of base plate
# --------------------------------------------------
global L
L = int(6 * e)


def find_length():
    if M == 0:
        return D + (2 * C)
    elif M > 0:
        if L > D:
            return L
        elif L < D:
            return (D + 2 * 100)

print ('Length of plate =',find_length())


# ----------------------------------------------
# Identifying type of case
# ----------------------------------------------

def find_case():
    if M == 0:
        print('Only axial load condition occurred')
    elif M > 0:
        if e < find_length() / 6:
            print('e < L/6 No Tension occured in base plate.')
        elif e == find_length() / 6:
            print ('We design as L =6*e, Therefore no tension condition occured.')
        elif find_length() / 6 < e < find_length() / 3:
            print('L/6 < e < L/3 Small Tension occured in base plate.')
        elif e > find_length() / 3:
            print('e > L/3 Large Tension occured in base plate.')
        else:
            print('Eccentricity beyond the edges of base plate.')
    else:
        return


find_case()


# ------------------------------------------------------
# Width of base plate
# -----------------------------------------------------

def calc_width():
    if M == 0:
        B = bf + (2 * C)
        return B
    elif M > 0:
        B = round(((2 * P * 1000) / (find_length() * 0.45 * fck)),2)
        """ [Reference: N.Subramanian, Example:15.3, Pg.No.661] """
        if e <= (find_length() / 6):
            if B < bf:
                return float(bf + 75 + 75)
            elif B > bf:
                return B
        elif e > (L / 6):
            return 'tension condition occured'


print('Width of plate =',calc_width())

# projection
if M > 0:
    b = (calc_width() - bf) / 2
    a = (find_length() - D) / 2

# -------------------------------------------------
# Calculate p_max. and p_min.
# -------------------------------------------------

def stress():
    """
    [Reference: N.Subramanian, cl.no.:15.4.1, Pg.No.651]

         maximum or minimum stress = (P/A) +- (M/Z)
         where,
            P = Axial load
            A = Area of base plate
            M = Moment coming on base plate
            Z = section modulus of base plate

            where, Z =(l*t**2)/6
    """
    if M == 0:
        pass
    elif M > 0:
        A = find_length() * calc_width()
        Z_e = (calc_width() * find_length() ** 2) / 6
        global p_max
        p_max = round(((P * 1000 / A) + (M * 10**6 / Z_e)),3)
        p_min = round(((P * 1000 / A) - (M * 10**6 / Z_e)),3)
        return (p_max, p_min)

print(stress())

# ----------------------------------------------
# Thickness of base plate
# ----------------------------------------------

# Moment due to stress
def moment():
    if M == 0:
        pass
    elif M > 0:
        Y = round((((p_max * find_length() - a)) / find_length()),2)
        M_x = ((Y * a*a) / 2) + ((a * (a / 2) * (p_max - Y) * (2/3)))
        return M_x

print ('moment :',moment())


# thickness of base plate
def thick_plate():
    """
        [Reference: IS:800-2007, cl.no.7.4.3.1, Pg.No.47]

        Moment due to stress on base plate = Moment capacity of base plate
        where,
         Moment due to stress on base plate = M_x (calculated)
         Moment capacity of base plate = (1.2* f_y* Z)/(gamma_mo)
         Z = (l/mm* t**2)/6

        therefore,
         M_x = (1.2* f_y* L/mm* t**2)/(gamma_mo* 6)
         By simplifying equation we get thickness of plate As below...
        """
    w = (P * 1000) / (find_length() * calc_width())
    if M == 0:
        t_p = math.ceil(math.sqrt((2.5 * 0.6 * fck * C ** 2 * gamma_mo) / f_y))
        if t_p > t_f:
            print ('Thickness of base plate is (t_p) =', t_p)
        elif t_p < t_f:
            print ('Thickness of base plate is (t_p) = ', t_f)
    elif M > 0:
        t_p = math.ceil(math.sqrt((moment() * gamma_mo * 6) / (1.2 * f_y)))
        if t_p > t_f:
            print ('Thickness of base plate is (t_p) =', t_p)
        elif t_p < t_f:
            print ('Thickness of base plate is (t_p) = ', t_f)


thick_plate()


# -------------------------------------
# Design of Weld
# -------------------------------------

# Axial load on flange and web
def total_load():
    """
       Axial load shared by flange,
       = (P * 2 * Area of flange)/(Cross sectional area of I-section)
    """
    p_moment = float((M * 1000) / (D - t_f))
    A_f = bf * t_f
    p_force = float((p_moment * 2 * A_f) / A_cs)
    p_flange = p_force / 2
    global p_web
    p_web = P - p_force
    if M == 0 :
        return round((p_flange + p_web),2)
    elif M > 0 :
        return round((p_flange),2)

print('Axial load shared by each flange =', total_load())


# Effective length of weld for flange
def length_eff_f():
    """
    [Reference: IS:800-2007, cl.no.10.5.7.1.1., Pg.No.79]

    Strength of fillet weld per mm length,
            = (l_w * t_t * fu)/(sqrt(3) * gamma_mw)
     """

    l_w = 1
    t_t = 0.7 * s_f
    q = ((l_w * t_t * fu) / (math.sqrt(3) * gamma_mw))
    global l_eff_f
    l_eff_f = (total_load() * 1000) / q
    return round(l_eff_f,3)


print('Effective length of weld = ', length_eff_f())


# Available length for weld on each flange
def length_fla():
    if M == 0:
        pass
    elif M > 0:
        L_a = math.ceil(bf + (bf - t_w))

        if L_a > l_eff_f:
            print ('It is safe. Hence provide length =', L_a)
        elif L_a < l_eff_f:
            print ('It is not safe. Hence, extra plate is provided to the flange. =', l_eff_f)

length_fla()


# Effective length of weld for web
def length_eff_w():
    """
    [Reference: IS:800-2007, cl.no.10.5.7.1.1., Pg.No.79]

        Strength of fillet weld per mm length,
            = (l_w * t_t * fu)/(sqrt(3) * gamma_mw)
    """
    if M == 0:
        pass
    elif  M > 0:
        l_w = 1
        t_t = 0.7 * s_w
        q = float((l_w * t_t * fu) / (math.sqrt(3) * gamma_mw))
        global l_eff_w
        l_eff_w = round(((p_web * 1000) / q),3)
        print ('Effective length of web =',l_eff_w)

length_eff_w()


# Available length of weld for web
def length_web():
    if M ==0:
        pass
    elif M > 0:
        L_a1 = math.ceil(2 * (D - (2 * t_f)))
        if L_a1 > l_eff_w:
            print ('It is safe. Hence provide length =', L_a1)
        elif L_a1 < l_eff_w:
            print ('It is not safe. Hence, extra plate is provided to the web.', l_eff_w)

length_web()

# Available total length of weld
def length_total():
    if M > 0 :
        pass
    elif M == 0:
        L_total = math.ceil(2 * (bf + (bf - t_w) + (D - t_f)))
        if L_total > l_eff_f:
            print ('It is safe. Hence provide length =', L_total)
        elif L_total < l_eff_f:
            print ('It is not safe. Hence, extra plate is provided to the section.', l_eff_f)

print(length_total())
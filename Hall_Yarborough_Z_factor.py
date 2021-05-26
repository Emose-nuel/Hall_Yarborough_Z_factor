import math
import time
#############################################################################################################################################################################
#CALCULATE PSEUDO-CRITICAL AND PSEUDO-REDUCED TEMPERATURE AND PRESSURE:
#############################################################################################################################################################################
def pseudo_critical_pressure( s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction):
    Ppc = 678 - 50 * (s_gravity - 0.5) - 206.7 * n2MolFraction + 440 * cO2MolFraction + 606.7 * h2SMolFraction
    return Ppc

def pseudo_critical_temperature( s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction):
    Tpc = 326 + 315.7 * (s_gravity - 0.5) - 240 * n2MolFraction - 83.3 * cO2MolFraction + 133.3 * h2SMolFraction
    return Tpc

def pseudo_reduced_temperature(temp):
    Tpc = pseudo_critical_temperature( s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction)
    Tpr = (temp + 460.0) / Tpc
    return Tpr

def reciprocal_Tpr(Tpr):
    t= 1 / Tpr
    return t

def pseudo_reduced_pressure(press):
    Ppc = pseudo_critical_pressure( s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction)
    Ppr = press / Ppc
    return Ppr
# print(f"temp_pc : {temp_pc}; press_pc : {press_pc}; temp_pr :{temp_pr}; press_pr : {press_pr}; t : {t}" )

#############################################################################################################################################################################
## DEFINE THE NEWTON-RAPHSON TECHNIQUE SOLVE FOR THE REDUCED DENSITY, Y
### DEFINE THE HALL-YARBOROUGH Z-FACTOR
#############################################################################################################################################################################

def newton_raphson_reduced_density(Ppr, t, Y=0):
    A = 0.06125 * t * math.exp (-1.2 * (1 -t) **2)
    B = t * (14.76 - 9.76 * t + 4.58 * t ** 2)
    C = t * (90.7 - 242.2 * t + 42.4 * t ** 2)
    D = 2.18 + 2.82 * t
    print (f'A = {A}; B = {B}; C = {C}; D = {D}')
    for i in range(1000):
        f = (((Y + Y**2 + Y**3 - Y**4) / ((1 - Y)**3)) -
              A * Ppr - B * Y**2 + C * Y**D)
        df = (((1 + 4 * Y + 4 * Y ** 2 - 4 * Y ** 3 + Y ** 4) /
             ((1- Y) ** 4)) - 2 * B * Y + C * D * Y ** (D - 1))
        Y1 = Y - (f / df)
        if Y1 == Y or abs((Y1 - Y) / Y1) < 0.0005:
            break
        Y = Y1
    return Y

def hall_yarborough_Z_factor(temp, press, s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction):
    pseudo_reduced_press = pseudo_reduced_pressure(press)
    pseudo_reduced_temp = pseudo_reduced_temperature(temp)
    t = reciprocal_Tpr(pseudo_reduced_temp)
    reduced_density_Y = newton_raphson_reduced_density(pseudo_reduced_press, t)
    A = 0.06125 * t * math.exp (-1.2 * (1 -t) **2)
    z_factor = round (A * pseudo_reduced_press / reduced_density_Y, 2)
    print(f"Tpr = {round(pseudo_reduced_temp, 2)}; Ppr = {round (pseudo_reduced_press, 2)}; Y = {round(reduced_density_Y, 4)}")
    return z_factor
#############################################################################################################################################################################
# CALCULATE Z-FACTOR
#############################################################################################################################################################################
Next = (input ("Do you want to perform a calculation? Enter yes/y to continue or any key to cancel : ")).lower()
while (Next == 'yes' or Next == 'y') :
    try:
        temp = float(input("Enter the temperature in Fahrenheit : ")) #180 Fahrenheit
        press = float(input("Enter the pressure in psi : ")) #2000 # psia
        s_gravity = float(input("Enter the specific gravity of the gas mixture : ")) #0.7
        n2MolFraction = float(input("Enter the mole fraction of nitrogen : ")) #0.005
        cO2MolFraction = float(input("Enter the mole fraction of CO2 : ")) #0.02
        h2SMolFraction = float(input("Enter the mole fraction of H2S : ")) #0.001
    except :
        print("You have entered an invalid number")
        time.sleep(5)
        quit()
    try:
        z_factor = hall_yarborough_Z_factor(temp, press, s_gravity, n2MolFraction, cO2MolFraction, h2SMolFraction)
        print (f'z-factor = {z_factor}')
        time.sleep(1)
        Next = (input ("Do you want to perform another calculation? yes/no : ")).lower()
    except:
        print("The Newton-Raphson method failled to converge for the input parameters")
        time.sleep(5)
        Next = (input ("Do you want to perform another calculation? yes/no : ")).lower()

# perform_cal()

import math

nm = []
baseline = []
spectrum = []
baseline2 = []
spectrum2 = []
absorption = []
nmPlot = []
absorPlot = []
accum = 1
average = 0


def wavelength():
    for i in range(0, 288):  # initilizing arrays
        nm.append(i)
        baseline.append(i)
        baseline[i] = 0
        spectrum.append(i)
        baseline2.append(i)
        baseline2[i] = 0
        spectrum2.append(i)
        spectrum2[i] = 0
        absorption.append(i)

        # calculating wavelengths from the formula provided by manufacturer
        k = (
            3.059651344 * math.pow(10, 2)
            + 2.716298429 * i 
            - 1.284751120 * math.pow(10, -3) * math.pow(i, 2)
            - 6.672071166 * math.pow(10, -6) * math.pow(i, 3)
            + 5.557539172 * math.pow(10, -9) * math.pow(i, 4)
            + 1.015634508 * math.pow(10, -11) * math.pow(i, 5)
        )
        nm[i] = k

    return nm

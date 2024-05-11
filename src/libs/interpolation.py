import numpy as np

from libs.fileutil import write_data


def interpolate():

    with open("./data/wavelength_muestra.txt", "r") as f:
        wavelengths = [line.strip() for line in f]
    with open("./data/single_muestra.txt", "r") as f:
        absorbances = [line.strip() for line in f]
    # Assuming wavelengths and absorbances are lists
    wavelengths = np.array(wavelengths)
    absorbances = np.array(absorbances)

    # Create an array of new x values (i.e., 305, 306, 307, ...)
    new_wavelengths = np.arange(int(wavelengths[0]), int(wavelengths[-1]) + 1)

    # Interpolate the y values
    new_absorbances = np.interp(
        (new_wavelengths.astype(float)),
        (wavelengths.astype(float)),
        (absorbances.astype(float)),
    )

    for i in range(len(new_wavelengths)):
        write_data(
            "./data/interpolate_muestra.txt",
            str(new_wavelengths[i]),
            str(new_absorbances[i]),
        )

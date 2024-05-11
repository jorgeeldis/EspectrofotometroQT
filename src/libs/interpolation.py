import numpy as np


def interpolate(wavelengths, absorbances):
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

    return new_absorbances, new_wavelengths

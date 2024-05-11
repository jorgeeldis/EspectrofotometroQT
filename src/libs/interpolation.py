import os
import numpy as np

from libs.fileutil import write_data

SINGLE_FILE = os.getenv("SINGLE_FILE")
WAVELENGTH_FILE = os.getenv("WAVELENGTH_FILE")
INTERPOLATE_FILE = os.getenv("INTERPOLATE_FILE")

single_path = os.path.join("data", SINGLE_FILE)
wavelength_path = os.path.join("data", WAVELENGTH_FILE)
interpolate_path = os.path.join("data", INTERPOLATE_FILE)


def interpolate():

    if os.path.exists(interpolate_path):
        os.remove(interpolate_path)

    with open(wavelength_path, "r") as f:
        wavelengths = [line.strip() for line in f]
    with open(single_path, "r") as f:
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

        data = str(new_wavelengths[i]) + "," + str(new_absorbances[i]) + "\n"
        write_data(
            interpolate_path,
            data,
        )

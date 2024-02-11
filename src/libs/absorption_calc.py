import math


def absorption(baseline, single):
    calc = math.log10((baseline / single))
    return calc

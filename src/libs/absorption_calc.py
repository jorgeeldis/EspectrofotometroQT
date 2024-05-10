import math


def absorption(baseline, single):
    calc = math.log10((baseline / single))*1.41
    return calc

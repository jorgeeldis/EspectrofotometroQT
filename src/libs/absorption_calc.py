import math


def absorption(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 1.060251*to-0.133634
    calc = math.log10(1/t)
    return calc

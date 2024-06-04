import math


def absorption(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 1.060251*to-0.133634
    calc = -math.log10(t)
    return calc

#absorption 305 - 453
def absorption440(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 0.9856*to-0.0795
    calc = -math.log10(t)
    return calc

#absorption 454 - 506
def absorption465(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 0.9791*to-0.1171
    calc = -math.log10(t)
    return calc

#absorption 507 - 568
def absorption546(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 1.0005*to-0.1033
    calc = -math.log10(t)
    return calc

#absorption 569 - 613
def absorption590(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 1.0316*to-0.1101
    calc = -math.log10(t)
    return calc

#absorption 613 - 748
def absorption635(baseline, single):
    a = math.log10((baseline / single))
    to = single/baseline
    t = 1.3452*to-0.4025
    calc = -math.log10(t)
    return calc

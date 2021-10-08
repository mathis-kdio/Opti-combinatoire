
def glouton(convives):
    s = 0
    while convives != []:
        i = convives[0][1] * len(convives[0][2])
        if i > s:
            s = i
        convives.pop(0)
    return s
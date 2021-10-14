from glouton import *

def initPop(convives, taillePop):
  population = []

  res = glouton(convives, False)
  print("res: " + str(res))
  population.append(res)

  for i in range(0, taillePop - 1):
    res = glouton(convives, True)
    print("res: " + str(res))
    population.append(res)

  return population

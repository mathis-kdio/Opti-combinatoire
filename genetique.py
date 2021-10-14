from glouton import *

def initPop(convives, taillePop):
  res = glouton(convives, False)
  print("res: " + str(res))

  for i in range(0, taillePop):
    res = glouton(convives, True)
    print("res: " + str(res))

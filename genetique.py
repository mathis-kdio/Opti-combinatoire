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

def croisement(population, p_croisement):
  populationEnfants = []
  for i in range(0, len(population), 2):
    rand = random.uniform(0, 1)
    if rand < p_croisement: #croisement
      if len(population[i] > len(population[i+1])):
        K = random.randrange(1, len(population[i+1]))
      else:
        K = random.randrange(1, len(population[i]))
        populationEnfants.append([population[i][i:j] for i, j in zip([0]+K, K+[None])])
        print("test")
    else: #recopier
      print("recopier")
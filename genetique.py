from random import randrange
from glouton import *

def initPop(convives, taillePop):
  population = []

  res = glouton(convives, False)  
  population.append(res)

  for i in range(0, taillePop - 1):
    res = glouton(convives, True)
    population.append(res)

  return population

def croisement(population, p_croisement):
  populationEnfants = []
  for i in range(0, len(population), 2):
    rand = random.uniform(0, 1)
    if rand < p_croisement: #croisement
      lenPop1 = len(population[i])
      lenPop2 = len(population[i+1])
      if lenPop1 > lenPop2:
        K = random.randrange(1, lenPop2)
      else:
        K = random.randrange(1, lenPop1)

      populationEnfants.append(population[i][0:K] + population[i + 1][K:lenPop2])
      populationEnfants.append(population[i + 1][0:K] + population[i][K:lenPop1])

    else: #recopier
      populationEnfants.append(population[i])
      populationEnfants.append(population[i+1])

  return populationEnfants

def selection(convives, population, taille):
  reproduction = []
  score = 0
  listScore = []
  somme = 0
  borneInf = 0
  borneSup = 0

  # On calcule le score de tout le monde qu'on stocke, on calcule la somme on determine les bornes du rand
  for i in range(0, len(population)):
    for j in range(0, len(population[i])):
      score += convives[population[i][j]][1]

    somme += score
    listScore.append(score)
    if score < borneInf or i == 0:
      borneInf = score
    if score > borneSup:
      borneSup = score
    score = 0

  for i in range(0, len(listScore)):
    randProba = randrange(borneInf, borneSup)/somme
    proba = listScore[i]/somme
    if proba > randProba and len(reproduction) < taille:
      reproduction.append(population[i])

  if len(reproduction)%2 != 0:
    reproduction.pop(-1)

  return reproduction


def mutation(population, numerateur):
  rand = 0
  newValeur = 0
  probaMute = 0
  for i in range(0, len(population)):
    for j in range(0, len(population[i])):
      rand = random.uniform(0, 1)
      probaMute = numerateur/len(population[i])
      if rand < probaMute:
        newValeur = randrange(0, len(population))
        population[i][j] = newValeur

  return population


def survie(convives, population, taille):
  listTmp = []
  score = 0

  for i in range(0, len(population)):
    for j in range(0, len(population[i])):
      score += convives[population[i][j]][1]
    
    listTmp.append([score, population[i]])
    score = 0
  
  listTmp.sort(reverse=True)
  population.clear()
  for i in range(0, taille):
    population.append(listTmp[i])

  return population



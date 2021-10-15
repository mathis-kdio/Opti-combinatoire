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

  randProba = randrange(borneInf, borneSup)/somme

  for i in range(0, len(listScore)):
    proba = listScore[i]/somme
    if proba > randProba and len(reproduction) < taille:
      reproduction.append(population[i])

  return reproduction



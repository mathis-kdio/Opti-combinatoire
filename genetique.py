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

def reparation(convives, populations):
  print("DEBUT réparation")
  print(populations)

  scoresWithConvives = []
  scores = []
  score = 0
  for population in populations:
    acceptable = False
    while acceptable == False:
      #Calcul des scores
      for invite in population:
        score = 0
        for autresInvites in population:
          if invite != autresInvites and invite not in convives[autresInvites][2]:
            score += 1
        scoresWithConvives.append([score, invite])
        scores.append(score)
      
      #Test si solution possible
      if all(ele[0] == 0 for ele in scoresWithConvives):
        acceptable = True
        break

      #On enlève aléatoirement des convives avec un score non nu en fct du score
      scoresWithConvives.sort(reverse=True)
      scores.sort(reverse=True)
      population.remove(scoresWithConvives[random.randrange(0, scores.count(scores[0]))][1])
      scores.clear()
      scoresWithConvives.clear()

      #On ajoute des convives à la manière d’un glouton
      convivesCopy = convives.copy()
      convivesCopy.sort(reverse=True)
      popval = []
      for i in range(0, len(population)):
        popval.append([convives[population[i]][1], convives[population[i]][0]])

      popval.sort(reverse=True)

      theOne = popval[0][1]
      listVoisin = []
      listVoisin.append(list(convives[theOne][2]))
      for i in range(0, len(population)):
        if population[i] != theOne:
          listVoisin.append(list(convives[population[i]][2]))
      
      connaissancesH = []
      for i in range(0, len(convives[theOne][2])):
        h = convives[listVoisin[0][i]][1] * len(convives[listVoisin[0][i]][2])
        connaissancesH.append([h, listVoisin[0][i]])

      connaissancesH.sort(reverse=True)
      nbVoisins = len(listVoisin)
      for i in range(0, nbVoisins):
        apparition = 0
        for j in range(0, nbVoisins):
          if listVoisin[i][0] in listVoisin[j]:
            apparition += 1
        if apparition == nbVoisins and listVoisin[i][0] not in population:
          population.append(listVoisin[i][0])
          break

      #print("Calcul des nouveaux scores après ajout")

    #print(population)
    #print("pop suivante")
  print("FIN réparation")
  print(populations)

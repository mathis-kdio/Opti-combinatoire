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
    if (borneSup != borneInf):
      randProba = randrange(borneInf, borneSup)/somme
    else:
      randProba = randrange(borneInf-5, borneSup+5)/somme
    proba = listScore[i]/somme
    if proba > randProba and len(reproduction) < taille:
      reproduction.append(population[i])

  if len(reproduction)%2 != 0:
    reproduction.pop(-1)

  return reproduction


def mutation(population, numerateur, convives):
  rand = 0
  newValeur = 0
  probaMute = 0
  for i in range(0, len(population)):
    for j in range(0, len(population[i])):
      rand = random.uniform(0, 1)
      probaMute = numerateur/len(population[i])
      if rand < probaMute:
        #Test si la valeur random n'est pas déjà dans la population afin d'éviter les doublons
        newValeurOK = False
        while newValeurOK != True:
          newValeur = randrange(0, len(convives))
          if newValeur not in population[i]:
            newValeurOK = True
        population[i][j] = newValeur

  return population

def reparation(convives, populations):
  scoresWithConvives = []
  scores = []
  for population in populations:
    #Calcul des scores
    (scoresWithConvives, scores) = calculScore(population, convives)

    #On enlève aléatoirement des convives avec un score non nu en fct du score jusqu'à une solution réalisable
    while all(ele[0] == 0 for ele in scoresWithConvives) == False:
      scoresWithConvives.sort(reverse=True)
      scores.sort(reverse=True)
      population.remove(scoresWithConvives[random.randrange(0, scores.count(scores[0]))][1])
      (scoresWithConvives, scores) = calculScore(population, convives)

    #Une fois la solution réalisable (Les convives dans la pop se connaissent tous)
    #On ajoute des convives à la manière d’un glouton
    popval = []
    for i in range(0, len(population)):
      popval.append([convives[population[i]][1], convives[population[i]][0]])

    popval.sort(reverse=True)

    listeConnaissancesPop = []
    for i in range(0, len(popval)):
      listeConnaissancesPop.append(list(convives[popval[i][1]][2]))
    
    #On regarde toutes les connaissances du convive dans la population avec le meilleur interet
    connaissancesH = []
    for i in range(0, len(listeConnaissancesPop[0])):
      connaissanceBestConvivePop = listeConnaissancesPop[0][i]
      h = convives[connaissanceBestConvivePop][1] * len(convives[connaissanceBestConvivePop][2])
      connaissancesH.append([h, connaissanceBestConvivePop])
    
    #On trie les connaissances selon leur interet
    connaissancesH.sort(reverse=True)
    for i in range(0, len(connaissancesH)):
      connaissance = connaissancesH[i][1]
      if connaissance not in population:
        ajout = True
        for j in range(0, len(listeConnaissancesPop)):
          if connaissance not in listeConnaissancesPop[j]:
            ajout = False
            break
        if ajout == True:
          listeConnaissancesPop.append(list(convives[connaissance][2]))
          population.append(connaissance)

  return populations

def calculScore(population, convives):
  scoresWithConvives = []
  scores = []
  for invite in population:
    score = 0
    for autresInvites in population:
      if invite != autresInvites and invite not in convives[autresInvites][2]:
        score += 1
    scoresWithConvives.append([score, invite])
    scores.append(score)
    
  return (scoresWithConvives, scores)

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
    population.append(listTmp[i][1])

  return population[:]

def calculBest(invite, convives):
  score = 0
  for i in invite:
    score += convives[i][1]
  return score


def genetique(convives, pc, pm, taillePop, tailleS, iterMax):
  best = 0
  tmpBest = 0
  solution = []

  population = initPop(convives, taillePop)
  best = calculBest(population[0], convives)
  print(best)

  for k in range(0, iterMax):
    for i in range(0, len(population)):
      solution.append(population[i][:])
    population = selection(convives, population, tailleS)
    print("avant croisement")
    population = croisement(population, pc)
    print("avant mutation")
    population = mutation(population, pm, convives)
    print("avant réparation")
    population = reparation(convives, population)
    #for i in range(0, len(population)):
      #solution.append(population[i][:])
    population = survie(convives, solution, taillePop)
    solution.clear()
    for i in range(0, len(population)):
      population[i] = list(set(population[i]))
      solution.append(population[i][:])

    tmpBest = calculBest(solution[0], convives)
    if tmpBest > best:
      best = tmpBest
    print("Best is "+ str(best)+" au bout de l'itération "+ str(k) +" avec la solution " +str(solution[0]))

  return best


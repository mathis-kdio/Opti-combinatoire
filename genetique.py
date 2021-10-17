from random import randrange
from glouton import *
import time

def initPop(convives, taillePop):
  population = []

  res = glouton(convives, False)  
  population.append(res)

  for i in range(taillePop - 1):
    res = glouton(convives, True)
    population.append(res)

  return population

def selection(convives, populations, taille):
  reproduction = []
  score = 0
  listScore = []
  somme = 0
  borneInf = 0
  borneSup = 0

  # On calcule le score de tout le monde qu'on stocke, on calcule la somme on determine les bornes du rand
  i = 0
  for population in populations:
    for invite in population:
      score += convives[invite][1]

    listScore.append(score)
    if score < borneInf or i == 0:
      borneInf = score
    if score > borneSup:
      borneSup = score
    somme += score
    score = 0
    i+=1

  for i in range(0, len(listScore)):
    if (borneSup != borneInf):
      randProba = randrange(borneInf, borneSup)/somme
    else:
      randProba = randrange(borneInf-5, borneSup+5)/somme
    
    proba = listScore[i]/somme
    if proba > randProba and len(reproduction) < taille:
      reproduction.append(populations[i])

  if len(reproduction)%2 != 0:
    reproduction.pop(-1)

  return reproduction

def croisement(population, p_croisement):
  populationEnfants = []
  for i in range(0, len(population), 2):
    rand = random.uniform(0, 1)
    if rand < p_croisement: #croisement
      lenPop1 = len(population[i])
      lenPop2 = len(population[i+1])
      maxRand = lenPop1
      if lenPop1 > lenPop2:
        maxRand = lenPop2

      k = randrange(1, maxRand)
      croisement1 = population[i][0:k] + population[i + 1][k:lenPop2]
      croisement2 = population[i + 1][0:k] + population[i][k:lenPop1]
      #On supprime si doublons générés par les croisement
      populationEnfants.append(list(set(croisement1)))
      populationEnfants.append(list(set(croisement2)))
    else: #recopier
      populationEnfants.append(population[i])
      populationEnfants.append(population[i+1])

  return populationEnfants

def mutation(populations, numerateur, convives):
  rand = 0
  newValeur = 0
  probaMute = 0
  for population in populations:
    for i in range(len(population)):
      rand = random.uniform(0, 1)
      probaMute = numerateur/len(population)
      if rand < probaMute:
        #Test si la valeur random n'est pas déjà dans la population afin d'éviter les doublons
        newValeurOK = False
        while newValeurOK != True:
          newValeur = randrange(0, len(convives))
          if newValeur not in population:
            newValeurOK = True
        population[i] = newValeur

  return populations

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
      population.remove(scoresWithConvives[randrange(0, scores.count(scores[0]))][1])
      (scoresWithConvives, scores) = calculScore(population, convives)

    #Une fois la solution réalisable (Les convives dans la pop se connaissent tous)
    #On ajoute des convives à la manière d’un glouton
    
    popval = []
    for invite in population:
      popval.append([convives[invite][1], invite, convives[invite][2]])

    popval.sort(reverse=True) #Liste des invites triés selon leur intéret avec l'intéret et [0] et numero en [1] et connaissance en [2]

    listeConnaissancesPop = []
    for invite in popval:
      listeConnaissancesPop.append(invite[2])
    
    #On calcul l'heuristique de toutes les connaissances du convive dans la population avec le meilleur interet
    connaissancesH = []
    for connaissanceBestConvivePop in listeConnaissancesPop[0]:
      h = convives[connaissanceBestConvivePop][1] * len(convives[connaissanceBestConvivePop][2])
      connaissancesH.append([h, connaissanceBestConvivePop])
    
    #On trie les connaissances selon leur interet
    connaissancesH.sort(reverse=True)
    for connaissanceH in connaissancesH:
      connaissance = connaissanceH[1]
      if connaissance not in population:
        ajout = True
        for connaissancePop in listeConnaissancesPop:
          if connaissance not in connaissancePop:
            ajout = False
            break
        if ajout:
          listeConnaissancesPop.append(convives[connaissance][2])
          population.append(connaissance)

  return populations

def calculScore(population, convives):
  scoresWithConvives = []
  scores = []
  for invite in population:
    score = 0
    for autresInvites in population:
      #test si un invite ne connait pas les autres invites, dans ce cas +1
      if invite != autresInvites and invite not in convives[autresInvites][2]:
        score += 1
    scoresWithConvives.append([score, invite])
    scores.append(score)
    
  return (scoresWithConvives, scores)

def survie(convives, populations, taille):
  listTmp = []
  score = 0
  for population in populations:
    for invite in population:
      score += convives[invite][1]
    
    listTmp.append([score, population])
    score = 0
  
  listTmp.sort(reverse=True)
  populations.clear()
  for i in range(0, taille):
    populations.append(listTmp[i][1])

  return populations

def calculBest(invite, convives):
  score = 0
  for i in invite:
    score += convives[i][1]
  return score


def genetique(convives, pc, pm, taillePop, tailleS, iterMax, tempsMax):
  best = 0
  tmpBest = 0
  solution = []
  temps_passe = 0
  start = time.time()
  print('start', start)

  population = initPop(convives, taillePop)
  best = calculBest(population[0], convives)
  print(best)
  solution = population.copy()
  for k in range(0, iterMax):
    population = selection(convives, population, tailleS)
    population = croisement(population, pc)
    population = mutation(population, pm, convives)
    population = reparation(convives, population)
    solution.extend(population) #Ajout de la population à la solution
    solution = survie(convives, solution, taillePop)
    population = solution.copy() #La population est égale à la population
    tmpBest = calculBest(solution[0], convives)
    if tmpBest > best:
      best = tmpBest
    print("Best is "+ str(best)+" au bout de l'itération "+ str(k) +" avec la solution " + str(solution[0]))
    temps_passe = time.time() - start
    print('temps passé', temps_passe)

    if temps_passe > tempsMax:
      return best

  return (best, solution[0])


def tabu_search(convives, nb_iteration):
	solution = glouton(convives, False)
	tmp = calculBest(solution, convives)

	for i in range(0, nb_iteration):
		liste_finale = flip(solution[:], convives, nb_iteration)
		liste_finale_repare = reparation(convives, liste_finale)

		cpt = 0
		
		for j in liste_finale_repare:
			score = calculBest(j, convives)
			if score > tmp:
				tmp = score
				solution = liste_finale_repare[cpt]
			cpt += 1		

	return solution, calculBest(solution, convives)


def flip(solution_initial, convives, nb_iteration):
	liste_taboue = []
	liste_finale = []
	for i in range(nb_iteration):
		copy_solution_initial = solution_initial.copy()
		for j in range(3):
			indexConviveRetire = randrange(0, len(copy_solution_initial))
			conviveRetire = copy_solution_initial.pop(indexConviveRetire)
			liste_taboue.append(conviveRetire)

		for j in range(3):
			newConvive = randrange(0, len(convives))
			while newConvive in copy_solution_initial or newConvive in liste_taboue:
				newConvive = randrange(0, len(convives))
			copy_solution_initial.append(newConvive)

		liste_finale.append(copy_solution_initial)

	return liste_finale


def hybridation(convives, pc, pm, taillePop, tailleS, iterMax, tempsMax, nbIteration):
  
  solution = []
  score = 0

  population = initPop(convives, taillePop)
  best = calculBest(population[0], convives)
  solution = population.copy()

  for i in range(1, iterMax):
    cpt = 0
    population = selection(convives, population, tailleS)
    population = croisement(population, pc)
    population = mutation(population, pm, convives)
    population = reparation(convives, population)
    solution.extend(population) #Ajout de la population à la solution
    solution = survie(convives, solution, taillePop)
    population = solution.copy()
    for j in solution:
      score = calculBest(j, convives)
      if score > best:
        print("Score amélioré par le génétique à l'itération "+str(i))
        best = score
        bestSolution = solution[cpt][:]
        print(bestSolution, calculBest(bestSolution, convives))	
      cpt += 1	

    listTabu = flip(bestSolution, convives, nbIteration)
    listTabu = reparation(convives, listTabu)
    cpt = 0
		
    for j in listTabu:
      score = calculBest(j, convives)
      if score > best:
        print("Score amélioré par le tabou à l'itération "+str(i))
        best = score
        bestSolution = listTabu[cpt]
        population[0] = bestSolution[:]
        print(bestSolution, calculBest(bestSolution, convives))
      cpt += 1	

  return best
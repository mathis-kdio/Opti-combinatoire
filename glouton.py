import random

def glouton(convives, randomize):
    #Déclaration des variables
    heuristique = 0
    tmp = 0
    theOne = 0
    solution = []
    listVoisin = []
    connaissancesH = []

    if randomize == False:
        #On détermine la meilleure heuristique avec le critère de choix et on ajoute sa valeur ainsi que ses voisins
        for i in range(0, len(convives)):
            heuristique = convives[i][1] * len(convives[i][2])
            if heuristique > tmp:
                tmp = heuristique
                theOne = i

        solution.append(theOne)
        listVoisin.append(list(convives[theOne][2]))
    if randomize == True:
        theOne = random.randrange(0, len(convives))
        solution.append(theOne)
        listVoisin.append(list(convives[theOne][2]))

    #On trie le tableau des voisins en fonction de la meilleure heuristique
    for i in range (0, len(convives[theOne][2])):
        h = convives[listVoisin[0][i]][1] * len(convives[listVoisin[0][i]][2])
        connaissancesH.append([h, listVoisin[0][i]])
    
    connaissancesH.sort(reverse=True)
    for i in range(0, len(connaissancesH)):
        listVoisin[0][i] = connaissancesH[i][1]

    while listVoisin[0] != []:
        apparition = 0
        for j in range(0, len(listVoisin)):
            if listVoisin[0][0] in listVoisin[j]:
                apparition += 1 
        if apparition == len(listVoisin):
            listVoisin.append(list(convives[listVoisin[0][0]][2]))
            solution.append(listVoisin[0][0])
                            
        listVoisin[0].pop(0)

    return solution
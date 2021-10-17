import random

def glouton(convives, randomize):
    #Déclaration des variables
    heuristique = 0
    tmp = 0
    conviveChoisi = 0
    solution = []
    listConnaissance = []
    connaissancesH = []

    if randomize == False:
        #On détermine la meilleure heuristique avec le critère de choix et on ajoute sa valeur ainsi que ses voisins
        for i in range(0, len(convives)):
            heuristique = convives[i][1] * len(convives[i][2])
            if heuristique > tmp:
                tmp = heuristique
                conviveChoisi = i
    else:
        conviveChoisi = random.randrange(0, len(convives))
    solution.append(conviveChoisi)

    #On trie le tableau des voisins en fonction de la meilleure heuristique
    for connaissance in convives[conviveChoisi][2]:
        h = convives[connaissance][1] * len(convives[connaissance][2])
        connaissancesH.append([h, connaissance])
    
    connaissancesH.sort(reverse=True)

    listConnaissance = [[a[1] for a in connaissancesH]]

    while listConnaissance[0] != []:
        connaissance = listConnaissance[0][0]
        ajout = True
        for connaissances1Solution in listConnaissance:
            if connaissance not in connaissances1Solution:
                ajout = False
                break
        if ajout:
            listConnaissance.append(convives[connaissance][2])
            solution.append(connaissance)
                            
        listConnaissance[0].pop(0)

    return solution
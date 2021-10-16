import random


def glouton(convives, randomize):
    # Déclaration des variables
    heuristique = 0
    tmp = 0
    theOne = 0
    solution = []
    listConnaissance = []
    connaissancesH = []

    if randomize == False:
        # On détermine la meilleure heuristique avec le critère de choix et on ajoute sa valeur ainsi que ses voisins
        for i in range(0, len(convives)):
            heuristique = convives[i][1] * len(convives[i][2])
            if heuristique > tmp:
                tmp = heuristique
                theOne = i
        solution.append(theOne)
        listConnaissance.append(list(convives[theOne][2]))

    if randomize == True:
        theOne = random.randrange(0, len(convives))
        solution.append(theOne)
        listConnaissance.append(list(convives[theOne][2]))

    # On trie le tableau des voisins en fonction de la meilleure heuristique
    for i in range(0, len(convives[theOne][2])):
        h = convives[listConnaissance[0][i]][1] * len(convives[listConnaissance[0][i]][2])
        connaissancesH.append([h, listConnaissance[0][i]])

    connaissancesH.sort(reverse=True)
    for i in range(0, len(connaissancesH)):
        listConnaissance[0][i] = connaissancesH[i][1]

    while listConnaissance[0] != []:
        apparition = 0
        for j in range(0, len(listConnaissance)):
            if listConnaissance[0][0] in listConnaissance[j]:
                apparition += 1
        if apparition == len(listConnaissance):
            listConnaissance.append(list(convives[listConnaissance[0][0]][2]))
            solution.append(listConnaissance[0][0])

        listConnaissance[0].pop(0)

    return solution


def liste_taboue(convives, iteration):
    print("liste taboue")

    liste_voisin = []
    liste_heuristique = []
    heuristique = 0
    connard = 0

    for i in range(iteration):
        res_glouton = glouton(convives, True)
        liste_voisin.append(res_glouton)

    for j in liste_voisin:
        heuristique = 0
        for k in j:
            heuristique += convives[k][1]
        liste_heuristique.append(heuristique)

    print('liste heuristique', liste_heuristique)
    liste_heuristique.append(heuristique)
    index_liste_heur = liste_heuristique.index(max(liste_heuristique))

    print('liste max', liste_voisin[index_liste_heur])

    for l in liste_voisin[index_liste_heur]:
        connard += convives[l][1]

    print('connard', connard)

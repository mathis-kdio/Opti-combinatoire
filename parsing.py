import sys

def parsing(lignes):
    nm = lignes[0].split(" ")
    nbConvives = int(nm[0])
    m = int(nm[0])
    lignes.pop(0)
    print("nombre de convives potentiels: " + str(nbConvives))
    print("nombre de liens d’amitié: " + str(m))

    m = []
    for ligne in lignes:
        elements = ligne.split("\n")
        for element in elements:
            if (element != ""):
                m.append([int(x) for x in element.split(' ')])

    return nbConvives, m


def writeLp(convives, nbConvives, outputFile):
    result = []
    result.append("Maximize")
    
    objectif = "z:"
    for i in range(0, nbConvives):
        objectif += " " + str(convives[i][1]) + " x" + str(i) + " +"
    objectif = objectif[:len(objectif)-1]
    result.append(objectif)

    result.append("Subject To")

    k = 0
    for i in range(0, nbConvives):
        for j in range(i + 1, nbConvives):
            if j not in convives[i][2]:
                poids = "c" + str(k) + ":"
                poids += " x" + str(i) + " + x" + str(j) + " <= 1"
                k += 1
                result.append(poids)

    result.append("Binaries")

    for i in range(0, nbConvives):
        result.append("x" + str(i))

    result.append("End")

    try:
        fichierSortie = open(outputFile, "w")
    except:
        sys.exit("Impossible d'écrire dans le fichier")

    for mot in result:
        fichierSortie.write(str(mot) + "\n")
    fichierSortie.close()

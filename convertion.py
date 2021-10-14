import sys

from glouton import *

if __name__ == '__main__':
  
  print("Projet Optimisation Combinatoire")

  # Lecture du fichier d'instance
  try:
      fichier = open(sys.argv[1], "r")
  except:
      sys.exit("Impossible de lire le fichier")
  
  lignes = fichier.readlines()
  fichier.close()

  # Parsing
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

  # Fin parsing

  convives = []
  for i in range(0, nbConvives):
    convives.append(m[i])
    convives[i].append([])

  for j in range(nbConvives, len(m)):
    convives[m[j][0]][2].append(m[j][1])
    convives[m[j][1]][2].append(m[j][0])


  # Ecriture du résultat dans le fichier lp
  result = []
  result.append("Maximize")
  
  objectif = "z:"
  for i in range(1, nbConvives + 1):
    objectif += " " + str(convives[i - 1][1]) + " x" + str(i) + " +"
  objectif = objectif[:len(objectif)-1]
  result.append(objectif)

  result.append("Subject To")

  for i in range(0, nbConvives):
    poids = "c" + str(i + 1) + ":"
    for j in range(0, len(convives[i][2])):
      connaissance = convives[i][2][j]
      poids += " " +  str(convives[connaissance][1]) + " x" + str(connaissance + 1) + " +"
    poids = poids[:len(poids)-1]
    poids += "<= " + str(len(convives[i][2]))
    result.append(poids)

  result.append("Binaries")

  for i in range(1, nbConvives + 1):
    result.append("x" + str(i))

  result.append("End")

  try:
      fichierSortie = open(sys.argv[2], "w")
  except:
      sys.exit("Impossible d'écrire dans le fichier")

  for mot in result:
      fichierSortie.write(str(mot) + "\n")
  fichierSortie.close()

  
  res = glouton(convives)
  print("res: " + str(res))
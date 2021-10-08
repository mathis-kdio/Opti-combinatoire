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

  res = glouton(convives)
  print("res: " + str(res))

  # Ecriture du résultat dans le fichier lp
  result = []
  result.append("Maximize")
  
  objectif = "z:"
  for i in range(1, nbConvives):
    objectif += " " + str(m[i - 1][0]) + " x" + str(i) + " +"
  objectif = objectif[:len(objectif)-1]
  result.append(objectif)

  result.append("Subject To")

  poids = "poids:"
  for i in range(1, nbConvives):
    poids += " " + str(m[i - 1][1]) + " x" + str(i) + " +"
  poids = poids[:len(poids)-1]
  poids += "<= 10"
  result.append(poids)

  result.append("Binaries")

  for i in range(1, nbConvives):
    result.append("x" + str(i))

  result.append("End")

  try:
      fichierSortie = open(sys.argv[2], "w")
  except:
      sys.exit("Impossible d'écrire dans le fichier")

  for mot in result:
      fichierSortie.write(str(mot) + "\n")
  fichierSortie.close()
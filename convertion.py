import sys

from genetique import *

if __name__ == '__main__':

  Tab_result_GLPK = [73, 91, 84, 83, 81, 80, 81, 85, 77, 91]
  argu = sys.argv[1]
  sans_instance = argu.split("instance")
  sans_txt = sans_instance[1].split(".txt")
  instance_num = sans_txt[0]

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
      fichierSortie = open(sys.argv[2], "w")
  except:
      sys.exit("Impossible d'écrire dans le fichier")

  for mot in result:
      fichierSortie.write(str(mot) + "\n")
  fichierSortie.close()

  solution = []
  taillePop = 400
  tailleS = 100
  pc = 0.8
  pm = 2
  iterMax = 500

  best = genetique(convives, pc, pm, taillePop, tailleS, iterMax)  
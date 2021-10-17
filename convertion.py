import sys

from genetique import *
from parsing import parsing, writeLp

if __name__ == '__main__':

  argu = sys.argv[1]
  if argu.split("instance"):
    tab_result_GLPK = [73, 91, 84, 83, 81, 80, 81, 85, 77, 91]
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
  nbConvives, m = parsing(lignes)

  convives = []
  for i in range(0, nbConvives):
    convives.append(m[i])
    convives[i].append([])

  for j in range(nbConvives, len(m)):
    convives[m[j][0]][2].append(m[j][1])
    convives[m[j][1]][2].append(m[j][0])

  # Ecriture du résultat dans le fichier lp
  if argu.split("instance"):
    writeLp(convives, nbConvives)


  # Algo génétique
  solution = []
  taillePop = 400
  tailleS = 100
  pc = 0.8
  pm = 2
  iterMax = 500

  best = genetique(convives, pc, pm, taillePop, tailleS, iterMax)  

  solution_taboue = liste_taboue(convives, 1000)

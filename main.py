import sys

from genetique import *
from parsing import parsing

if __name__ == '__main__':
  print("Projet Optimisation Combinatoire")

  # Lecture du fichier d'instance
  inputFile = sys.argv[2]
  try:
    fichier = open(inputFile, "r")
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

  #Ecriture dans le fichier .lp
  #ouputLPFile = sys.argv[3]
  #writeLp(convives, nbConvives, ouputLPFile)

  # Algo génétique
  solution = []
  taillePop = 400
  tailleS = 100
  pc = 0.8
  pm = 2
  iterMax = 500
  tempsMax = int(sys.argv[1])
  (interet, solution) = genetique(convives, pc, pm, taillePop, tailleS, iterMax, tempsMax)

  outputFile = sys.argv[3]
  try:
    fichierSortie = open(outputFile, "w")
  except:
    sys.exit("Impossible d'écrire dans le fichier")
  fichierSortie.write("Interet maximum trouve : " + str(interet) + " avec les " + str(len(solution)) + " invites suivants : " + str(solution) + "\n")
  fichierSortie.close()

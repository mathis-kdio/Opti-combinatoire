import sys

from genetique import *
from parsing import parsing

if __name__ == '__main__':
  print("Début programme Projet Optimisation Combinatoire")
  start = time.time()

  if len(sys.argv) < 5:
    print("vous avez oubliez de préciser un argument")
    print("        p : pour une petite instance")
    print("        g : pour une grande instance")
    sys.exit()


  input_algo = sys.argv[4]
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

  '''res_tabu = tabu_search(convives, 100)
  print("res_tabu ", res_tabu)'''

  if input_algo == 'p':
    print('Début algorithme hybridation')
    (interet, solution) = hybridation(convives, pc, pm, taillePop, tailleS, iterMax, tempsMax - 5, start, 100)
    print('Fin algorithme hybridation')
  if input_algo == 'g':
    print('Début algorithme genetique')
    (interet, solution) = genetique(convives, pc, pm, taillePop, tailleS, iterMax, tempsMax - 5, start)
    print('Fin algorithme genetique')



  outputFile = sys.argv[3]
  try:
    fichierSortie = open(outputFile, "w")
  except:
    sys.exit("Impossible d'écrire dans le fichier")
  fichierSortie.write("Interet maximum trouve : " + str(interet) + " avec les " + str(len(solution)) + " invites suivants : " + str(solution) + "\n")
  fichierSortie.close()

  print("Fin programme Projet Optimisation Combinatoire")
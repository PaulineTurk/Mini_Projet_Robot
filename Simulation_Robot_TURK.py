#!/bin/env python         
# -*- coding: utf-8 -*-  

import POO_Robot_TURK
import random
import matplotlib.pyplot as plt


def affichage_grille(liste_robots, taille_x, taille_y, noms, avancement):        
    """
    Affiche sur une grille de taille <taille_x> x <taille_y>,
    les robots dont les coordonnees sont dans la liste <positions_occupees>
    """
    positions_occupeesX = []
    positions_occupeesY = []

    for robot in liste_robots:                 # liste_robots et noms gardent l'ordre de creation des robots
        positions_occupeesX.append(robot.px)   # pour récupérer les bonnes abscisses des robots (dans le bon ordre)
        positions_occupeesY.append(robot.py)   # pour récupérer les bonnes ordonnées des robots (dans le bon ordre)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1)) # pour avoir intervalle de 1 dans la grille
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
    titre = "Simulation Robots : {} %".format(avancement)
    plt.title(titre)
    plt.axis([0, taille_x, 0, taille_y])
    plt.scatter(positions_occupeesX, positions_occupeesY)
    for i, txt in enumerate(noms):                  # récupérer les tuples (indices, nom_du_robot)
        plt.annotate(txt, (positions_occupeesX[i], positions_occupeesY[i]))   # annoter chaque point représentant un robot par son nom
    plt.grid(True)      
    plt.show(block=False)  # pour ne pas bloquer la suite du script 
    plt.pause(0.01)        
    plt.clf()              # pour ne pas refermer la fenetre d'affichage 
  


def creation_robots(nbre_robots, grille_x, grille_y):
    '''
    Cree et positionne aléatoirement nbre_robots robots dont la nature est choisie aleatoirement,
    vivant sur une grille de taille <grille_x> x <grille_y>.

    --> Renvoie:
    - liste_robots : la liste de robots créés
    - positions_libres : la liste des cases de la grille non occupees par des robots
    - positions_occupees : la liste des cases de la grille occupees par des robots
    - etiquettes : la liste des noms des robots crees
    '''
    print("Initialisation des {} robots :".format(nbre_robots))
    nbre_robots_ancien = random.randint(0, nbre_robots)
    liste_robots = []         # contiendra les robots créés dans l'ordre de leur création
    etiquettes = []           # contiendra les noms des robots dans l'odre de leur creation
    positions_occupees = []   # contiendra les positions de chaque robot dans l'ordre de leur creation
    positions_libres = []     # contiendra les positions non occupées par des robots

    for i in range(grille_x + 1):   # positions_libres avant l'ajout de robots
        for j in range(grille_y + 1):
            positions_libres.append([i, j])     

    for i in range(nbre_robots) :
        if i < nbre_robots_ancien :
            nom_robot = "A{}".format(i + 1)
            liste_robots.append(POO_Robot_TURK.Robot(nom_robot))    # création d'un robot de 1ère génération
        else:
            nom_robot = "N{}".format(i-nbre_robots_ancien + 1)
            liste_robots.append(POO_Robot_TURK.RobotNG(nom_robot))  # création d'un robot nouvelle génération

        etiquettes.append(liste_robots[i].nom)
        position_robot = random.choice(positions_libres)            # initialisation aléatoire de la position du robot sur la grille
        liste_robots[i].px, liste_robots[i].py = position_robot[0], position_robot[1]
        print(liste_robots[i].nom)

        positions_libres.remove(position_robot)                # position_robot devient occupée
        positions_occupees.append(position_robot)     

    # Ajout des robots sur la grille
    affichage_grille(liste_robots, grille_x, grille_y, etiquettes, 0)

    return (liste_robots, positions_libres, positions_occupees, etiquettes)



def choix_move_Ancien(robot):
    """
    Choisit aleatoirement un déplacement/changement de direction pour un robot de 1ère génération.
    """
    choix_aleatoire = random.randint(1, 2)         
    if choix_aleatoire == 1:
        robot.avance()   
    else:
        robot.droite()



def choix_move_NG(robot, nbre_pas_max):
    """
    Choisit aleatoirement un déplacement/changement de direction pour un robot de la Nouvelle generation.
    """
    choix_aleatoire = random.randint(1, 4)        
    if choix_aleatoire == 1:
        nbre_pas = random.randint(1, nbre_pas_max)
        robot.avance(nbre_pas)
    elif choix_aleatoire == 2:
        robot.droite()
    elif choix_aleatoire == 3:
        robot.gauche()
    else:
        robot.demiTour()
   


def legalite_move(robot, px_courant, py_courant,  grille_x, grille_y, positions_occupees, positions_libres):
    """
    Verifie si le mouvement choisi aleatoirement par le robot est possible i.e le robot sur la grille et la case n'est pas deja occupee par un autre robot.
    Si c'est le cas, les coordonnées du robots sont modifiees comme envisage et les listes positions_occupees, positions_libres sont mises à jour.
    Sinon, les coordonnées du robot restent inchangées et donc les listes positions_occupees, positions_libres aussi.
    """
    px_objectif, py_objectif =  robot.px, robot.py   # coordonnées prises par le robot si le mouvement qu'il a choisi est possible.

    if (0 <= px_objectif <= grille_x) and (0 <= py_objectif <= grille_y) and ([px_objectif, py_objectif]) not in positions_occupees: # si la case d'arrivée est dans la grille et est non occupée, alors le mouvement est possible
        positions_occupees.remove([px_courant, py_courant])                    # la case quittée par le robot devient libre
        positions_libres.append([px_courant, py_courant])
        positions_libres.remove([px_objectif, py_objectif])                    # la nouvelle case qu'il occupe devient occupée
        positions_occupees.append([px_objectif, py_objectif])
    else:                                                                                                                            
        robot.px, robot.py = px_courant, py_courant                                                                                  # sinon, le mouvement n'est pas possible, alors le robot garde ses coordonnées de départ d'itération




def vie_robot(liste_robots, positions_libres, positions_occupees, nbre_iteration,  grille_x, grille_y, etiquettes):
    """
    Simule la vie des robots sur la grille en nbre_iteration iterations.
    A chaque iteration, chaque robot a la possibilite de bouger/changer de direction une fois et ce sequentiellement dans l'ordre de leur creation.

    --> Renvoie:
    - liste_coord : la liste dont l'element i est la liste des positions prises par chaque robot (dans l'ordre de leur creation) a la ième iteration de la simulation.
    """
    nbre_robots = len(liste_robots)
    nbre_tour = 0
    positions_initiales = positions_occupees.copy()    # je ne sais pas pourquoi le .copy() a été nécessaire sinon <positions_initiales> était mise à jour avec les modifications de <positions_occupees>
    liste_coord = [positions_initiales]                # initialisation de la liste contenant les positions occupées par chaque robot au cours de la simulation avec la liste des positions initialement occupées par chaque robot dans l'odre de leur création
    # print("Position de chaque robot à l'initialisation {}".format(liste_coord))

    while nbre_tour < nbre_iteration :
        numero_iteration = nbre_tour + 1            # ajouter 1 à nbre_tour pour pouvoir afficher le numéro de l'itération
        print("Simulation à l'itération n°{}\n".format(numero_iteration))
        compte_robot = 0
        liste_coord_iteration = []                     # initialisation de la liste contenant les positions occupées par chaque robot dans l'ordre de leur création pour une itération

        for compte_robot in range(nbre_robots):
            robot_courant = liste_robots[compte_robot]                              # chaque robot aura l'opportunité de se déplacer/changer de direction à chaque itération
            x_courant, y_courant = robot_courant.px, robot_courant.py               # coordonnées du robot avant son potentiel déplacement
            print("Départ {}: ({}, {})".format(robot_courant.nom, x_courant, y_courant))                   # affichage de la position du robot avant l'itération en cours

            if isinstance(robot_courant, POO_Robot_TURK.RobotNG) == False:          # On considère tous les robots de 1ère génération qui ont été créés en premier
                choix_move_Ancien(robot_courant)                                    # le robot choisit une option de déplacement propre à la classe Robot
                legalite_move(robot_courant, x_courant, y_courant, grille_x, grille_y, positions_occupees, positions_libres)   # vérification de la faisabilité du mouvement --> déplacement effectif en cas de mouvement possible
                print("Arrivée {} : ({}, {})\n".format(robot_courant.nom, robot_courant.px, robot_courant.py))                             # affiche la position du robot à la fin de l'itération en cours
                avancement = round(100*((nbre_tour)*(nbre_robots) + (compte_robot))/((nbre_iteration)*(nbre_robots)))          # affiche le taux d'avancement de la simulation
                affichage_grille(liste_robots, grille_x, grille_y, etiquettes, avancement)                                     # afficher la grille à ce taux d'avancement de la simulation    
            
            else:                                                                  # Il reste les robots de Nouvelle Génération
                nbre_pas_max = max(grille_x,grille_y)         # nbre_pas_max est pris au max entre grille_x et grille_y pour rendre tous les déplacements possibles, quelque soient les dimensions de la grille
                choix_move_NG(robot_courant, nbre_pas_max)    # le robot choisit une option de déplacement propre à la classe RobotNG                         
                legalite_move(robot_courant, x_courant, y_courant,  grille_x, grille_y, positions_occupees, positions_libres)   # vérification de la faisabilité du mouvement --> déplacement effectif en cas de mouvement possible
                print("Arrivée {} : ({}, {})\n".format(robot_courant.nom, robot_courant.px, robot_courant.py))                            # affiche la position du robot à la fin de l'itération en cours
                avancement = round(100*((nbre_tour)*(nbre_robots) + (compte_robot))/((nbre_iteration)*(nbre_robots)))           # affiche le taux d'avancement de la simulation
                affichage_grille(liste_robots, grille_x, grille_y, etiquettes, avancement)                                      # afficher la grille à ce taux d'avancement de la simulation

            liste_coord_iteration.append([robot_courant.px, robot_courant.py])           # ajout de la position du robot d'indice <compte_robot> à l'itération <nbre_tour>
            # print(liste_coord_iteration)
        
        liste_coord.append(liste_coord_iteration)                                        # ajout de la liste des coordonnées de tous les robots à l'itération <nbre_tour>
        # print("Liste des positions de tous les robots, historique en cours : \n",liste_coord)
        nbre_tour += 1

    print("Liste des positions de tous les robots pour chaque itération de la simulation : \n",liste_coord)
    return liste_coord



def recuperation_coord_robot(liste_coord, liste_robots):
    """
    Entrees:
    - liste_coord : la liste dont l'element i est la liste des positions prises par chaque robot (dans l'ordre de leur creation) a la ième iteration de la simulation.
    - liste_robots : la liste des robots crees.

    --> Renvoie:
    - liste_cases_visitees : la liste du nombre de cases différentes visitees par chaque robot (dans l'ordre de leur création)
    """
    liste_cases_visitees = []          # initialisation de la liste contienant le nombre de cases différentes visitées par chaque robot pendant la simulation (dans l'ordre de creation des robots)
    nbre_robot = len(liste_robots)
    nbre_iteration = len(liste_coord)   # nbre_iteration est le nombre d'itérations de la simulation + 1 (pour la position initiale)
    
    for compte_robot in range(nbre_robot):    
        liste_coord_robot = []                      # Pour chaque robot, initialisation de la liste contenant les coordonnées de toutes les cases que ce robot a visité
        for iteration in range(nbre_iteration):     
            liste_coord_robot.append(liste_coord[iteration][compte_robot])     # pour chaque itération dans la simulation, on récupère la coordonnées de la case occupée par le robot sélectionné

        liste_cases_visitees.append(liste_robots[compte_robot].surface_couverte(liste_coord_robot)) # Pour chaque robot, on ajoute le nombre de cases différentes visitées lors de la simulation (dans l'odre de leur création)

    return liste_cases_visitees



def histogramme(liste_robots,liste_cases_visitees):
    """
    Entrees:
    - liste_robots : la liste des robots
    - liste_cases_visitees : la liste des cases visitees par chaque robot lors de la simulation
    Affiche l'histogramme donnant le nombre de cases différentes visitees par chaque robot (represente par leur nom) lors de la simulation.
    """
    nbre_robot = len(liste_robots)
    position_histo_robot = list(range(nbre_robot))              # pour positionner les barres de l'histogramme
    liste_nom_robot = []
    for robot in liste_robots:
        liste_nom_robot.append(robot.nom)                       # récupération du noms des robots pour l'affichage
    plt.xticks(position_histo_robot, liste_nom_robot)
    plt.bar(position_histo_robot , liste_cases_visitees)        # affiche le nombre de cases différentes visitées par chaque robot lors de la simulation
    plt.xlabel('Nom de robot')
    plt.ylabel('Nombre de cases différentes')
    plt.title("Cases visitées lors de la simulation")
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
    plt.show()






"""
Programme principal de simulation
"""

# Conseils d'ordre de grandeur de bons tests illustratifs : 
# - taille grille: 20*20, avec 2 robots et 3 itérations  # pour un petit exemple pour comprendre la simulation (mais il est assez probable qu'aucun robot ne bouge sur un si petit exemple)
# - taille grille: 50*50, avec 10 robots et 5 itérations  # pour un plus grand exemple qui ne prenne pas trop de temps

print("")
print("Simluation vie Robots".center(100, "-"))  

# Choix des dimensions de la grille de simulation par l'utilisateur --> creation de cette grille
grille_x = int(input("Donnez une largeur à la grille de simulation (un entier positif) :"))
grille_y = int(input("Donnez une longueur à la grille de simulation (un entier positif) :"))

# Choix du nombre de robots par l'utilisateur --> creation de ces robots dont une partie est de première génération et le reste est NG + placement aléatoire de ces robots sur la grille.
nbre_de_robots = int(input("Donnez un nombre de robots (entier entre 1 et {}), conseil: prendre une valeur proche de la borne inférieure :".format(grille_x*grille_y-1)))
print("")
(liste_robots, positions_libres, positions_occupees, etiquettes) = creation_robots(nbre_de_robots, grille_x, grille_y)

# Choix du nombre d'itérations dans la simulation par l'utilisateur et déclanchement de la simulation + affichage de l'histogramme du nombre de cases différentes visitées par chaque robot lors de la simulation.
print("")
nbre_iteration = int(input("Choisissez un nombre d'itérations dans la simulation de vie :"))
print("")
liste_cases_visitees = vie_robot(liste_robots, positions_libres, positions_occupees, nbre_iteration,  grille_x, grille_y, etiquettes)
nbre_case_diff_robot = recuperation_coord_robot(liste_cases_visitees, liste_robots)
histogramme(liste_robots, nbre_case_diff_robot)
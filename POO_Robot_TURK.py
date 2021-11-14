#!/bin/env python         
# -*- coding: utf-8 -*-   

'''
Classe des Robots de premiere generation
'''

class Robot(object):
    """
    Classe de robots de 1ère génération.
    """
    def __init__(self, nom_robot, coord_x = 0, coord_y = 0, direction = "Est"):  # position du robot par défaut à (0, 0) avec direction à l'Est
        """
        Cree un robot de 1ère génération.
        """
        self.nom = nom_robot
        self.px = coord_x
        self.py = coord_y
        self.direction = direction

    def avance(self):   
        """
        Le robot avance d'un pas.
        """
        dico_rotation = {"Nord": [0,1],
                         "Est": [1,0],
                         "Sud": [0,-1],
                         "Ouest": [-1,0]}
        dx, dy = dico_rotation[self.direction][0], dico_rotation[self.direction][1]
        self.px += dx
        self.py += dy

    def droite(self):
        """
        Le robot tourne a droite de 90 degres.
        """
        liste_direction = ["Nord", "Est", "Sud", "Ouest"]  
        N = len(liste_direction)
        index_direction = liste_direction.index(self.direction)   
        if index_direction <= N-2:
            self.direction = liste_direction[index_direction + 1]
        else:
            self.direction = liste_direction[0]

    def surface_couverte(self, liste_coord):
        """
        Entree: 
        - liste_coord: liste des coordonnees des cases occupees par un robot lors de la simulation.
        
        --> Renvoie le nombre de cases distinctes visitées par ce robot.
        """
        liste_coord_unique = []                       # initialisation de la liste des coordonnees des cases distinctes occupees par un robot lors de la simulation
        for element in liste_coord:
            if element not in liste_coord_unique:     # si la case visitée n'a pas encore été ajoutée à la liste des cases visitées, l'ajouter
                liste_coord_unique.append(element)
        surface = len(liste_coord_unique)             # nombre de cases distinctes visitées par le robot
        return surface

'''
Classe des Robots NG (Nouvelle Génération) 
'''

class RobotNG(Robot):
    def __init__(self, nom_robot, coord_x = 0, coord_y = 0, direction = "Est"):  
        """
        Cree un robot de Nouvelle Génération.
        """
        Robot.__init__(self, nom_robot, coord_x, coord_y, direction)               # la classe RobotNG hérite de la classe Robot
        
    def avance(self, nombre_pas):   
        """
        Le robot avance d'un nombre de pas valant nombre_pas.
        """
        dico_rotation = {"Nord": [0,1],
                         "Est": [1,0],
                         "Sud": [0,-1],
                         "Ouest": [-1,0]}
        dx, dy = dico_rotation[self.direction][0], dico_rotation[self.direction][1]
        self.px += nombre_pas*dx
        self.py += nombre_pas*dy

    def gauche(self):   
        """
        Le robot tourne a gauche de 90 degres.
        """
        liste_direction = ["Nord", "Ouest", "Sud", "Est"]  
        N = len(liste_direction)
        index_direction = liste_direction.index(self.direction)   
        if index_direction <= N-2:
            self.direction = liste_direction[index_direction + 1]
        else:
            self.direction = liste_direction[0]

    def demiTour(self):
        """
        Le robot tourne de 180 degres.
        """
        dico_demiTour = {"Nord" : "Sud",
                         "Sud"  : "Nord",
                         "Est"  : "Ouest",
                         "Ouest": "Est"}
        self.direction = dico_demiTour[self.direction]




"""
Test de verification des classes crees
"""

# Tests Robot de 1ère génération

print("")
print("Tests de la classe Robot".center(100, "-"))  

robot1 = Robot("robot_test")        # test de création d'un robot de première génération
print("Création d'une instance de la classe Robot de nom : {}".format(robot1.nom))
print("Position initiale de {} : {} , {}".format(robot1.nom, robot1.px, robot1.py))

robot1.avance()                     # test de la méthode .avance() relative à la classe Robot
print("Position de {} après 1 pas vers la direction {} : {} , {}".format(robot1.nom, robot1.direction, robot1.px, robot1.py))

robot1.droite()                     # test de la méthode .droite() relative à la classe Robot
robot1.avance() 
print("Position de {} après 1 pas vers la direction {} : {} , {}".format(robot1.nom, robot1.direction, robot1.px, robot1.py))


# Tests RobotNG (nouvelle génération)

print("")
print("Tests de la classe RobotNG".center(100, "-"))  

robotNG1 = RobotNG("robotNG1")      # test de création d'un robot NG
print("Création d'une instance de la classe RobotNG de nom : {}".format(robotNG1.nom))
print("Position initiale de {} : {} , {}".format(robotNG1.nom, robotNG1.px, robotNG1.py))

nombre_de_pas = 5
robotNG1.avance(nombre_de_pas)      # test de la méthode .avance() relative à la classe RobotNG (avancer de plusieurs pas en 1 appel de la méthode)
print("Position de {} après {} pas vers la direction {} : {} , {}".format(robotNG1.nom, nombre_de_pas, robotNG1.direction, robotNG1.px, robotNG1.py))

robotNG1.gauche()                   # test de la méthode .gauche() relative à la classe RobotNG
nombre_de_pas = 10
robotNG1.avance(nombre_de_pas)
print("Position de {} après {} pas vers la direction {} : {} , {}".format(robotNG1.nom, nombre_de_pas, robotNG1.direction, robotNG1.px, robotNG1.py))

robotNG1.demiTour()                 # test de la méthode .demiTour() relative à la classe RobotNG
nombre_de_pas = 5
robotNG1.avance(nombre_de_pas)     
print("Position de {} après {} pas vers la direction {} : {} , {}".format(robotNG1.nom, nombre_de_pas, robotNG1.direction, robotNG1.px, robotNG1.py))


    

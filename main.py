##########################   IMPORTATION & DEFINITIION DES CONSTANTES ########################

from utils import World
from os import system
from time import sleep

hauteur = 10
largeur = 7

##########################   INITIALISATION DU MONDE       ###################################
monde = World(hauteur,largeur)
monde.generer_requins(5)
monde.generer_thons(13)

###########################    BOUCLE PRINCIPALE             #################################
for i in range (50):
    _ = system('clear')
    monde.variation_pop = 0
    monde.display_world()
    len(monde.liste_creatures)
    nb_creatures = len(monde.liste_creatures) + monde.variation_pop
    print(f"\nil y a {nb_creatures} creatures")
    for i in range(nb_creatures):
        if i == nb_creatures + monde.variation_pop + 1:
            break
        creature =(monde.liste_creatures[i-1])
        creature.se_deplacer(monde, creature.choix_deplacement(creature.cases_autour(monde)))
    
    sleep(2)
    
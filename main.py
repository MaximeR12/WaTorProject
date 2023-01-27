##########################   IMPORTATION & DEFINITIION DES CONSTANTES ########################

from utils import World, Thon, Requin
from os import system
from time import sleep

hauteur = 20
largeur = 13


##########################   INITIALISATION DU MONDE       ###################################

monde = World(hauteur,largeur)
monde.generer_requins(monde.taille[2]//8)
monde.generer_thons(monde.taille[2]//3)
Thon.limite_reproduction = 4
Requin.energie = 7
Requin.limite_reproduction = 8
Requin.gain_energie = 5
compteur_tours = 0


###########################    BOUCLE PRINCIPALE             #################################

while len(monde.liste_requins) > 0 and len(monde.liste_poissons) > 0:
    _ = system('clear')
    monde.display_world()
    print(f"\n{len(monde.liste_poissons)} poissons")
    print(f"{len(monde.liste_requins)} requins")

    for requin in monde.liste_requins:
        requin.se_deplacer(monde, requin.choix_deplacement(requin.cases_autour(monde)))
        monde.update_creatures()

    for poisson in monde.liste_poissons:
        poisson.se_deplacer(monde, poisson.choix_deplacement(poisson.cases_autour(monde)))
        monde.update_creatures()
    compteur_tours+=1
    sleep(0.3)


####################### AFFICHAGE APRES FIN DE LA BOUCLE  ###################################

_ = system('clear')
monde.display_world()
print(f"\n{len(monde.liste_poissons)} poissons")
print(f"{len(monde.liste_requins)} requins")
print(f'nombre de tours : {compteur_tours}')
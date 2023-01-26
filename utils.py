from random import randint,choice,shuffle

class World:
    def __init__(self, ligne, colonne):
        self.taille = [ligne, colonne, ligne*colonne]
        self.liste_creatures = []                  
        self.grille = []
        self.variation_pop = 0
        for i in range(ligne):
            ligne=[]
            for j in range(colonne):
                ligne.append(' ')
            self.grille.append(ligne)


    def display_world(self):
        """
        Print the grid with ' ' as water, 'R' for sharks, 'T' for thons
        """
        print('\n')
        for ligne in self.grille:
            for content in ligne:
                print (content,end="\t")
            print('',end="\n")



    def generer_requins(self, nb_requins):
        """
        generate sharks in self.grille list

        Args:
            nb_requins (int): number of sharks to generate in the grid
        """
        compteur = 0
        while compteur <= nb_requins -1:
            y = randint(0,self.taille[0]-1)
            x = randint(0,self.taille[1]-1)
            if self.grille[y][x]==' ':                #On cherche a verifier si le X ième element de la Y ième liste est vide
                compteur +=1
                self.liste_creatures.append(Requin(y,x))
                self.grille[y][x] = 'R'               #si c'est le cas, on la remplace par un requin

    
    def generer_thons(self, nb_thons):
        """generate fishes in the self.grille grid

        Args:
            nb_thons (int): _description_
        """
        compteur = 0
        while compteur < nb_thons:
            y = randint(0,self.taille[0]-1)
            x = randint(0,self.taille[1]-1)
            if self.grille[y][x]==' ':                #On cherche a verifier si le X ième element de la Y ième liste est vide
                self.liste_creatures.append(Thon(y,x))
                self.grille[y][x] = 'T'           #si c'est le cas, on la remplace par un thon
                compteur +=1

    def mourir(self, coord):
        """delete the object (shark or fish) that has the exact same coordinates as the coord var

        Args:
            coord (list): a list of 2 elements that represents the coordinates of the object to kill [row, column]
        """
        ligne = coord[0]
        colonne = coord[1]

        self.variation_pop -= 1
        cre_list = self.liste_creatures.copy()
        for creature in cre_list:
            if creature.ligne == ligne and creature.colonne == colonne:
                (self.liste_creatures).remove(creature)
                break

class Creature:
    """"
    classe de toutes les créatures
    """
    def __init__(self) -> None:
        self.compteur_reproduction=0 # attribut commun à toutes les créatures
        



    def se_reproduire(self):
        pass
    def manger(self):
        pass


    def cases_autour(self, monde) -> dict:
        """checks the cases around the coordinates of the object by watching monde.grid and checking for 'R' or 'T'

        Args:
            monde (object): instance of the world in which the grid must be checked

        Returns:
            dict: dict containing lists of coordinates of empty cases at key "vide", coordinates of cases with sharks at key "requins", coordinates of cases with fishes at key "thons"
        """
        liste_vide ,liste_thon, liste_requin = [], [], []

        hauteur = monde.taille[0]
        largeur = monde.taille[1]

        nord = [(self.ligne-1) % hauteur, self.colonne]
        sud = [(self.ligne+1) % hauteur, self.colonne]
        est = [self.ligne, (self.colonne+1) % largeur]
        ouest = [self.ligne, (self.colonne-1) % largeur]
        coord_autour = [nord, sud, est, ouest]
        
        for l in coord_autour:
            if monde.grille[l[0]][l[1]] == 'R':
                liste_requin.append(l)
            elif monde.grille[l[0]][l[1]] == 'T':
                liste_thon.append(l)
            else:
                liste_vide.append(l)
        
        return {"vide" : liste_vide, "thons" : liste_thon, "requins" : liste_requin}


class Requin(Creature):
    limite_reproduction = 7
    def __init__(self, ligne, colonne) -> None:
        Creature.__init__(self)# attributs de la sous classe à définir
        #Creature.__init__(self): # hérite les attributs de la classe Creature
        self.ligne = ligne
        self.colonne = colonne
        self.energie = 6


    def choix_deplacement(self, dico):
        """takes the dictionnary from cases_autour and return coordinates of dico["thons"] if not empty, else it returns coordinates from dico[empty]

        Args:
            dico (dict): dict with keys : "vide" "requins" "thons"

        Returns:
            list: list of 2 coordinates that represents where the object should go
        """
        if dico["thons"] != []:
            return choice(dico["thons"])
        elif dico["vide"]==[]:
            return []
        return choice(dico["vide"])



    def se_deplacer(self, monde, coord_cible):
        if self.energie <=0:
            monde.mourir([self.ligne, self.colonne])
            monde.grille[self.ligne][self.colonne] = ' '
                
        
        elif coord_cible != []:
            colonne_avant = self.colonne
            ligne_avant = self.ligne

            if monde.grille[coord_cible[0]][coord_cible[1]] == 'T':
                monde.mourir(coord_cible)
                self.energie = 5
            
            self.colonne = coord_cible[1]
            self.ligne = coord_cible[0]
            monde.grille[coord_cible[0]][coord_cible[1]] = 'R'
            

            if self.compteur_reproduction >= self.limite_reproduction:
                monde.grille[ligne_avant][colonne_avant] = 'R'
                (monde.liste_creatures).insert(0,Requin(ligne_avant, colonne_avant))
                monde.variation_pop += 1
                self.compteur_reproduction = 0
            else:
                monde.grille[ligne_avant][colonne_avant] = ' '
                
        self.energie -= 1
        self.compteur_reproduction += 1



# création de sous classe
class Thon(Creature):
    limite_reproduction = 10
    energie = 99
    def __init__(self, ligne, colonne) -> None:
        Creature.__init__(self)# attributs de la sous classe à définir
        self.ligne = ligne
        self.colonne = colonne                #Creature.__init__(self): # hérite les attributs de la classe Creature

    def choix_deplacement(self, dico):
        if dico["vide"]==[]:
            return []
        return choice(dico["vide"])

    def se_deplacer(self, monde, coord):

        if coord != []:
            colonne_avant = self.colonne
            ligne_avant = self.ligne
            self.colonne = coord[1]
            self.ligne = coord[0]

            if self.compteur_reproduction >= self.limite_reproduction:
                monde.grille[coord[0]][coord[1]] = 'T'
                monde.grille[ligne_avant][colonne_avant] = 'T'
                (monde.liste_creatures).insert(0,Thon(ligne_avant, colonne_avant))
                monde.variation_pop += 1
                self.compteur_reproduction = 0
            else:
                monde.grille[coord[0]][coord[1]] = 'T'
                monde.grille[ligne_avant][colonne_avant] = ' '

        self.compteur_reproduction += 1



from random import randint,choice
#####################################################################################################
##############################        CLASS  WORLD     ##############################################
#####################################################################################################

class World:
    def __init__(self, ligne, colonne):
        self.taille = [ligne, colonne, ligne*colonne]
        self.liste_requins = []
        self.liste_poissons = []
        self.requins_morts = []  
        self.nouv_req = []
        self.nouv_poiss = []                
        self.grille = []
        for i in range(ligne):
            ligne=[]
            for j in range(colonne):
                ligne.append(' ')
            self.grille.append(ligne)


    def display_world(self):
        """
        Print the grid with ' ' as water, 'R' for sharks, 'T' for thons
        """
        barre=(8*(self.taille[1])-1)*'-'
        print(f'+{barre}+')
        for ligne in self.grille:
            print('⏐',end='')
            for content in ligne:
                print (content,end="\t")
            print('⏐',end="\n")
        print(f'+{barre}+')


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
                self.liste_requins.insert(0,Requin(y,x))
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
                self.liste_poissons.append(Thon(y,x))
                self.grille[y][x] = 'T'           #si c'est le cas, on la remplace par un thon
                compteur +=1

    def mourir(self, coord):
        """delete the object (shark or fish) that has the exact same coordinates as the coord var

        Args:
            coord (list): a list of 2 elements that represents the coordinates of the object to kill [row, column]
        """
        ligne = coord[0]
        colonne = coord[1]

        cre_list = self.liste_requins + self.liste_poissons
        for creature in cre_list:
            if creature.ligne == ligne and creature.colonne == colonne:
                self.grille[ligne][colonne] = ' '
                if cre_list.index(creature) < len(self.liste_requins):
                    (self.requins_morts).append(creature)
                    self.grille[ligne][colonne] = ' '
                else:
                    (self.liste_poissons).remove(creature)
                break

    def update_creatures(self):
        while len(self.requins_morts) >0:
            (self.liste_requins).remove(self.requins_morts[0])
            self.requins_morts.pop(0)
        while len(self.nouv_poiss) > 0:
            self.liste_poissons.append(self.nouv_poiss[0])
            self.nouv_poiss.pop(0)
        while len(self.nouv_req) > 0:
            self.liste_requins.append(self.nouv_req[0])
            self.nouv_req.pop(0)


#####################################################################################################
###################################  CLASS  REQUINS  ################################################
#####################################################################################################

class Requin():
    limite_reproduction = 0
    gain_energie = 0
    def __init__(self, ligne, colonne) -> None:
        self.compteur_reproduction = 0
        self.ligne = ligne
        self.colonne = colonne
        self.energie = 10

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
        """changes the coordinates (self.ligne and self.colonne) attributes and changes the data in monde.grille
        if self has moved enough to reproduces, creates a new object at the old position of self

        Args:
            monde (object): instance of Monde class, it carries the monde.grille andmonde.list_creatures
            coord_cible (list): list containing 2 elements representing the future coordinates of self
        """
        if self.energie <=0:
            monde.grille[self.ligne][self.colonne] = ' '
            monde.mourir([self.ligne, self.colonne])
                
        
        elif coord_cible != []:
            colonne_avant = self.colonne
            ligne_avant = self.ligne

            if monde.grille[coord_cible[0]][coord_cible[1]] == 'T':
                monde.mourir(coord_cible)
                self.energie = Requin.gain_energie
            
            self.colonne = coord_cible[1]
            self.ligne = coord_cible[0]
            monde.grille[coord_cible[0]][coord_cible[1]] = 'R'
            

            if self.compteur_reproduction >= self.limite_reproduction:
                monde.grille[ligne_avant][colonne_avant] = 'R'
                (monde.nouv_req).append(Requin(ligne_avant, colonne_avant))
                self.compteur_reproduction = 0
            else:
                monde.grille[ligne_avant][colonne_avant] = ' '
                
        self.energie -= 1
        self.compteur_reproduction += 1


#####################################################################################################
######################################    CLASS  POISSONS   #########################################
#####################################################################################################

class Thon():
    limite_reproduction = 5
    def __init__(self, ligne, colonne) -> None:
        self.compteur_reproduction = 0
        self.ligne = ligne
        self.colonne = colonne                #Creature.__init__(self): # hérite les attributs de la classe Creature

    def cases_autour(self, monde) -> dict:
        """checks the cases around the coordinates of the object by watching monde.grille and checking if it's empty in the grid (==' ')

        Args:
            monde (object): instance of the world in which the grid must be checked

        Returns:
            list: list containing list(s) with 2 coordinates of empty cases
        """
        liste_vides = []

        hauteur = monde.taille[0]
        largeur = monde.taille[1]

        nord = [(self.ligne-1) % hauteur, self.colonne]
        sud = [(self.ligne+1) % hauteur, self.colonne]
        est = [self.ligne, (self.colonne+1) % largeur]
        ouest = [self.ligne, (self.colonne-1) % largeur]
        coord_autour = [nord, sud, est, ouest]
        
        for direction in coord_autour:
            if monde.grille[direction[0]][direction[1]] == ' ':
                liste_vides.append(direction)
        
        return liste_vides

    def choix_deplacement(self, liste_coord):
        """randomly chooses one of the coordinates in liste_coord

        Args:
            liste_coord (list): list of list of coordinates,

        Returns:
            list: list of 2 int in the Monde.grid if liste_coord == [] returns []
        """
        if liste_coord==[]:
            return []
        return choice(liste_coord)


    def se_deplacer(self, monde, coord):
        """moves the self representation in the grid and changes the self.ligne, self.colonne
        if the self has survived enough turns to reproduce, creates a new Thon object at the old position of self

        Args:
            monde (object): instance of Monde object
            coord (list): list of 2 int representing new coordinates for self.ligne and self.colonne
        """

        if coord != []:
            colonne_avant = self.colonne
            ligne_avant = self.ligne
            self.colonne = coord[1]
            self.ligne = coord[0]

            if self.compteur_reproduction >= self.limite_reproduction:
                monde.grille[coord[0]][coord[1]] = 'T'
                monde.grille[ligne_avant][colonne_avant] = 'T'
                (monde.nouv_poiss).append(Thon(ligne_avant, colonne_avant))
                self.compteur_reproduction = -1
            else:
                monde.grille[coord[0]][coord[1]] = 'T'
                monde.grille[ligne_avant][colonne_avant] = ' '

        self.compteur_reproduction += 1

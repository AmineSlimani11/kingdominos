import pygame as pg
from pygame.locals import *

import random as rnd
import numpy as np

ecran = None  # pour l'affichage, initialisé après

class Ecran:
    def __init__(self, dim_x, dim_y, titre):
        self.cursor = (0, 0)
        self.taille_fonte_y = 20
        pg.init()
        if not pg.font.get_init():
            print("Désolé, les fontes de caractères sont absentes, je ne peux démarrer")
            quit()
        self.font = pg.font.SysFont("Courrier, Monospace",
                                    self.taille_fonte_y)
        self.taille_fonte_x = self.font.size('A')[0]
        self.ecran = pg.display.set_mode((dim_x * self.taille_fonte_x ,
                                          dim_y * self.taille_fonte_y))
        pg.display.set_caption(titre)
    def write(self, texte, fgcolor=(255,255,255), bgcolor=(0,0,0)):
        texte = self.font.render(texte,
                            True,
                            pg.Color(fgcolor),
                            pg.Color(bgcolor))
        self.ecran.blit(texte,
                        (self.cursor[0]*self.taille_fonte_x,
                         self.cursor[1]*self.taille_fonte_y))
        pg.display.flip()

class Oriente:
    ''' conventions pour donner l'orientation d'un domino.
    Utilisation: if sens == Oriente.GD: ...    (Voir dessiner_domino())
    '''
    GD = 0   # domino orienté Gauche à Droite
    HB = 1   # domino orienté Haut vers Bas
    DG = 2   # domino orienté Droite à Gauche
    BH = 3   # domino orienté Bas vers Haut

class Cellule:
    ''' cellule du plateau de jeu et aussi élément de domino (voir ci-dessous) '''
    def __init__(self, terrain='a', bonus=0) :
        ''' défaut vide et autorisée en écriture, sans bonus de comptage de point '''
        self._terrain = terrain
        self._couleur = Params.couleur[terrain]
        self._bonus = bonus
        self._decompte = False
    # fonctions accesseurs pour lire les attributs
    # (qui ne doivent pas être modifiables après création de la cellule)
    def terrain(self):
        return self._terrain
    def couleur(self):
        return self._couleur
    def bonus(self):
        return self._bonus
    def decompte(self):
        return self._decompte
    def set_decompte(self):
        self._decompte = True

class Domino:
    ''' un domino pour le jeu (ne pas confondre avec la liste des "dominos" dans la
    classe Params ci-dessous qui est juste une représentation en chaînes de texte)
    - on pourra indicer par [0] et [1] les 2 cellules du domino et demander son
    numéro de domino par la méthode numero()    
    '''
    def __init__(self, numero = -1, cell1 = None, cell2 = None):
        self._numero = numero
        self._cellule = [cell1, cell2]
    def __getitem__(self, indice):   # implante l'indiçage: objet[indice]
        if isinstance(indice, int):   # implante l'indiçage par entier (pas par tranches)
            return self._cellule[indice]
    def numero(self):
        return self._numero
        
class Params:
    ''' paramètres du jeu : seulement des variables de classe, pas de méthodes
        ni de variables d'instances/objets
        exemple d'utilisation: pile_dominos = Params.dominos'''
    # couleurs utiles définies en RGB sur [0,255]
    couleurs_utiles = {
        'champ'   : (198, 175, 15),
        'bois'    : (52, 122, 48),
        'pature'  : (135, 220, 69),
        'marais'  : (154, 182, 135),
        'filon'   : (170, 110, 90),
        'eau'     : (80, 115, 224),
        'chateau' : (255, 255, 255),
        'interdit': (0, 0, 0),
        'autorisé': (100, 100, 100),
        'rouge'   : (213, 11, 11),
        'bleu'    : (11, 11, 240),
        'blanc'   : (255, 255, 255),
        'noir'    : (0, 0, 0)
    }
    # couleur associées aux types de terrain des cellules
    couleur = {
        'i': couleurs_utiles['interdit'],
        'a': couleurs_utiles['autorisé'],
        '#': couleurs_utiles['chateau'],
        'C': couleurs_utiles['champ'],
        'E': couleurs_utiles['eau'],
        'P': couleurs_utiles['pature'],
        'M': couleurs_utiles['marais'],
        'F': couleurs_utiles['filon'],
        'B': couleurs_utiles['bois'],
    }
    # liste des dominos du jeu comme nuplet d'abbréviations de terrains avec
    # chaque bonus marqué comme "+": ces nuplets devront être traduits
    liste_dominos = [
        ("C", "C"), ("C", "C"), ("B", "B"), ("B", "B"), ("B", "B"), ("B", "B"),
        ("E", "E"), ("E", "E"), ("E", "E"), ("P", "P"), ("P", "P"), ("M", "M"),
        ("B", "C"), ("C", "E"), ("C", "P"), ("C", "M"), ("B", "E"), ("B", "P"),
        ("B", "C+"), ("C+", "E"), ("C+", "P"), ("C+", "M"), ("C+", "F"), ("B+", "C"),
        ("B+", "C"), ("B+", "C"), ("B+", "C"), ("B+", "E"), ("B+", "P"), ("C", "E+"),
        ("C", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("C", "P+"),
        ("P+", "E"), ("C", "M+"), ("P", "M+"), ("C", "F+"), ("C", "P++"), ("E", "P++"),
        ("C", "M++"), ("P", "M++"), ("C", "F++"), ("M", "F++"), ("M", "F++"), ("C", "F+++")
        ]
    # nombre et répartitions des rois # 4 rois, 2 pour joueur 0, 2 pour joueur 1
    nombre_rois = (4, (2, 2))  
    # dimensions pour tracer les terrains des joueurs
    taille_terrain = 11  # taille du côté de la zone de jeu en nombre de cellules
    taille_cellule = (2, 1)  # taille (x,y) cellule de zone de jeu en caracteres
    dim_ecran_x = taille_cellule[0] * taille_terrain * 2 + 3
    dim_ecran_y = taille_cellule[1] * (taille_terrain + 8) + 6
    # ligne où afficher les infos sans pause
    lig_info = (taille_terrain - 2) * taille_cellule[1] + 2
    # ligne où afficher les messages avec pause
    lig_message = (taille_terrain + 8) * taille_cellule[1] + 4
    # décalage horizontal terrain 2nd joueur
    decal_x_joueur2 = taille_cellule[0] * taille_terrain + 1
    # dimensions pour affichage des tirages de dominos
    tirage_y = lig_info + 2
    tirage_x = 6
    tirage_droit_x = 20
    
##########
##### fonctions graphiques
##########

def init_graphiques():
    ''' construit la palette de couleurs curses pour les types de terrains 
    '''
    global ecran
    ecran = Ecran(Params.dim_ecran_x,
                  Params.dim_ecran_y,
                  'Projet KD')
    
def attendre():
    ''' attendre une pression de touche ENTRÉE '''
    global ecran
    pg.event.clear()
    while True:
        event = pg.event.wait()
        if event.type == QUIT:  # toujours traiter action fermer la fenêtre de jeu
            exit()
        if (event.type == pg.KEYUP and
            event.key == pg.K_RETURN):  # attendre relachement de touche ENTRÉE
            break
    
def message(texte):
    """ affiche un message en bas de l'écran et attends une pression de touche """
    global ecran
    ecran.cursor = (0, Params.lig_message)
    ecran.write(" " * 80)  # efface ligne des messages
    ecran.cursor = (0, Params.lig_message)
    ecran.write(texte)
    attendre()
    ecran.write(" " * 80)  # efface ligne des messages
    
def info(texte):
    """ affiche une info au dessus de la zone de choix de l'écran sans attendre """
    global ecran
    ecran.cursor = (0, Params.lig_info)
    ecran.write(" " * 80)  # efface ligne des messages
    ecran.write(texte)
            
def dessiner_cellule(ligne, colonne, cellule, mode="normal"):
    ''' dessine une cellule de terrain dans la couleur de son contenu '''
    global ecran
    if mode == "possible":  # place possible domino, mettre en relief avec ">  <"
        motif = "<>"
    elif mode == "impossible":  # place impossible, mettre en relief avec "@  @" 
        motif = "@@"
    else:  # mode normal de dessin
        motif = "  "

    lig = ligne
    col = colonne    
    for i in range(Params.taille_cellule[1]):
        ecran.cursor = (col, lig)
        ecran.write(motif, bgcolor = cellule.couleur())
        lig += 1
    # gère bonus
    if cellule.bonus():
        ecran.cursor = (colonne + 1, ligne)
        ecran.write(str(cellule.bonus()),
                    fgcolor = Params.couleurs_utiles["blanc"],
                    bgcolor = cellule.couleur())                    

def dessiner_domino(haut, gauche, orient, domino, mode="normal"):
    global ecran
    if orient == Oriente.GD:   # domino horizontal sens domino[0], domino[1]
        dessiner_cellule(haut, gauche, domino[0], mode)
        dessiner_cellule(haut, gauche+Params.taille_cellule[0], domino[1], mode)
    elif orient == Oriente.HB:   # domino vertical sens domino[0], domino[1]
        dessiner_cellule(haut, gauche, domino[0], mode)
        dessiner_cellule(haut+Params.taille_cellule[1], gauche, domino[1], mode)
    elif orient == Oriente.DG:   # domino horizontal sens domino[1], domino[0]
        dessiner_cellule(haut, gauche, domino[0], mode)
        dessiner_cellule(haut, gauche-Params.taille_cellule[0], domino[1], mode)  
    elif orient == Oriente.BH:   # domino vertical sens domino[1], domino[0]
        dessiner_cellule(haut, gauche, domino[0], mode)
        dessiner_cellule(haut-Params.taille_cellule[1], gauche, domino[1], mode)

def abs_coord(joueur, ligne, colonne):
    ''' convertir des coords sur le tableau terrain en coords cellule à l'écran '''
    if joueur == 0:
        return (ligne * Params.taille_cellule[1] - 1,
                colonne * Params.taille_cellule[0] - 2)
    else:  # joueur == 1
        return (ligne * Params.taille_cellule[1] - 1,
                colonne * Params.taille_cellule[0] + Params.decal_x_joueur2)
        
def dessiner_terrains(terrains):
    global ecran
    # dessiner les éléments de terrain
    for joueur in range(len(terrains)):
        for ligne in range(1, Params.taille_terrain - 1):
            for colonne in range(1, Params.taille_terrain - 1):
                # convertir coords terrain en coords absolues écran
                lig, col = abs_coord(joueur, ligne, colonne)
                dessiner_cellule(lig, col, terrains[joueur][ligne][colonne])

def dessiner_tirage(tirage, choix, cote):
    ''' 
    dessine une pile de dominos, avec éventuel placement des rois/choix des joueurs,
    à 'gauche' ou 'droite' selon la valeur de cote
    '''
    global ecran
    if cote == "gauche":
        # effacer côté droit
        col = Params.tirage_droit_x
        for ligne in range(len(tirage) * (Params.taille_cellule[1] + 2)):
            lig = Params.tirage_y + ligne
            ecran.cursor = (col, lig)
            ecran.write(" " * (80 - col))
        # fixer colonne d'affichage
        col = Params.tirage_x
    else:
        col = Params.tirage_droit_x
    for ligne in range(len(tirage)):
        lig = Params.tirage_y + ligne * (Params.taille_cellule[1] + 2)
        joueur = choix[ligne]
        if joueur == -1:  # pas choisi
            surligner_domino(ligne, "ko", cote)
        else:  # choisi
            surligner_domino(ligne, str(joueur), cote)
        dessiner_domino(lig, col, Oriente.GD, tirage[ligne])

def surligner_domino(position, mode, cote):
    global ecran
    lig = Params.tirage_y + position * (Params.taille_cellule[1] + 2)
    if cote == "gauche":
        col = Params.tirage_x - 4
    else:
        col = Params.tirage_droit_x - 4
    ecran.cursor = (col, lig)
    if mode == "ok":
        ecran.write(">> ")
    elif mode == "ko":
        ecran.write("   ")
    elif mode == "X":
        ecran.write("XXX")
    else:
        ecran.write("-"+mode+"-")

def lire_touche():
    pg.event.clear()
    while True:
        event = pg.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                return "HAUT"
            if event.key == pg.K_DOWN:
                return "BAS"
            if event.key == pg.K_LEFT:
                return "GAUCHE"
            if event.key == pg.K_RIGHT:
                return "DROITE"
            if event.key >=  pg.K_a and event.key <=  pg.K_z:
                lettre = chr(ord('a') + (event.key - pg.K_a))
                if event.mod and pg.KMOD_SHIFT:
                    return lettre.upper()
                else:
                    return lettre
            if event.key == pg.K_SPACE:
                return " "
        
def choisir_domino(choix, position, joueur, cote):
    ''' 
    choisi un domino pour le joueur num sur la pile du côté gauche ou droit 
    choix: liste des choix des joueurs
    '''
    global ecran
    # afficher le joueur
    info("Joueur n° "+str(joueur)+" place son roi: touches haut/bas et V=valider")
    # attendre son choix
    domino = -1
    # trouver le 1er domino libre
    dom_libres = [pos for pos, dom in enumerate(choix) if dom == -1]
    pos = 0  # indice du 1er domino libre
    while domino == -1:
        numero = dom_libres[pos]
        surligner_domino(numero, "ok", cote)
        touche = lire_touche()
        surligner_domino(numero, "ko", cote)
        if touche == "HAUT":
            pos = (pos - 1) % len(dom_libres)
        elif touche == "BAS":
            pos = (pos + 1) % len(dom_libres)
        elif touche == "V":
            surligner_domino(numero, str(joueur), cote)
            break
    choix[numero] = joueur
    info(" " * 80)  # nettoie

def placer_domino(domino, joueur, terrains):
    '''TODO: différencier coords selon joueur, tester position vs terrain'''
    # position de départ: sur le château
    centre = Params.taille_terrain // 2
    ligne = centre
    colonne = centre
    rotation = Oriente.GD
    info("Joueur "+str(joueur)+" placer: haut/bas/gauche/droite, espace=rotation, a=abandon, V=valider")
    while True:
        mode = position_possible(joueur, ligne, colonne, domino, rotation, terrains)
        lig, col = abs_coord(joueur, ligne, colonne)
        dessiner_domino(lig, col, rotation, domino, mode)
        touche = lire_touche()
        dessiner_terrains(terrains)
        if touche == "HAUT":
            ligne_propose = ligne - 1
            if (position_possible(joueur, ligne_propose, colonne, domino, rotation, terrains) !=
                "interdit"):
                ligne = ligne_propose
        elif touche == "BAS":
            ligne_propose = ligne + 1
            if (position_possible(joueur, ligne_propose, colonne, domino, rotation, terrains) !=
                "interdit"):
                ligne = ligne_propose
        if touche == "GAUCHE":
            colonne_propose = colonne - 1
            if (position_possible(joueur, ligne, colonne_propose, domino, rotation, terrains) !=
                "interdit"):
                colonne = colonne_propose
        elif touche == "DROITE":
            colonne_propose = colonne + 1
            if (position_possible(joueur, ligne, colonne_propose, domino, rotation, terrains) !=
                "interdit"):
                colonne = colonne_propose
        elif touche == " ":
            rotation_propose = (rotation + 1) % (Oriente.BH + 1)
            if (position_possible(joueur, ligne, colonne, domino, rotation_propose, terrains) !=
                "interdit"):
                rotation = rotation_propose
        elif touche == "A":
            # on abandonne le domino
            break
        elif (touche == "V" and
              position_possible(joueur, ligne, colonne, domino, rotation, terrains) ==
              "possible"):
            # ici on peut poser le domino à sa place définitive
            poser_domino(joueur, ligne, colonne, domino, rotation, terrains)
            dessiner_terrains(terrains)
            break

    
##########
##### fonctions de gestion du jeu
##########
    
def choisir_nombre_joueurs():
    ''' TODO: gérer plus de 2 joueurs ? cela impactera d'autres fonctions
    '''
    return 2

def ajuster_dominos_joueurs(pile, nombre_joueurs):
    ''' ajuste le nombres de domino de la pile selon le nombre de joueurs
    TODO: gérer plus de 2 joueurs '''
    if nombre_joueurs == 2:
        return pile[:len(pile)//2]
    else:
        print("Désolé, on ne gère pas plus de 2 joueurs: fin de partie")
        quit()
    
def texte_en_cellule(texte):
    ''' transforme le texte de description d'une cellule en objet Cellule '''
    terrain = texte[0]
    bonus = texte.count('+')
    return Cellule(terrain, bonus)
    
def preparer_dominos(nombre_joueurs):
    ''' lit les descriptions de dominos, les convertit en liste d'objets de
    classe Domino, les mélange et ajuste leur nombre selon le nombre de joueurs,
    retourne la pile d'objets Domino'''
    pile = Params.liste_dominos[:]
    # ajouter numéro de tuile (toujours avant de mélanger) et convertir en cellules
    for i in range(len(pile)):
        dom = pile[i]
        pile[i] = Domino(i, texte_en_cellule(dom[0]), texte_en_cellule(dom[1]))
    # mélange
    rnd.shuffle(pile)
    # retire des dominos si nécessaire selon règle
    return  ajuster_dominos_joueurs(pile, nombre_joueurs)

def preparer_terrains(nombre_joueurs):
    ''' prépare la zone de jeu de chaque joueur: un tableau numpy de cellules
    vides et autorisées à poser des dominos, sauf la cellule au centre qui
    est le château du joueur (point de départ des dominos)
    '''
    terrains = []
    # un terrain par joueur, encadré d'une couronne toujours vide
    for i in range(nombre_joueurs):
        terrains.append(
            np.ndarray(shape=(Params.taille_terrain, Params.taille_terrain),
                     dtype=object))
    # initialise les zones de jeu et place les châteaux au centre
    centre = Params.taille_terrain // 2
    for joueur in range(nombre_joueurs):
        for i in range(Params.taille_terrain):
            for j in range(Params.taille_terrain):
                if i == centre and j == centre:
                    terrains[joueur][i][j] = Cellule("#")   # place château
                elif (i == 0 or i == Params.taille_terrain - 1 or
                      j == 0 or j == Params.taille_terrain - 1):
                    terrains[joueur][i][j] = Cellule("i")  # bord interdit
                else:   # défaut cellule vide autorisée
                    terrains[joueur][i][j] = Cellule()
    return terrains

def piocher_dominos(pile, nombre_rois):
    ''' récupérer le bon nombre de dominos pour ce tour, les trier '''
    tirage = []   # les dominos qui sont en jeu ce tour
    for i in range(nombre_rois):
        tirage.append(pile.pop())
    # les trier par numéro
    tirage.sort(key= lambda domino: domino.numero())
    return tirage

def ordre_jeu_initial(nombre_joueurs):
    ''' rend une liste avec les numéros des joueurs dans l'ordre du tour (valable
    pour plus de 2 joueurs)
    '''
    ordre = [] 
    for joueur in range(len(Params.nombre_rois[1])):
        for rois in range(Params.nombre_rois[1][joueur]):
            ordre.append(joueur)   # ajoute le numéro du joueur dans l'ordre 
    rnd.shuffle(ordre)  # mélange initialement l'ordre des tours des joueurs
    return ordre

def placer_rois_initiaux(ordre_jeu):
    ''' 
    procède au choix de la 1ère série de dominos
    '''
    choix = [-1] * len(ordre_jeu)   # indices choisis par joueurs (-1 = pas encore choisi)
    for numero_roi in range(len(ordre_jeu)):
        # trouver à qui le tour (convention : -1 dans l'ordre de jeu si déjà joué)
        joueurs_en_lice = [position for position,joueur in enumerate(ordre_jeu) if joueur != -1]
        position = joueurs_en_lice[0]
        choisir_domino(choix, position, ordre_jeu[position], cote="droite")
        ordre_jeu[position] = -1
    return choix

def coord_2nd_cellule_domino(ligne, colonne, rotation):
    if rotation == Oriente.GD:   # domino horizontal sens domino[0], domino[1]
        lig = ligne
        col = colonne + 1 
    elif rotation == Oriente.HB:   # domino vertical sens domino[0], domino[1]
        lig = ligne + 1
        col = colonne 
    elif rotation == Oriente.DG:   # domino horizontal sens domino[1], domino[0]
        lig = ligne
        col = colonne - 1 
    elif rotation == Oriente.BH:   # domino vertical sens domino[1], domino[0]
        lig = ligne - 1
        col = colonne
    return lig, col

def est_connecte(ligne, colonne, terrain, cellule):
    connecte_chateau = (terrain[ligne + 1, colonne].terrain() == "#" or
                        terrain[ligne, colonne + 1].terrain() == "#" or
                        terrain[ligne, colonne - 1].terrain() == "#" or
                        terrain[ligne - 1, colonne].terrain() == "#")
    connecte_terrain = (terrain[ligne + 1, colonne].terrain() == cellule.terrain() or
                        terrain[ligne, colonne + 1].terrain() == cellule.terrain() or
                        terrain[ligne, colonne - 1].terrain() == cellule.terrain() or
                        terrain[ligne - 1, colonne].terrain() == cellule.terrain())
    return connecte_chateau or connecte_terrain

def position_possible(joueur, ligne, colonne, domino, rotation, terrains):
    ''' retourne une indication sur la possibilité de placer un domino en ligne/colonne '''
    terrain = terrains[joueur]
    #  coord 2ème cellule domino
    lig, col = coord_2nd_cellule_domino(ligne, colonne, rotation)
    # position interdite ? (= sur bords du terrain)
    if (terrain[ligne][colonne].terrain() ==  "i" or 
        terrain[lig][col].terrain() ==  "i"):
        return "interdit"
    rien_dessous = (terrain[ligne][colonne].terrain() ==  "a" and
                    terrain[lig][col].terrain() ==  "a")
    # connecté à une même couleur ou château ?
    bien_connecte = (est_connecte(ligne, colonne, terrain, domino[0]) or
                     est_connecte(lig, col, terrain, domino[1]))
    if rien_dessous and bien_connecte:
        return "possible"
    else:
        return "impossible"

def poser_domino(joueur, ligne, colonne, domino, rotation, terrains):
    # poser
    terrains[joueur][ligne][colonne] = domino[0]
    lig, col = coord_2nd_cellule_domino(ligne, colonne, rotation)
    terrains[joueur][lig][col] = domino[1]
    # réduire le terrain possible en interdisant au delà de 5x5 case de cette cellule
    for i in range(0, ligne - 4):
        for j in range(Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
    for i in range(0, lig - 4):
        for j in range(Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
    for i in range(ligne + 5, Params.taille_terrain):
        for j in range(Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")
    for i in range(lig + 5, Params.taille_terrain):
        for j in range(Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")
            
    for i in range(Params.taille_terrain):
        for j in range(0, colonne-4):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
    for i in range(Params.taille_terrain):
        for j in range(0, col-4):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
    for i in range(Params.taille_terrain):
        for j in range(colonne+5, Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
    for i in range(Params.taille_terrain):
        for j in range(col+5, Params.taille_terrain):
            terrains[joueur][i][j] = Cellule("i")  # interdit dorénavant
            
def jouer_tour(pile, ancien_tirage, ancien_choix, terrains):
    dessiner_tirage(ancien_tirage, ancien_choix, cote="gauche")
    nombre_rois = len(ancien_choix)  # ne pas confondre nombre de rois et de joueurs
    if len(pile) > 0:
        nouveau_tirage = piocher_dominos(pile, nombre_rois)
        nouveau_choix = [-1] * nombre_rois
        dessiner_tirage(nouveau_tirage, nouveau_choix, cote="droit")
    else:
        nouveau_tirage = []
        nouveau_choix = []
    ordre_jeu = ancien_choix[:]  # le choix précédent donne l'ordre du tour suivant
    for numero_roi in range(len(ordre_jeu)):
        # choisir futur domino
        surligner_domino(numero_roi, "X", cote="gauche")
        joueur = ordre_jeu[numero_roi]
        if nouveau_tirage:  # s'il reste des numéros à tirer 
            choisir_domino(nouveau_choix, numero_roi, joueur, cote="droit")
        # placer "ancien" domino
        placer_domino(ancien_tirage[numero_roi], joueur, terrains)
        # marquer tour joué
        ordre_jeu[numero_roi] = -1
    return nouveau_tirage, nouveau_choix

def evaluer_zone(i, j, type_cellule, terrain):
    ''' retourne une paire (nombre de cases de la zone, somme des bonus de la zone) '''
    # fin de récursion : terrain déjà comptabilisé ou différent de type_cellule
    if (terrain[i][j].terrain() != type_cellule or
        terrain[i][j].decompte()):
        return 0, 0; # dans ce cas la zone actuelle est de taille 0, avec 0 bonus
    
    else: # on comptabilise la case courante
        terrain[i][j].set_decompte() # pour éviter de compter plusieurs fois la même case (récursion infinie)
        # on évalue la zone de ses voisines
        nord = evaluer_zone(i - 1, j, type_cellule, terrain)
        sud = evaluer_zone(i + 1, j, type_cellule, terrain)
        est = evaluer_zone(i, j + 1, type_cellule, terrain)
        ouest = evaluer_zone(i, j - 1, type_cellule, terrain)
        # cumuler les zones en comptant la cellule [i][j] elle-même
        cases = 1 + nord[0] + est[0] + sud[0] + ouest[0] # nombres de cases
        bonus = terrain[i][j].bonus() + nord[1] + est[1] + sud[1] + ouest[1] # somme des bonus
        return cases, bonus
    
def compter_points(terrains, nombre_joueurs):
    ''' Calcule et retourne sous forme de liste les points obtenus par les terrains de chaque joueur, renvoie une liste de sous-listes [numéro joueur, score]'''
    liste_scores = []
    for joueur in range(nombre_joueurs):
        le_terrain = terrains[joueur]
        score = 0
        for i in range(Params.taille_terrain):
            for j in range(Params.taille_terrain):
                # ignorer les cellules qui ne sont pas comptables
                if (le_terrain[i][j].terrain() == "i" or
                    le_terrain[i][j].terrain() == "a" or
                    le_terrain[i][j].terrain() == "#" or
                    le_terrain[i][j].decompte()):
                    continue;
                # ici cellule comptable et pas encore décomptée : on évalue la zone
                cases, bonus = evaluer_zone(i, j, le_terrain[i][j].terrain(), le_terrain)
                score_zone = cases * bonus # score de la zone
                score += score_zone # on met à jour le score
        liste_scores.append([joueur, score])
    return liste_scores
                
##########
##### fonction principale
##########

def kingdom():
    ''' joue une partie '''    
    # mémoriser l'écran pygcurse de manière globale
    global ecran

    # initialisations
    init_graphiques()
    nombre_joueurs = choisir_nombre_joueurs()
    pile = preparer_dominos(nombre_joueurs)
    terrains = preparer_terrains(nombre_joueurs)
    dessiner_terrains(terrains)

    # "tour" préparatoire pour placer les premiers rois
    ordre_jeu = ordre_jeu_initial(nombre_joueurs)
    nombre_rois = len(ordre_jeu)  # ne pas confondre nombre de rois et de joueurs
    tirage = piocher_dominos(pile, nombre_rois)
    choix = [-1] * len(ordre_jeu)   # indices choisis par joueurs (-1 = pas encore choisi)
    dessiner_tirage(tirage, choix, cote="droite")
    choix = placer_rois_initiaux(ordre_jeu)

    # boucle des tours de jeu
    compte_tours = 1
    while tirage:  # tant que tirage non vide, il reste des dominos à placer
        message("tour " + str(compte_tours) + " pressez ENTRÉE svp")        
        tirage, choix = jouer_tour(pile, tirage, choix, terrains)
        compte_tours += 1

    #afficher les résultats
    scores = compter_points(terrains, nombre_joueurs)
    message("Fin du tour " + str(compte_tours - 1))
    message("joueur 0: " + str(scores[0][1]) +
            " pts; joueur 1: " + str(scores[1][1]) + " pts")
    
    
if __name__ == "__main__":   # vrai si fichier exécuté et pas inclus comme module
    kingdom()

import pygame
from time import time
from random import randint


####### Manual ########

# flip alive cell -> mouse click
# multiple flip alive cell -> long click

# next generation -> space
# clean board -> c
# fill board -> w
# checkable -> b

# new project -> numbers
# move project -> arrows
# boost move -> b
# destroy project -> escape
# build project -> space

# flip auto generation -> a
# speed_up - > p
# speed_down -> m

# flip color -> f

#########################


class Color:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    GOLD = 200, 150, 30
    GREY = 125, 125, 125
    LIGHT_BLUE = 140, 160, 255
    LIGHT_GREEN = 140, 180, 160
    LIGHT_RED = 150, 50, 50
    LIGHT_GREY = 200, 200, 200
    DARK_GREY = 50, 50, 50
    DARK_GREY_1 = 90, 90, 90
    DARK_GREY_2 = 70, 70, 70
    DARK_GREY_3 = 30, 30, 30
    DARK_BLUE = 50, 50, 100


class Cell:
    colors = [Color.WHITE, None, Color.LIGHT_BLUE, Color.GREEN, Color.GOLD,
              Color.GREY]  # Liste des couleurs possibles des cellules vivantes

    def __init__(self, i, j, game):
        # On stocke les informations de la partie
        self.game = game

        self.alive = False
        self.neighbors = set()

        # Initialisation des couleurs
        self.selected_color = Color.WHITE
        self.random_color = [randint(0, 255), randint(0, 255), randint(0, 255)]

        # Définit le Rect qui correspond à la cellule
        self.rect = pygame.Rect((i * self.game.long_cell + self.game.grid, j * self.game.larg_cell + self.game.grid),
                                (self.game.long_cell - self.game.grid, self.game.larg_cell - self.game.grid))

    def consider_alive(self):
        """ Retourne un boolean correspondant au fait que la cellule doit être percue comme vivante """
        return self.alive

    def birth(self, now):
        """ Fais naître la cellule """
        self.alive = True
        # Permet de différencier les causes de la naissance (clic, nouvelle génération)
        if now:
            self.add_checkable()
        else:
            self.add_next_checkable()
        # On affiche l'état de la cellule à l'écran
        pygame.draw.rect(self.game.screen, self.selected_color, self.rect)

    def kill(self):
        """" Tue la cellule"""
        self.alive = False
        # On affiche l'état de la cellule à l'écran
        pygame.draw.rect(self.game.screen, Color.BLACK, self.rect)

    def flip(self):
        """ Modifie l'état de la cellule """
        self.kill() if self.alive else self.birth(True)

    def new_neighbor(self, neighbor):
        """ Ajoute un voisin à la cellule """
        self.neighbors.add(neighbor)

    def count_alive_neighbors(self):
        """ Détermine le nombre de voisins considérés comme vivants """
        counter = 0
        for cell in self.neighbors:
            if cell.consider_alive():
                counter += 1
        return counter

    def pre_update(self):
        """ Détermine le prochain état de la cellule après une nouvelle génération """
        alive_neighbors = self.count_alive_neighbors()
        if (self.alive and 2 <= alive_neighbors <= 3) or (not self.alive and alive_neighbors == 3):
            self.next_alive = True
        else:
            self.next_alive = False

    def update(self):
        """ Applique l'état de la prochaine génération à la cellule """
        # Actualise l'état si il est différent du précédent
        if self.alive and not self.next_alive:
            self.kill()
        elif not self.alive and self.next_alive:
            self.birth(False)

        self.alive = self.next_alive

        # On ajoute la cellule dans l'ensemble de celles susceptibles de changer d'état à la prochaine génération
        if self.alive:
            self.add_next_checkable()

    def actu_color(self):
        """ Met à jour la couleur des cellules """
        self.selected_color = self.colors[self.game.num_color] if self.game.num_color != 1 else self.random_color

    def add_next_checkable(self):
        """ Ajoute la cellule et ses voisins à la liste de celles susceptibles de changer d'état à la prochaine génération """
        self.game.next_checkable.add(self)
        for neighbor in self.neighbors:
            self.game.next_checkable.add(neighbor)

    def add_checkable(self):
        """ Ajoute la cellule et ses voisins à la liste de celles susceptibles de changer d'état """
        self.game.board_checkable.add(self)
        for neighbor in self.neighbors:
            self.game.board_checkable.add(neighbor)


class Corallien_cell(Cell):
    skeleton_color = Color.LIGHT_GREEN  # Couleur d'une cellule dont l'état est squelette

    def __init__(self, i, j, game):
        # On initialise comme les cellules classiques et on ajoute un nouveau booléen sur l'état de la cellule
        Cell.__init__(self, i, j, game)
        self.skelly = False

    # On redéfinit la manière dont la cellule doit être considérée comme vivante 
    def consider_alive(self):
        """ Retourne un booléen correspondant au fait que la cellule doit être percue comme vivante """
        return self.alive or self.skelly

    def birth(self, now):
        """ Fais naître la cellule """
        Cell.birth(self, now)
        self.skelly = False  # On redéfinit la fonction pour actualiser le booléen skelly

    def kill(self):
        """ Tue la cellule """
        Cell.kill(self)
        self.skelly = False  # On redéfinit la fonction pour actualiser le booléen skelly

    def skeleton(self):
        """ Transforme la cellule en squelette """
        self.alive = False
        self.skelly = True
        # On affiche l'état de la cellule à l'écran
        pygame.draw.rect(self.game.screen, self.skeleton_color, self.rect)

    def update(self):
        """ Applique l'état de la prochaine génération à la cellule """
        if self.alive and not self.next_alive:
            self.skeleton()
        elif not self.alive and self.next_alive and not self.skelly:  # On redéfinit la fonction pour vérifier que la cellule n'est pas dejà un squelette
            self.birth(False)
        self.alive = self.next_alive
        if self.alive:
            self.add_next_checkable()


class Project:
    cell_color = Color.GREY
    line_color = Color.LIGHT_RED

    def __init__(self, game, key):
        # On récupère les données du jeu
        self.game = game
        self.make_project = True
        # On récupère le modèle demandé
        self.init_model(key)
        self.init_size()

        self.posx = (self.game.long - self.long) // 2
        self.posy = (self.game.larg - self.larg) // 2

    def init_model(self, key):
        """ Associe à chaque nombre un pattern pré-enregistré """
        if key == pygame.K_1:
            self.glider()
        elif key == pygame.K_2:
            self.slider()
        elif key == pygame.K_3:
            self.diamond()
        elif key == pygame.K_4:
            self.chaos()
        elif key == pygame.K_5:
            self.gosper_glider_gun()
        elif key == pygame.K_6:
            self.drone()
        elif key == pygame.K_7:
            self.rocket()
        elif key == pygame.K_8:
            self.dropper()
        elif key == pygame.K_9:
            self.glider_portal()
        elif key == pygame.K_0:
            self.gol()

    def init_size(self):
        """ Met à jour la taille du pattern """
        self.larg = len(self.scheme)
        self.long = max(sum(self.scheme, [])) + 1

    def display_outlines(self, color):
        """ Affiche un cadre de couleur pour discerner au mieux le pattern et sa taille """
        pygame.draw.line(self.game.screen, color, (self.posx * self.game.long_cell, self.posy * self.game.larg_cell),
                         ((self.posx + self.long) * self.game.long_cell, self.posy * self.game.larg_cell))
        pygame.draw.line(self.game.screen, color, (self.posx * self.game.long_cell, self.posy * self.game.larg_cell),
                         (self.posx * self.game.long_cell, (self.posy + self.larg) * self.game.larg_cell))
        pygame.draw.line(self.game.screen, color,
                         (self.posx * self.game.long_cell, (self.posy + self.larg) * self.game.larg_cell),
                         ((self.posx + self.long) * self.game.long_cell, (self.posy + self.larg) * self.game.larg_cell))
        pygame.draw.line(self.game.screen, color,
                         ((self.posx + self.long) * self.game.long_cell, self.posy * self.game.larg_cell),
                         ((self.posx + self.long) * self.game.long_cell, (self.posy + self.larg) * self.game.larg_cell))

    def display_project(self):
        """ Affiche provisoirement le projet """
        # On vérifie que le project n'est pas encore placé
        if self.make_project:
            for j in range(len(self.scheme)):
                for i in self.scheme[j]:
                    # On affiche chaque cellule concernée d'une couleur particulière
                    pygame.draw.rect(self.game.screen, self.cell_color, self.game.board[self.posy + j][self.posx + i])
            # On affiche le cadre puis on actualise l'écran
            self.display_outlines(self.line_color)
            pygame.display.flip()
            # On remet le quadrillage initial du jeu si il y en a un, sinon on efface les lignes du projet
            self.display_outlines(Game.line_color if self.game.grid else Color.BLACK)

    def restore_background(self):
        """ Affiche le contenu du plateau de jeu dans la zone du projet """
        self.game.print_again_board(self.posx, self.posy, self.long + (1 - self.game.grid),
                                    self.larg + (1 - self.game.grid))

    def dep_up(self):
        """" Déplace le projet d'une cellule vers le haut, si cela est possible """
        self.restore_background()
        self.posy = max(0, self.posy - 1)

    def dep_left(self):
        """" Déplace le projet d'une cellule vers la gauche, si cela est possible """
        self.restore_background()
        self.posx = max(0, self.posx - 1)

    def dep_right(self):
        """" Déplace le projet d'une cellule vers la droite, si cela est possible """
        self.restore_background()
        self.posx = min(self.posx + 1, self.game.long - self.long)

    def dep_down(self):
        """" Déplace le projet d'une cellule vers le bas, si cela est possible """
        self.restore_background()
        self.posy = min(self.posy + 1, self.game.larg - self.larg)

    def dep_turn(self):
        """ Effectue la rotation du projet d'un quart de tour, si cela est possible  """
        self.restore_background()
        # On vérifie que le projet peut être tourner tout en restant sur le plateau
        if self.posx + self.larg <= self.game.long and self.posy + self.long <= self.game.larg:
            self.larg, self.long = self.long, self.larg
            new_scheme = []
            for i in range(self.larg):
                new_l = []
                for j in range(self.long):

                    if i in self.scheme[j]:
                        new_l.append(self.long - j - 1)
                new_scheme.append(new_l)
            # On met a jour le nouveau pattern du projet    
            self.scheme = new_scheme

    def fix(self):
        """ Applique le projet sur le plateau """
        self.make_project = False
        # On fait naître les cellules concernées puis on actualise l'écran
        for j in range(len(self.scheme)):
            for i in self.scheme[j]:
                self.game.board[self.posy + j][self.posx + i].birth(True)
        self.display_outlines(Game.line_color if self.game.grid else Color.BLACK)
        pygame.display.flip()

    # On définit différents objets remarquables dans le mode classique du jeu de la vie
    def glider(self):
        self.scheme = [[2], [0, 2], [1, 2]]

    def double_cube(self):
        self.scheme = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [3, 4, 5], [3, 4, 5], [3, 4, 5]]

    def fumarole(self):
        self.scheme = [[3, 4], [1, 6], [1, 6], [1, 6], [2, 5], [0, 2, 5, 7], [0, 1, 6, 7]]

    def simkin_glider_gun(self):
        self.scheme = [[0, 1, 7, 8], [0, 1, 7, 8], [], [4, 5], [4, 5], [], [], [], [], [22, 23, 25, 26], [21, 27],
                       [21, 28, 31, 32], [21, 22, 23, 27, 31, 32], [26], [], [], [], [20, 21], [20], [21, 22, 23], [23]]

    def gosper_glider_gun(self):
        self.scheme = [[24], [22, 24], [12, 13, 20, 21, 34, 35], [11, 15, 20, 21, 34, 35], [0, 1, 10, 16, 20, 21],
                       [0, 1, 10, 14, 16, 17, 22, 24], [10, 16, 24], [11, 15], [12, 13]]

    def chaos(self):
        self.scheme = [[27], [28], [29], [28], [27], [29, 30, 31], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [0, 1], [2], [2], [3, 4, 5, 6]]

    def rocket(self):
        self.scheme = [[33], [16, 32, 34], [6, 8, 15, 21, 22, 31], [6, 11, 16, 18, 19, 20, 21, 22, 23, 28, 29],
                       [6, 8, 9, 10, 11, 12, 13, 14, 15, 26, 29, 31, 32, 33], [9, 15, 23, 24, 25, 26, 31, 32, 33],
                       [4, 5, 23, 24, 25, 27], [1, 4, 5, 13, 14, 23, 24], [1, 4], [0], [1, 4],
                       [1, 4, 5, 13, 14, 23, 24], [4, 5, 23, 24, 25, 27], [9, 15, 23, 24, 25, 26, 31, 32, 33],
                       [6, 8, 9, 10, 11, 12, 13, 14, 15, 26, 29, 31, 32, 33],
                       [6, 11, 16, 18, 19, 20, 21, 22, 23, 28, 29], [6, 8, 15, 21, 22, 31], [16, 32, 34], [33]]

    def diamond(self):
        self.scheme = [[4, 5, 6, 7], [], [2, 3, 4, 5, 6, 7, 8, 9], [], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [],
                       [2, 3, 4, 5, 6, 7, 8, 9], [], [4, 5, 6, 7]]

    def slider(self):
        self.scheme = [[1, 4], [0], [0, 4], [0, 1, 2, 3]]

    def drone(self):
        self.scheme = [[1, 2, 3], [], [2], [2, 3], [1, 3], [0, 1, 2], [2, 7, 11], [6, 8, 9, 11], [4, 7], [4, 5, 9],
                       [3, 5, 6, 8], [2, 3, 8, 9], [2, 3, 8, 9], [3, 5, 6, 8], [4, 5, 9], [4, 7], [6, 8, 9, 11],
                       [2, 7, 11], [0, 1, 2], [1, 3], [2, 3], [2], [], [1, 2, 3]]

    def glider_portal(self):
        self.scheme = [[20, 21], [20, 21], [], [], [], [], [22, 23], [22], [22], [23], [], [], [], [], [], [], [], [],
                       [32, 35], [33, 34, 35], [0, 1, 40, 41], [0, 1, 40, 41], [6, 7, 8], [6, 9], [], [], [], [], [],
                       [], [], [], [18], [19], [19], [18, 19], [], [], [], [], [20, 21], [20, 21]]

    def dropper(self):
        self.scheme = [[13], [10, 11, 12, 13, 25, 26, 27, 28], [10, 11, 18, 24, 25, 26, 27, 28, 29],
                       [8, 16, 17, 18, 23, 24, 26, 27, 28, 29], [8, 9, 10, 11, 12, 13, 15, 16, 24, 25],
                       [5, 7, 17, 18, 19, 20], [4, 5, 6, 7, 8, 9, 10, 12, 17, 21], [3, 4, 12, 17, 18, 19],
                       [2, 3, 8, 9, 14, 15, 19, 21, 23], [3, 4, 9, 12, 21, 23], [10, 12, 21, 22, 24], [3, 4, 22, 23],
                       [2, 3, 6, 7, 12, 14, 23], [1, 2, 5, 6, 7, 12], [0, 1, 2, 4, 11, 14], [1, 2, 5, 6, 7, 12],
                       [2, 3, 6, 7, 12, 14, 23], [3, 4, 22, 23], [10, 12, 21, 22, 24], [3, 4, 9, 12, 21, 23],
                       [2, 3, 8, 9, 14, 15, 19, 21, 23], [3, 4, 12, 17, 18, 19], [4, 5, 6, 7, 8, 9, 10, 12, 17, 21],
                       [5, 7, 17, 18, 19, 20], [8, 9, 10, 11, 12, 13, 15, 16, 24, 25],
                       [8, 16, 17, 18, 23, 24, 26, 27, 28, 29], [10, 11, 18, 24, 25, 26, 27, 28, 29],
                       [10, 11, 12, 13, 25, 26, 27, 28], [13]]

    def gol(self):
        self.scheme = [
            [1, 2, 3, 4, 8, 12, 16, 18, 19, 20, 21, 22, 28, 29, 30, 33, 34, 35, 36, 37, 42, 48, 49, 50, 52, 53, 54, 55,
             56, 58, 59, 60, 61, 62], [0, 7, 9, 12, 13, 15, 16, 18, 27, 31, 33, 42, 49, 52, 58],
            [0, 6, 10, 12, 14, 16, 18, 27, 31, 33, 42, 49, 52, 58],
            [0, 2, 3, 4, 6, 10, 12, 14, 16, 18, 19, 20, 21, 22, 27, 31, 33, 34, 35, 42, 49, 52, 53, 54, 58, 59, 60, 61,
             62], [0, 4, 6, 7, 8, 9, 10, 12, 16, 18, 27, 31, 33, 42, 49, 52, 58],
            [0, 4, 6, 10, 12, 16, 18, 27, 31, 33, 42, 49, 52, 58],
            [1, 2, 3, 4, 6, 10, 12, 16, 18, 19, 20, 21, 22, 28, 29, 30, 33, 42, 43, 44, 45, 46, 48, 49, 50, 52, 58, 59,
             60, 61, 62]]


class Game:
    line_color = Color.DARK_GREY
    checkable_color = Color.DARK_BLUE

    def __init__(self, length, height, screen, long, larg, auto_init_board=True):
        """ Initialise une partie de GoL

        Args:
            length int: Longueur de la fenêtre
            height int: Largeur de la fenêtre
            screen pygame.Surface: Fenêtre 
            long int: Nombre de cellules horizontales
            larg int: Nombre de cellules verticales
            auto_init_board (bool, optional): Détermine si l'initialisation du plateau se fait directement. Defaults to True.
        """
        # On stocke les données de la partie
        self.screen = screen
        self.length = length
        self.height = height
        self.long = long
        self.larg = larg

        # On détermine la logneur et la largeur d'une cellule
        self.long_cell = self.length / self.long
        self.larg_cell = self.height / self.larg

        self.cursor = 0
        self.cell_type = Cell
        # Détermine  si il est possible de placer une grille sur l'écran
        self.grid = self.long <= 512

        if auto_init_board:
            self.init_board()
            self.init_neighbors()
        else:
            # L'initialisation du tableau se fera plus tard
            self.pre_partial_init()

        # Variables diverses
        self.num_color = 0
        self.board_checkable = set()
        self.next_checkable = set()
        self.print_checkable = False
        self.pressed = {}
        self.project = None
        self.auto_generation = False
        self.auto_generation_speed = 2

    def init_board(self):
        """ Initialise en une seule fois l'ensemble des cellules du plateau """
        self.board = [[self.cell_type(i, j, self) for i in range(self.long)] for j in range(self.larg)]

    def new_cell_board(self, i, j):
        """ Ajoute une cellule au plateau avec une place précise """
        self.board[-1].append(self.cell_type(i, j, self))

    def pre_partial_init(self):
        """ Initialise les variables nécessaires à une initialisation pas à pas """
        self.board_inited = False
        self.neighbors_inited = False
        self.board = []

    def partial_init_board(self):
        """ Ajoute la prochaine cellule du plateau """
        if self.cursor % self.long == 0:
            self.board.append([])
        self.new_cell_board(self.cursor % self.long, self.cursor // self.long)
        self.cursor += 1
        # Vérifie si l'ensemble des cellules du plateau ont été intialisées
        if self.cursor == self.long * self.larg:
            self.board_inited = True
            self.cursor = 0

    def potential_neighbour(self, i, j, dec_i, dec_j):
        """ Essaie d'ajouter un voisin à une cellule sans créer d'erreurs """
        try:
            if i + dec_i >= 0 and j + dec_j >= 0:
                self.board[i][j].new_neighbor(self.board[i + dec_i][j + dec_j])
        except:
            pass

    def partial_init_neighbors(self):
        """ Initialise les voisins de la prochaine cellule """
        i, j = self.cursor // self.long, self.cursor % self.long
        if j * i != 0 and i != self.larg - 1 and j != self.long - 1:  # Cas ou la cellule n'est pas sur un bord du plateau
            self.board[i][j].new_neighbor(self.board[i][j + 1])
            self.board[i][j].new_neighbor(self.board[i + 1][j])
            self.board[i][j].new_neighbor(self.board[i][j - 1])
            self.board[i][j].new_neighbor(self.board[i - 1][j])
            self.board[i][j].new_neighbor(self.board[i + 1][j + 1])
            self.board[i][j].new_neighbor(self.board[i - 1][j + 1])
            self.board[i][j].new_neighbor(self.board[i + 1][j - 1])
            self.board[i][j].new_neighbor(self.board[i - 1][j - 1])
        else:  # Cas ou la cellule est sur un bord, donc avec des voisins qui n'existent pas
            self.potential_neighbour(i, j, 0, 1)
            self.potential_neighbour(i, j, 1, 0)
            self.potential_neighbour(i, j, 0, -1)
            self.potential_neighbour(i, j, -1, 0)
            self.potential_neighbour(i, j, 1, 1)
            self.potential_neighbour(i, j, -1, 1)
            self.potential_neighbour(i, j, 1, -1)
            self.potential_neighbour(i, j, -1, -1)
        self.cursor += 1
        # Vérifie si les voisins ont été initialisé sur l'ensemble des cellules
        if self.cursor == self.long * self.larg:
            self.neighbors_inited = True

    def init_neighbors(self):
        """ Initialise en une seule fois l'ensemble des voisins de chaque cellule du plateau """
        for _ in range(self.larg * self.long):
            self.partial_init_neighbors()

    def new_generation(self):
        """ Actualise le plateau à la prochaine génération """
        for cell in self.board_checkable:
            cell.pre_update()
        self.next_checkable = set()
        for cell in self.board_checkable:
            cell.update()
        for cell in self.board_checkable:
            if cell not in self.next_checkable and self.print_checkable:
                pygame.draw.rect(self.screen, Color.BLACK, cell.rect)
        self.board_checkable = self.next_checkable

    def quadrillage(self):
        """ Affiche le quadrillage du plateau, si cela est possible """
        if self.grid:
            for i in range(1, self.long):
                pygame.draw.line(self.screen, self.line_color, (self.long_cell * i, 0),
                                 (self.long_cell * i, self.height))

            for i in range(1, self.larg):
                pygame.draw.line(self.screen, self.line_color, (0, self.larg_cell * i),
                                 (self.length, self.larg_cell * i))

    def complete_display(self):
        """ Actualise l'affichage en vérifiant si il est demandé d'afficher les cellules potentiellement actives """
        if self.print_checkable:
            for cell in self.board_checkable:
                if not cell.consider_alive():
                    pygame.draw.rect(self.screen, self.checkable_color, cell.rect)
        pygame.display.flip()

    def baby_boom(self):
        """ Fais naître l'ensemble des cellules du plateau """
        for cells in self.board:
            for cell in cells:
                cell.birth(True)

    def clear(self):
        """ Tue l'ensemble des cellules du plateau """
        for cells in self.board:
            for cell in cells:
                cell.kill()

    def new_project(self, key):
        """ Créé un nouveau projet """
        self.project = Project(self, key)

    def flip_color(self):
        """ Change la couleur des cellules vivantes """
        self.num_color += 1
        self.num_color %= len(Cell.colors)
        # On actualise la couleur pour l'ensemble des cellules
        for cells in self.board:
            for cell in cells:
                cell.actu_color()

    def recolor(self, new_color=None):
        """ Modifie la couleur des cellules vivantes """
        self.flip_color()
        for cells in self.board:
            for cell in cells:
                if cell.alive:
                    pygame.draw.rect(self.screen, new_color if new_color != None else cell.selected_color, cell.rect)

    def cell_click(self, check_previous=False, prev=None):
        """ Vérifie si une cellule a été cliquée, et actualise son état si c'est le cas """
        x, y = pygame.mouse.get_pos()
        bloc_x, bloc_y = int(x // self.long_cell), int(y // self.larg_cell)
        if not check_previous or (bloc_y, bloc_x) != prev:
            self.board[int(y // self.larg_cell)][int(x // self.long_cell)].flip()
        return bloc_y, bloc_x

    def erase_checkable(self):
        """ Supprime l'affichage des éléments potentiellement actifs """
        for cell in self.board_checkable:
            if not cell.consider_alive():
                pygame.draw.rect(self.screen, Color.BLACK, cell.rect)

    def print_again_board(self, x, y, width, height):
        """ Affiche à nouveau le plateau, donc l'état des cellules, sur une partie du plateau """
        for cells in self.board[y: y + height]:
            for cell in cells[x: x + width]:
                if cell.alive:
                    pygame.draw.rect(self.screen, cell.selected_color, cell.rect)
                elif cell.consider_alive():
                    pygame.draw.rect(self.screen, Corallien_cell.skeleton_color, cell.rect)
                else:
                    pygame.draw.rect(self.screen, Color.BLACK, cell.rect)

    def manuel(self):
        """ Affiche le manuel  """
        dec_code = 40
        dec_description = dec_code + 450
        police = pygame.font.SysFont("monospace", 30)
        self.screen.blit(police.render("ESPACE", 1, Color.WHITE), (dec_code, 40))
        self.screen.blit(police.render("-> Prochaine génération", 1, Color.LIGHT_GREY), (dec_description, 40))
        self.screen.blit(police.render("S (maintenu)", 1, Color.WHITE), (dec_code, 80))
        self.screen.blit(police.render("-> Générations suivantes (vitesse maximale)", 1, Color.LIGHT_GREY),
                         (dec_description, 80))
        self.screen.blit(police.render("C", 1, Color.WHITE), (dec_code, 120))
        self.screen.blit(police.render("-> Nettoyer le plateau", 1, Color.LIGHT_GREY), (dec_description, 120))
        self.screen.blit(police.render("W", 1, Color.WHITE), (dec_code, 160))
        self.screen.blit(police.render("-> Remplir le plateau", 1, Color.LIGHT_GREY), (dec_description, 160))
        self.screen.blit(police.render("Click de souris", 1, Color.WHITE), (dec_code, 200))
        self.screen.blit(police.render("-> Changer l'état d'une cellule", 1, Color.LIGHT_GREY), (dec_description, 200))
        self.screen.blit(police.render("Click de souris maintenu", 1, Color.WHITE), (dec_code, 240))
        self.screen.blit(police.render("-> Changer l'états de plusieurs cellules", 1, Color.LIGHT_GREY),
                         (dec_description, 240))
        self.screen.blit(police.render("F", 1, Color.WHITE), (dec_code, 280))
        self.screen.blit(police.render("-> Changer de couleur", 1, Color.LIGHT_GREY), (dec_description, 280))
        self.screen.blit(police.render("CHIFFRES (0, ..., 9)", 1, Color.WHITE), (dec_code, 360))
        self.screen.blit(police.render("-> Introduire un pattern pré enregistré", 1, Color.LIGHT_GREY),
                         (dec_description, 360))
        self.screen.blit(police.render("FLECHES", 1, Color.WHITE), (dec_code, 400))
        self.screen.blit(police.render("-> Déplacer le pattern", 1, Color.LIGHT_GREY), (dec_description, 400))
        self.screen.blit(police.render("B", 1, Color.WHITE), (dec_code, 440))
        self.screen.blit(police.render("-> Activer/Désactiver le boost de déplacement du pattern", 1, Color.LIGHT_GREY),
                         (dec_description, 440))
        self.screen.blit(police.render("T", 1, Color.WHITE), (dec_code, 480))
        self.screen.blit(police.render("-> Tourner le pattern", 1, Color.LIGHT_GREY), (dec_description, 480))
        self.screen.blit(police.render("ESPACE", 1, Color.WHITE), (dec_code, 520))
        self.screen.blit(police.render("-> Appliquer le pattern", 1, Color.LIGHT_GREY), (dec_description, 520))
        self.screen.blit(police.render("ECHAP", 1, Color.WHITE), (dec_code, 560))
        self.screen.blit(police.render("-> Supprimer le pattern", 1, Color.LIGHT_GREY), (dec_description, 560))
        self.screen.blit(police.render("A", 1, Color.WHITE), (dec_code, 640))
        self.screen.blit(police.render("-> Activer/Désactiver les générations automatiques", 1, Color.LIGHT_GREY),
                         (dec_description, 640))
        self.screen.blit(police.render("P", 1, Color.WHITE), (dec_code, 680))
        self.screen.blit(police.render("-> Accélérer la cadence des générations", 1, Color.LIGHT_GREY),
                         (dec_description, 680))
        self.screen.blit(police.render("M", 1, Color.WHITE), (dec_code, 720))
        self.screen.blit(police.render("-> Décélérer la cadence des générations", 1, Color.LIGHT_GREY),
                         (dec_description, 720))
        self.screen.blit(police.render("H", 1, Color.WHITE), (dec_code, 800))
        self.screen.blit(police.render("-> Ouvrir le manuel", 1, Color.LIGHT_GREY), (dec_description, 800))
        self.screen.blit(police.render("ECHAP", 1, Color.WHITE), (dec_code, 840))
        self.screen.blit(police.render("-> Retour au menu / Quitter", 1, Color.LIGHT_GREY), (dec_description, 840))


class Cora(Game):

    def __init__(self, length, height, screen, long, larg, auto_init_board=True):
        Game.__init__(self, length, height, screen, long, larg, auto_init_board)
        self.cell_type = Corallien_cell

    def new_generation(self):
        for cell in self.board_checkable:
            cell.pre_update()
        self.next_checkable = set()
        for cell in self.board_checkable:
            cell.update()
        for cell in self.board_checkable:
            if cell not in self.next_checkable and not cell.skelly:  # On redéfinit la fonction pour vérifier que la cellule n'est pas déjà un squelette
                pygame.draw.rect(self.screen, Color.BLACK, cell.rect)
        self.board_checkable = self.next_checkable


class Button:
    # Liste de l'ensemble des boutons
    all_buttons = []
    # On définit les couleurs des boutons
    line_color = Color.LIGHT_GREY
    clicked_color = Color.DARK_GREY_3
    under_mouse_color = Color.DARK_GREY_2
    unclicked_color = Color.DARK_GREY_1

    def __init__(self, label, height, width, screen, pos_center_x, pos_center_y, value):
        """ Initialise un boutton

        Args:
            label string: Nom ou intitlé du boutton
            height int: Hauteur du boutton
            width int: Largeur du boutton
            screen pygame.Surface: Fenêtre dans laquelle il faut l'afficher
            pos_center_x int: Position verticale
            pos_center_y int: Position horizontale
            value : Ce que le boutton permet
        """
        self.all_buttons.append(self)
        self.label = label
        self.height = height
        self.width = width
        self.screen = screen
        self.posx = pos_center_x - self.width / 2
        self.posy = pos_center_y - self.height / 2
        self.rect = pygame.Rect((self.posx, self.posy), (self.width, self.height))
        self.value = value
        self.clicked = False
        self.color = self.unclicked_color

    def display(self):
        """ Affiche un boutton sur la fenêtre """
        police = pygame.font.SysFont("monospace", 30)
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.line(self.screen, self.line_color, (self.posx, self.posy), (self.posx + self.width, self.posy))
        pygame.draw.line(self.screen, self.line_color, (self.posx, self.posy), (self.posx, self.posy + self.height))
        pygame.draw.line(self.screen, self.line_color, (self.posx, self.posy + self.height),
                         (self.posx + self.width, self.posy + self.height))
        pygame.draw.line(self.screen, self.line_color, (self.posx + self.width, self.posy),
                         (self.posx + self.width, self.posy + self.height))
        img_label = police.render(self.label, 1, Color.WHITE)
        screen.blit(img_label, (self.posx + self.width / 2 - img_label.get_width() / 2,
                                self.posy + self.height / 2 - img_label.get_height() / 2))

    def is_clicked(self, x, y):
        """ Vérifie si le boutton a été cliqué et agit en conséquence """
        if self.posx <= x <= self.posx + self.width and self.posy <= y <= self.posy + self.height and not self.clicked:
            self.clicked = True
            self.color = self.clicked_color
            self.action()

    def under_mouse(self, x, y):
        """ Vérifie si la souris est sur le boutton pour changer sa couleur """
        if self.posx <= x <= self.posx + self.width and self.posy <= y <= self.posy + self.height and not self.clicked:
            self.color = self.under_mouse_color
        elif not self.clicked:
            self.color = self.unclicked_color


class Multi_Button(Button):
    info = {}

    def __init__(self, label, height, width, screen, posx, posy, value, key, clicked):
        Button.__init__(self, label, height, width, screen, posx, posy, value)
        self.key = key
        self.clicked = clicked
        # Met à jour la valeur pa défault
        if self.clicked:
            self.info[key] = self.value, self
            self.color = self.clicked_color

    def action(self):
        """ Met à jour les valeurs renvoyées par l'ensemble des multi bouttons après qu'un nouveau a été cliqué """
        self.info.get(self.key)[1].clicked = False
        self.info.get(self.key)[1].color = Button.unclicked_color
        self.info[self.key] = (self.value, self)


class Solo_Button(Button):

    def action(self):
        """ Change la valeur du boutton """
        self.value = not self.value

    def reset(self):
        """ Remet les variables du boutton par défault """
        self.value = not self.value
        self.clicked = False
        self.color = self.unclicked_color


pygame.init()
running = True

# Esthetisme de la fenetre
pygame.display.set_caption("Game of Life")

# Creation de la fenetre
length, height = 1512, 1008
screen = pygame.display.set_mode((length, height))

# Creation des différents bouttons
Multi_Button("PETIT", 70, 180, screen, 2.5 * length / 9 - 40, 600, (36, 24), "dim", True),
Multi_Button("MOYEN", 70, 180, screen, 3.5 * length / 9 - 20, 600, (126, 84), "dim", False),
Multi_Button("GRAND", 70, 180, screen, 4.5 * length / 9, 600, (252, 168), "dim", False),
Multi_Button("ENORME", 70, 180, screen, 5.5 * length / 9 + 20, 600, (504, 336), "dim", False)
Multi_Button("MAX", 70, 180, screen, 6.5 * length / 9 + 40, 600, (1512, 1008), "dim", False)
Multi_Button("CLASSIQUE", 70, 180, screen, 4 * length / 9 - 10, 700, Game, "mode", True)
Multi_Button("CORALLIEN", 70, 180, screen, 5 * length / 9 + 10, 700, Cora, "mode", False)
start = Solo_Button("START", 70, 180, screen, length / 2, 850, False)
quitter = Solo_Button("QUITTER", 70, 180, screen, length / 2, 950, False)
manuel = Solo_Button("MANUEL", 70, 180, screen, length / 2, 950, False)

# Boucle principale
while running:

    intro_game = Game(length, height, screen, 72, 48)

    # Affichage du fond du menu
    screen.fill(0)
    intro_game.quadrillage()
    # Affichage de "GAME OF LIFE"
    intro_game.new_project(pygame.K_0)
    intro_game.project.posy = intro_game.project.posy * 2 // 3
    intro_game.project.fix()
    pygame.display.flip()

    # On reste sur le menu tant que le jeu n'est pas lancé
    while not start.value and running:

        if manuel.value:

            # On remet la valeur par défault de manuel
            manuel.reset()

            # On affiche le manuel
            screen.fill(0)
            intro_game.manuel()

            # On ajoute les intéractions avec le manuel
            while not quitter.value and running:
                x, y = pygame.mouse.get_pos()
                quitter.under_mouse(x, y)
                quitter.display()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        quitter.is_clicked(x, y)
                    elif event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            quitter.value = True
            # On remet la valeur par défault de quitter
            quitter.reset()

            # On rétablit l'affichage du menu quand on sort du manuel
            intro_game.print_again_board(0, 0, intro_game.length, intro_game.height)
            intro_game.quadrillage()

        x, y = pygame.mouse.get_pos()
        # On affiche tous les bouttons (sauf quitter qui sert dans le manuel)
        for button in Button.all_buttons:
            if button != quitter:
                button.under_mouse(x, y)
                button.display()
        pygame.display.flip()

        # On aoute les interactions avec le menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # On vérifie si l'un des boutton est cliqué 
                for button in Button.all_buttons:
                    if button != quitter:
                        button.is_clicked(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    # Une fois sorti du menu on vérifie que le jeu n'est pas fermé
    if running:

        # On créé le plateau demandé par l'utilisateur
        long, larg = Multi_Button.info.get("dim")[0]
        game = Multi_Button.info.get("mode")[0](length, height, screen, long, larg, False)

        # On fait une petite animation permettant de créer en parallèle le plateau (car long pour les plus gros)   
        total = sum(1 / (2 + i) for i in range(100))
        for i in range(100):
            time_checkpoint = time()
            intro_game.new_generation()
            vanishing_color = int(255 - 40 * i ** 0.40)
            intro_game.recolor((vanishing_color, vanishing_color, vanishing_color))
            # On garde les bouttons au premier plan
            for button in Button.all_buttons:
                if button != quit:
                    button.display()
            # On met à jour l'affichage
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            if not running:
                break
            pygame.display.flip()
            # On utilise le temps restant pour créer le tableau puis initialiser les voisins
            for _ in range(int(2 * game.larg * game.long / (2 + i) / total)):
                if not game.board_inited:
                    game.partial_init_board()
                elif not game.neighbors_inited:
                    game.partial_init_neighbors()

        # On vérifie que le plateau est bien chargé    
        while not game.board_inited and running:
            game.partial_init_board()
        while not game.neighbors_inited and running:
            game.partial_init_neighbors()

        # On remet la valeur par défault de start
        start.reset()

        # On affiche le plateau (vide)
        screen.fill(0)
        game.quadrillage()
        pygame.display.flip()

        # On initialise les variables utiles
        play = True
        previous_cell_click = None
        check_point = time()
        timer = 0

    # Boucle principale du jeu sur le plateau
    while running and play:

        # Affiche les générations suivantes a vitesse maximale
        if game.pressed.get(pygame.K_s):
            game.new_generation()

        # Met à jour les cellules cliquées par un clic prolongé
        elif game.pressed.get("Souris") and check_point > time() - timer > 0.2:
            previous_cell_click = game.cell_click(check_previous=True, prev=previous_cell_click)

        # On ajoute les autres intéractions avec le plateau
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quitter le jeu
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Clic sur une cellule
                timer = time()
                game.pressed["Souris"] = True
                game.cell_click()
            elif event.type == pygame.MOUSEBUTTONUP:  # Arrêt d'un clic prolongé
                game.pressed["Souris"] = False
                timer = 0

            elif event.type == pygame.KEYDOWN:  # Touches clavier

                if event.key == pygame.K_b:  # Afficher les cellules utiles pour la prochaine génération
                    game.print_checkable = not game.print_checkable
                    if not game.print_checkable:
                        game.erase_checkable()
                elif event.key == pygame.K_SPACE:  # On affiche la génération suivante
                    game.new_generation()
                elif event.key == pygame.K_c:  # On tue l'ensemble des cellules
                    game.clear()
                elif event.key == pygame.K_w:  # On fait naître l'ensemble des cellules
                    game.baby_boom()
                elif event.key == pygame.K_s:  # On commence la génération rapide
                    game.pressed[event.key] = True
                elif event.key == pygame.K_f:  # On change la couleur des cellules vivantes
                    game.recolor()
                elif event.key == pygame.K_ESCAPE:  # On retourne au menu
                    play = False
                elif event.key == pygame.K_h:  # On affiche le menu
                    # On affiche le menu
                    screen.fill(0)
                    game.manuel()
                    quitter.display()
                    pygame.display.flip()
                    # On ajoute les intéractions avec le menu
                    while not quitter.value and running:
                        x, y = pygame.mouse.get_pos()
                        quitter.under_mouse(x, y)
                        quitter.display()
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = pygame.mouse.get_pos()
                                quitter.is_clicked(x, y)
                            elif event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    quitter.value = True
                    # On rétablit le boutton quitter
                    quitter.reset()
                    # On rétablit l'affichage du plateau
                    game.print_again_board(0, 0, intro_game.length, intro_game.height)
                    game.quadrillage()
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                                   pygame.K_9]:  # On construit un nouveau projet
                    game.new_project(event.key)
                    if game.project.long <= game.long and game.project.larg <= game.larg:  # On vérifie que le projet n'est pas trop grand
                        boost = False

                        # On ajoute les intéractions avec le projet
                        while running and game.project.make_project:
                            if boost:  # On effectue les déplacements rapides si le boost est activé
                                if game.pressed.get(pygame.K_LEFT):
                                    game.project.dep_left()
                                if game.pressed.get(pygame.K_RIGHT):
                                    game.project.dep_right()
                                if game.pressed.get(pygame.K_DOWN):
                                    game.project.dep_down()
                                if game.pressed.get(pygame.K_UP):
                                    game.project.dep_up()

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:  # Quitter le jeu
                                    running = False
                                elif event.type == pygame.KEYDOWN:
                                    # Enregistre les flèches pressées (utile pour le boost)
                                    game.pressed[event.key] = True
                                    if event.key == pygame.K_SPACE:  # Construire le projet
                                        game.project.fix()
                                    elif event.key == pygame.K_ESCAPE:  # Supprimer le projet
                                        game.project.make_project = False
                                        game.project.restore_background()
                                    elif event.key == pygame.K_UP:  # Déplacements
                                        game.project.dep_up()
                                    elif event.key == pygame.K_DOWN:
                                        game.project.dep_down()
                                    elif event.key == pygame.K_RIGHT:
                                        game.project.dep_right()
                                    elif event.key == pygame.K_LEFT:
                                        game.project.dep_left()
                                    elif event.key == pygame.K_t:  # Tourner le projet
                                        game.project.dep_turn()
                                    elif event.key == pygame.K_b:  # Activer / Désactiver le boost
                                        boost = not boost
                                elif event.type == pygame.KEYUP:  # Enlève les flèches pressées
                                    game.pressed[event.key] = False
                            # On affiche le projet
                            game.project.display_project()
                elif event.key == pygame.K_a:
                    game.auto_generation = not game.auto_generation
                    while game.auto_generation and running and play:
                        start_time = time()
                        # On créé une boucle avec un timer
                        while time() - start_time < 1 / game.auto_generation_speed and running and play and game.auto_generation:

                            # On ajoute des intéractions
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:  # Quitter le jeu
                                    running = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:  # Click sur une cellule
                                    game.cell_click()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_a:  # Désactiver l'auto génération
                                        game.auto_generation = False
                                    elif event.key == pygame.K_b:  # Afficher les éléments à calculer
                                        game.print_checkable = not game.print_checkable
                                    elif event.key == pygame.K_m:  # Décélérer la vitesse de génération
                                        game.auto_generation_speed /= 1.5
                                        game.auto_generation_speed = max(game.auto_generation_speed, 0.000001)
                                    elif event.key == pygame.K_p:  # Accélérer la vitesse de génération
                                        game.auto_generation_speed *= 1.5
                                        game.auto_generation_speed = min(game.auto_generation_speed, 1000000)
                                    elif event.key == pygame.K_ESCAPE:  # Désactiver l'auto génération
                                        game.auto_generation = False
                            game.complete_display()
                        # On effectue une génération
                        game.new_generation()
                        # On affiche le résultat
                        game.complete_display()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:  # Vérifie si la touche s n'est plus utilisée
                    game.pressed[event.key] = False

        # On affiche le plateau
        game.complete_display()

# Fin de la boucle principale du jeu
# On arrête maintenant pygame
pygame.quit()

import pygame


class Cell :
    
    def __init__ (self,i,j,game):
        # Recupere les donnes de la partie
        self.game = game
        
        self.alive = False
        
        self.voisins = set()
        
        
        self.rect = pygame.Rect((i*self.game.long_cell, j*self.game.larg_cell), (self.game.long_cell + 1,self.game.larg_cell + 1))
      
    def birth (self) :
        self.alive = True

    def kill (self) :
        self.alive = False
        
    def flip (self) :
        self.alive = not self.alive
        
    def new_voisin (self,voisin) :
        self.voisins.add(voisin)
      
    def pre_update (self) :
        vivants = self.alive_voisins()
        if (self.alive and 2 <= vivants <= 3) or (not self.alive and vivants == 3) :
            self.next_alive = True
        else :
            self.next_alive = False
            
    def update (self) :
        self.alive = self.next_alive
        if self.alive :
            self.add_next_checkable()
        
        
    def alive_voisins (self) :
        compt = 0
        for cell in self.voisins :
            if cell.alive :
                compt += 1
        return compt
    
    def display (self) :
        if self.alive :
            pygame.draw.rect(self.game.screen,[255,255,255],self.rect)
        elif self.game.print_checkable :
            pygame.draw.rect(self.game.screen,[25,55,100],self.rect)
            
    def add_next_checkable (self) :
        self.game.next_checkable.add(self)
        for voisin in self.voisins :
            self.game.next_checkable.add(voisin)
            
    def add_checkable (self) :
        self.game.board_checkable.add(self)
        for voisin in self.voisins :
            self.game.board_checkable.add(voisin)
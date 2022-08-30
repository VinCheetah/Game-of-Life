import pygame
import time
import math

from project import Project
from cell import Cell



####### Commandes ########


# next_gen -> space
# clean -> c // c
# checkable -> b // b

# project -> numbers
# move_project -> arrows
# build_project -> space
# destroy_project -> escape

# auto_gen -> a // q
# speed_up - > p // p
# speed_down -> m // ,


class Game :
    
    long = 36
    larg = 24
    
    def __init__(self, weight, height, screen) :
        
        self.screen = screen
        
        self.weight = weight
        self.height = height
        
        self.long_cell = self.weight / self.long
        self.larg_cell = self.height / self.larg
        
        self.board = [[Cell(i,j,self) for i in range(self.long)] for j in range(self.larg)]
        self.board_checkable = set()  #sum(self.board,[])
        self.init_voisins()
        
        self.print_checkable = False
        
        self.pressed = {}
        
    
    def init_voisins (self) :
        for i in range(self.long - 1) :
            for j in range(self.larg) :
                try :
                    self.board[j][i].new_voisin(self.board[j][i + 1]) 
                except :
                    print(i,j)
                
        for i in range(self.long) :
            for j in range(self.larg - 1) :
                self.board[j][i].new_voisin(self.board[j + 1][i]) 
                
        for i in range(1,self.long) :
            for j in range(self.larg) :
                self.board[j][i].new_voisin(self.board[j][i - 1]) 
                
        for i in range(self.long) :
            for j in range(1,self.larg) :
                self.board[j][i].new_voisin(self.board[j - 1][i]) 
                
        for i in range(self.long - 1) :
            for j in range(self.larg - 1) :
                self.board[j][i].new_voisin(self.board[j + 1][i + 1]) 
                
        for i in range(self.long - 1) :
            for j in range(1,self.larg) :
                self.board[j][i].new_voisin(self.board[j - 1][i + 1]) 
                
        for i in range(1,self.long) :
            for j in range(self.larg - 1) :
                self.board[j][i].new_voisin(self.board[j + 1][i - 1]) 
                
        for i in range(1,self.long) :
            for j in range(1,self.larg) :
                self.board[j][i].new_voisin(self.board[j - 1][i - 1]) 
                
                
                
    def new_generation (self) :
        for cell in self.board_checkable :
            cell.pre_update()
        self.next_checkable = set()
        for cell in self.board_checkable :
            cell.update()
        self.board_checkable = self.next_checkable
                
    def quadrillage (self) :
        for i in range(1,self.long) :
            pygame.draw.line(game.screen, (50,50,50),(self.weight / self.long * i, 0),(self.weight / self.long * i, self.height))
                
        for i in range(1,self.larg) :
            pygame.draw.line(game.screen, (50,50,50),(0,self.height / self.larg * i),(self.weight, self.height / self.larg * i) )       
     
    def display_block (self) :
        for cell in self.board_checkable :
            cell.display()        
    
    def complete_display (self) :
        self.screen.fill(0)            
        self.display_block()
        self.quadrillage()       
        pygame.display.flip()
        
    def clear (self) :
        for cell in self.board_checkable :
            cell.kill()
            
    
    
    
pygame.init()

# Esthetisme de la fenetre
pygame.display.set_caption("Game of Life")
pygame.display.set_icon(pygame.image.load("gof_icon.png"))

# Dimensions de la fenetre
weight, height = 1200, 800

screen = pygame.display.set_mode((weight, height))


screen.fill(0)

game = Game(weight,height,screen)

game.quadrillage()
pygame.display.flip()


running = True
pause = True



while running :
    
    while pause and running :
        
        if game.pressed.get(pygame.K_s) :
            game.new_generation()
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                x, y = event.pos
                game.board[int(y//game.larg_cell)][int(x//game.long_cell)].flip()
                game.board[int(y//game.larg_cell)][int(x//game.long_cell)].add_checkable()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_a :
                    pause = not pause
                elif event.key == pygame.K_b :
                    game.print_checkable = not game.print_checkable
                elif event.key == pygame.K_SPACE :
                    game.new_generation()
                elif event.key == pygame.K_c :
                    game.clear()
                elif event.key == pygame.K_s :
                    game.pressed[event.key] = True
                    
                elif event.key in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9] :
                    
                    project = Project (game,event.key)
                    if project.long <= game.long and project.larg <= game.larg :
                        
                        boost = False
                        while running and project.go :
                            
                            if boost :
                                if game.pressed.get(pygame.K_LEFT) :
                                    project.dep_left()
                                if game.pressed.get(pygame.K_RIGHT) :
                                    project.dep_right()
                                if game.pressed.get(pygame.K_DOWN) :
                                    project.dep_down()
                                if game.pressed.get(pygame.K_UP) :
                                    project.dep_up()
                            
                            for event in pygame.event.get() :
                                if event.type == pygame.QUIT :
                                    running = False 
                                    
                                elif event.type == pygame.KEYDOWN :
                                    game.pressed[event.key] = True
                                    
                                    if event.key == pygame.K_SPACE :
                                        project.fix()
                                    elif event.key == pygame.K_ESCAPE :
                                        project.go = False
                                    elif event.key == pygame.K_UP :
                                        project.dep_up()
                                    elif event.key == pygame.K_DOWN :
                                        project.dep_down()
                                    elif event.key == pygame.K_RIGHT :
                                        project.dep_right()
                                    elif event.key == pygame.K_LEFT :
                                        project.dep_left()
                                    elif event.key == pygame.K_t :
                                        project.dep_turn()
                                    elif event.key == pygame.K_b :
                                        boost = not boost
                                elif event.type == pygame.KEYUP :
                                    game.pressed[event.key] = False
                                    
                            game.screen.fill(0)            
                            game.display_block()
                            game.quadrillage()    
                            project.display_project()
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_s :
                    game.pressed[event.key] = False
                
                    
                
        game.complete_display()
    speed = 20       
    while not pause and running :
        start_time = time.time ()
        
        while time.time() - start_time < 1/ math.sqrt(speed) :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    running = False
                    pause = False
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = event.pos
                    game.board[int(y//game.larg_cell)][int(x//game.long_cell)].flip()
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_a :
                        pause = not pause
                    elif event.key == pygame.K_b :
                        game.print_checkable = not game.print_checkable
                    elif event.key == pygame.K_m :
                        speed = max(1,speed - 1)
                    elif event.key == pygame.K_p :
                        speed += 1
            game.complete_display()            
                
        game.new_generation()
                        
        game.complete_display()
            
pygame.quit()

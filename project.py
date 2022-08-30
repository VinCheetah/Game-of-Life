import pygame

class Project :
    
    col = 50,50,50
    color = 150,50,50
    
    def __init__ (self,game,model) :
        
        self.game = game
        self.model = model
        self.init_model()
        self.go = True
        
        self.posx = (self.game.long - self.long) // 2
        self.posy = (self.game.larg - self.larg) // 2
        
    def display_project (self) :
        for j in range(len(self.scheme)) :
            for i in self.scheme[j] :
                pygame.draw.rect(self.game.screen,self.col,self.game.board[self.posy + j][self.posx + i])
        pygame.draw.line(self.game.screen,self.color,(self.posx * self.game.long_cell, self.posy * self.game.larg_cell),((self.posx + self.long) * self.game.long_cell, self.posy * self.game.larg_cell))
        pygame.draw.line(self.game.screen,self.color,(self.posx * self.game.long_cell, self.posy * self.game.larg_cell),(self.posx * self.game.long_cell, (self.posy + self.larg)* self.game.larg_cell))
        pygame.draw.line(self.game.screen,self.color,(self.posx * self.game.long_cell, (self.posy + self.larg)* self.game.larg_cell),((self.posx + self.long) * self.game.long_cell, (self.posy + self.larg)* self.game.larg_cell))
        pygame.draw.line(self.game.screen,self.color,((self.posx + self.long) * self.game.long_cell, self.posy * self.game.larg_cell),((self.posx + self.long) * self.game.long_cell, (self.posy + self.larg)* self.game.larg_cell))

        pygame.display.flip()
        
    def init_size (self) :
        self.larg = len(self.scheme)
        self.long = max(sum(self.scheme,[])) + 1
        
    def init_model (self) :
        if self.model == pygame.K_1 :
            self.glider()
        elif self.model == pygame.K_2 :
            self.slider()
        elif self.model == pygame.K_3 :
            self.diamond()
        elif self.model == pygame.K_4 :
            self.simkin_glider_gun()
        elif self.model == pygame.K_5 :
            self.gosper_glider_gun()
        elif self.model == pygame.K_6 :
            self.drone()
        elif self.model == pygame.K_7 :
            self.rocket()
        elif self.model == pygame.K_8 : 
            self.dropper()
        elif self.model == pygame.K_9 :
            self.glider_portal()
        self.init_size()
            
            
    def glider (self) :
        self.scheme = [[2],[0,2],[1,2]]
        
    def double_cube (self) :
        self.scheme = [[0,1,2],[0,1,2],[0,1,2],[3,4,5],[3,4,5],[3,4,5]]
        
        
    def fumarole (self) :
        self.scheme = [[3,4],[1,6],[1,6],[1,6],[2,5],[0,2,5,7],[0,1,6,7]]
        
    def simkin_glider_gun (self) :
        self.scheme = [[0,1,7,8],[0,1,7,8],[],[4,5],[4,5],[],[],[],[],[22,23,25,26],[21,27],[21,28,31,32],[21,22,23,27,31,32],[26],[],[],[],[20,21],[20],[21,22,23],[23]]
        
    def gosper_glider_gun (self) :
        self.scheme = [[24],[22,24],[12,13,20,21,34,35],[11,15,20,21,34,35],[0,1,10,16,20,21],[0,1,10,14,16,17,22,24],[10,16,24],[11,15],[12,13]]
        
    def chaos (self) :
        self.scheme = [[27],[28],[29],[28],[27],[29,30,31],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[0,1],[2],[2],[3,4,5,6]]
        
    def rocket (self) :
        self.scheme = [[33],[16,32,34],[6,8,15,21,22,31],[6,11,16,18,19,20,21,22,23,28,29],[6,8,9,10,11,12,13,14,15,26,29,31,32,33],[9,15,23,24,25,26,31,32,33],[4,5,23,24,25,27],[1,4,5,13,14,23,24],[1,4],[0],[1,4],[1,4,5,13,14,23,24],[4,5,23,24,25,27],[9,15,23,24,25,26,31,32,33],[6,8,9,10,11,12,13,14,15,26,29,31,32,33],[6,11,16,18,19,20,21,22,23,28,29],[6,8,15,21,22,31],[16,32,34],[33]]
        
    def diamond (self) :
        self.scheme = [[4,5,6,7],[],[2,3,4,5,6,7,8,9],[],[0,1,2,3,4,5,6,7,8,9,10,11],[],[2,3,4,5,6,7,8,9],[],[4,5,6,7]]
        
    def slider (self) :
        self.scheme = [[1,4],[0],[0,4],[0,1,2,3]]
        
    def drone (self) :
        self.scheme = [[1,2,3],[],[2],[2,3],[1,3],[0,1,2],[2,7,11],[6,8,9,11],[4,7],[4,5,9],[3,5,6,8],[2,3,8,9],[2,3,8,9],[3,5,6,8],[4,5,9],[4,7],[6,8,9,11],[2,7,11],[0,1,2],[1,3],[2,3],[2],[],[1,2,3]]
    
    def glider_portal (self) :
        self.scheme = [[20,21],[20,21],[],[],[],[],[22,23],[22],[22],[23],[],[],[],[],[],[],[],[],[32,35],[33,34,35],[0,1,40,41],[0,1,40,41],[6,7,8],[6,9],[],[],[],[],[],[],[],[],[18],[19],[19],[18,19],[],[],[],[],[20,21],[20,21]]
    
    def dropper (self) :
        self.scheme = [[13],[10,11,12,13,25,26,27,28],[10,11,18,24,25,26,27,28,29],[8,16,17,18,23,24,26,27,28,29],[8,9,10,11,12,13,15,16,24,25],[5,7,17,18,19,20],[4,5,6,7,8,9,10,12,17,21],[3,4,12,17,18,19],[2,3,8,9,14,15,19,21,23],[3,4,9,12,21,23],[10,12,21,22,24],[3,4,22,23],[2,3,6,7,12,14,23],[1,2,5,6,7,12],[0,1,2,4,11,14],[1,2,5,6,7,12],[2,3,6,7,12,14,23],[3,4,22,23],[10,12,21,22,24],[3,4,9,12,21,23],[2,3,8,9,14,15,19,21,23],[3,4,12,17,18,19],[4,5,6,7,8,9,10,12,17,21],[5,7,17,18,19,20],[8,9,10,11,12,13,15,16,24,25],[8,16,17,18,23,24,26,27,28,29],[10,11,18,24,25,26,27,28,29],[10,11,12,13,25,26,27,28],[13]]
    
    def fix (self) :
        self.go = False
        for j in range(len(self.scheme)) :
            for i in self.scheme[j] :
                self.game.board[self.posy + j][self.posx + i].birth()   
                self.game.board[self.posy + j][self.posx + i].add_checkable()
                
    def dep_up (self) :
        self.posy = max(0, self.posy - 1)
        
    def dep_left (self) :
        self.posx = max(0, self.posx - 1)
        
    def dep_right (self) :
        self.posx = min(self.posx + 1, self.game.long - self.long)
        
    def dep_down (self) :
        self.posy = min(self.posy + 1, self.game.larg - self.larg)
        
    def dep_turn (self) :
        if self.posx + self.larg <= self.game.long and self.posy + self.long <= self.game.larg :
            self.larg, self.long = self.long, self.larg
            new_scheme = []
            for i in range(self.larg) :
                new_l = []
                for j in range(self.long) :
                    
                    if i in self.scheme[j] :
                        new_l.append(self.long - j - 1)
                new_scheme.append(new_l)
                    
            self.scheme = new_scheme
                    
                    
        
        
        
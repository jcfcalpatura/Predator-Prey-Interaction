
class Game():
    cell_size = 8

    def __init__(self):
        #0a --> Empty
        #0b --> cell becomes empty after predator attack
        #1 --> Prey
        #2a --> Predator
        #2b --> Predator that just ate
        
        #rates of birth, death of prey (P) and predator(H)
        self.bP = 0.6
        self.dP = 0.6
        self.bH = 0.6
        self.dH = 0.2

        # Initialize self.rows, self.cols and set-up a list of lists
        self.cols = width / Game.cell_size
        self.rows = height / Game.cell_size
        # dispersion boardv
        self.board = [[0] * self.rows for _ in range(self.cols)]
        # Call function to fill array with random values
        self.init()

    def init(self):
        #initialize all empty cells
        Q = ['0a','1','2a']
        for i in range(self.cols):
            for j in range(self.rows):
                #self.board[i][j] = Q[1]
                self.board[i][j] = Q[int(random(0,2))]
        for i in range(self.cols):
            for j in range(self.rows):
                if self.board[i][j] == '0a':
                    self.board[i][j] = Q[int(random(1,3))]             

    # The process of creating the new generation
    def generate(self):

        next = self.board
        # Loop through every spot in our 2D array
        nPT2 = 0
        for x in range(self.cols):
            for y in range(self.rows):
                vn = self.getVN(x,y)
                m = self.getMoore(x,y)
                cell = self.board[x][y]
        
                nPT = 0
                nPR = 0
                for i in vn:#count surrounding states
                    if i == '1':
                        nPR +=1
                    elif i == '2a':
                        nPT +=1
                #attack phase
                if (cell== '1'):#if prey
                    prob = (1-self.dP)**(nPT) #calculate survival probability
                    if (random(0,1) <= prob):#remain alive
                        cell = '1'
                    else:#die due to predation
                        cell = '0b'
                if (cell == '2a'):
                    prob = (1-self.dP)**(nPR)
                    if (random(0,1) <= prob):#failed hunt
                        cell = '2a'
                    else:#successful hunt
                        cell = '2b'
                        nPT2 +=1

                #reproduction phase
                if cell == '2a' or cell == '2b':
                    if (random(0,1) <= self.dH):
                        cell = '0a'
                    else:
                        cell = '2a'
                if cell == '0a':#empty cells
                    if (nPT > 0 or nPR==0):#stay empty
                        cell = '0a'
                    else:#become prey
                        prob = (1-self.bP)**(nPR)
                        if (random(0,1) <= prob):
                            cell = '1'
                if cell == '0b': #eaten preys
                    prob = (1-self.bH)**(nPT2)
                    if (random(0,1) <= prob):#remain empty
                        cell = '0a'
                    else:#become predator
                        cell = '2a'
                #movement
                #north
                north,east,south,west = [],[],[],[]
                north.extend([0,1,2,3,4,6,7,8])
                east.extend([4,8,9,12,13,17,18,23])
                west.extend([0,5,6,10,11,14,15,19])
                south.extend([15,16,17,19,20,21,22,23])
                #format 
                #  0  1  2  3  4
                #  5  6  7  8  9
                # 10 11  X 12 13
                # 14 15 16 17 18
                # 19 20 21 22 23
                preyN,predN = 0,0
                preyE,predE = 0,0
                preyS,predS = 0,0
                preyW,predW = 0,0
                #predator and prey counting in Moore neighborhood
                for i in north:
                    if m[i] == '1':
                        preyN +=1
                    elif m[i] == '2a':
                        predN +=1
                for i in east:
                    if m[i] == '1':
                        preyE +=1
                    elif m[i] == '2a':
                        predE +=1
                for i in west:
                    if m[i] == '1':
                        preyW +=1
                    elif m[i] == '2a':
                        predW +=1                        
                for i in south:
                    if m[i] == '1':
                        preyS +=1
                    elif m[i] == '2a':
                        predS +=1
                #movement
                opt = []
                for i in range(-1,2,1):#get options for next path
                    for j in range(-1,2,1):
                        nx = (x+i+self.cols) % self.cols
                        ny = (y + j + self.rows)% self.rows
                        if (abs(i+j)/1 == 1):
                            opt.append([nx,ny])
                        #0 --> W, 1--> N 2--> S 3 --> E
                #print(x,y,opt)
                #print(opt[1])
                
                if cell == '2a':#if predator, seek prey
                    var = {preyN: "preyN", preyE: "preyE", preyS:"preyS", preyW:"preyW"}
                    dir = var.get(max(var))
                    
                    if dir == "preyN":
                        if next[opt[1][0]][opt[1][1]] == '0a':
                            next[opt[1][0]][opt[1][1]] = cell
                            cell = '0a'
                    if dir == "preyS":
                        if next[opt[2][0]][opt[2][1]] == '0a':
                            next[opt[2][0]][opt[2][1]] = cell
                            cell = '0a'
                    if dir == "preyE":
                        if next[opt[3][0]][opt[3][1]] == '0a':
                            next[opt[3][0]][opt[3][1]] = cell
                            cell = '0a'
                    if dir == "preyW":
                        if next[opt[0][0]][opt[0][1]] == '0a':
                            next[opt[0][0]][opt[0][1]] = cell
                            cell = '0a'
                predTot = predN + predS + predW +predE
                if cell == '1' and predTot > 0:
                    var = {predN: "predN", predE: "predE", predS:"predS", predW:"predW"}
                    dir = var.get(min(var))
                    if dir == "predN":
                        if next[opt[1][0]][opt[1][1]] == '0a':
                            next[opt[1][0]][opt[1][1]] = cell
                            cell = '0a'
                    if dir == "predS":
                        if next[opt[2][0]][opt[2][1]] == '0a':
                            next[opt[2][0]][opt[2][1]] = cell
                            cell = '0a'
                    if dir == "predE":
                        if next[opt[3][0]][opt[3][1]] == '0a':
                            next[opt[3][0]][opt[3][1]] = cell
                            cell = '0a'
                    if dir == "predW":
                        if next[opt[0][0]][opt[0][1]] == '0a':
                            next[opt[0][0]][opt[0][1]] = cell
                            cell = '0a'
                            
                #self.board[x][y] = cell
                next[x][y] = cell
        # next state
        self.board = next
        

        #savetable
        preyCount = 0
        predCount = 0
        emptyCount = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == '1':
                    preyCount+=1
                elif self.board[i][j] == '2a' or self.board[i][j] == '2b':
                    predCount +=1
                else:
                    emptyCount +=1
        return preyCount,predCount,emptyCount
        
    def getVN(self,x,y):
        #getting Von Neumann neighborhood
        vn = []
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                nx = (x+i+self.cols) % self.cols
                ny = (y + j + self.rows)% self.rows
                if abs(i+j)/1 == 1:
                    #print(x,y,nx,ny)
                    vn.append(self.board[nx][ny])
        return vn
    def getMoore(self,x,y):#get Moore neighborhood, r = 2
        m = []# 0 --> WALL
        #format 
        #  0  1  2  3  4
        #  5  6  7  8  9
        # 10 11  X 12 13
        # 14 15 16 17 18
        # 19 20 21 22 23
        for i in range(-2,3,1):
            for j in range(-2,3,1):
                nx = (x+i+self.cols) % self.cols
                ny = (y + j + self.rows)% self.rows
                if (ny != y or nx != x):
                    m.append(self.board[nx][ny])
        return m
    
    
    #red for pred, green for prey, white for empty
    def display(self):
        background(255)
        for i in range(self.cols):
            for j in range(self.rows):
                if (self.board[i][j] == '1'):
                   fill(0,255,0,255)
                elif (self.board[i][j] == '2a' or self.board[i][j] == '2b'):
                    fill(255,0,0,255)
                else:
                    fill(255)
                stroke(0)
                rect(i * Game.cell_size,
                     j * Game.cell_size,
                     Game.cell_size,
                     Game.cell_size)

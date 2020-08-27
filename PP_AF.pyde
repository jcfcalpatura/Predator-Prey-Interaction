from game import Game
def setup():
    global game, output, outList,q
    size(400, 400)
    game = Game()
    outList = []
    q = 0

def draw():
    global q, outList
    background(255)
    
    #comment out to record data
    game.generate()
    
    #uncomment to record data
    #a = game.generate()
    #record(a)
    
    game.display()

# reset board when mouse is pressed
def mousePressed():
    game.init()
    global q
    q = 0
    
def record(a):
    global q, outList
    if q < 400 and q > 0 :
        outList.append(str(a))
    if q == 10:
        print("SAVED")
        saveStrings("file.txt", outList)
    q+=1 
    print(q)

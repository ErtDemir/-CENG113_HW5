"""
Student Name: Ertuğrul Demir
Student ID  : 260201059
"""
import numpy

class Game():
    def __init__(self,map_width,map_height,init_time, action_cost):
        # The Game initializes map parameters.
        self.mapwidth = map_width
        self.mapheight = map_height
        # The Game initializes its map with all empty squares.
        self.map = [['empty' for col in range(map_width)] for row in range(map_height)]
        # The Game creates its player object.
        self.player = Player()
        # The Game creates its time object.
        self.time = Time(0,init_time, action_cost)
        # The Game initializes the player icon.
        self.picon = person
        # The Game sets the continue state to true (still has time)
        self.cont = True

        # The Game sets the safe state to false (still not in shelter)
        self.safe = False
        # The Game initializes the list of squares that constitutes the shelter 
        self.score_map = []
        # The Game randomly inserts wood, dirt or water on the map.
        self.generate_map()
        # The Game prints the current status on the screen.
        self.update_screen()
   
    def generate_map(self):
        # For each square, put wood with probability of 0.3, put dirt with probability of 0.3,
        # put water with probability of 0.2 or leave empty with probability of 0.2. You have
        # to use 'numpy.random.randint' function.
        ratios = {"wood " : [0,1,2] , "dirt " : [3,4,5] , "water" : [6,7] , "empty" : [8,9]}
        for col in range(len(self.map)):
            for row in range(len(self.map)):
                a = numpy.random.randint(10, size = 1)
                if a[0] in ratios["wood "] :
                    self.map[col][row] = "wood "
                elif a[0] in ratios["dirt "] :
                    self.map[col][row] = "dirt "
                elif a[0] in ratios["water"] :
                    self.map[col][row] = "water"

    def show_controls(self):        
        print()
        print("**************************** Game Control ****************************")
        print("w: up          s: down        a: left        d: rigth")
        print("1: put brick   2: put dirt    3: put plank   4: put water  5: put wood")
        print("q: pick        e: make plank  r: make brick  o: exit game")
        print("plank: 2 woods brick: 2 dirt 1 water")
        print("plank: 2 pts   brick: 3 pts   enclosed square: 3 pts")
        print("**********************************************************************")
        print()
    def show_map(self):
        ppx = self.player.pos[0]
        ppy = self.player.pos[1]
        print()
        for row in range(MAP_HEIGHT):
            color_row = [COLORS[self.map[row][c]] for c in range(MAP_WIDTH)]
            if row == ppy:
                color_row[ppx] = color_row[ppx].replace('   ',' '+self.picon+' ')
            print(''.join(color_row))    
            
    def update_screen(self):
        # Re-print controls, map, inventory and time. This function has to be
        # called at the end of each successfully executed action.
        self.show_map()
        self.show_controls()
        self.time.show_time()
        self.player.show_inventory()


    def _flood_fill(self,wmf,ppx,ppy,source,target,conn8=True):
            if wmf[ppy,ppx]!=source:
                return
            wmf[ppy,ppx] = target
            if ppy>0: self._flood_fill(wmf,ppx,ppy-1,source,target,conn8)
            if ppy<wmf.shape[0]-1: self._flood_fill(wmf,ppx,ppy+1,source,target,conn8)
            if ppx>0: self._flood_fill(wmf,ppx-1,ppy,source,target,conn8)
            if ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy,source,target,conn8)
            if conn8:
                if ppy>0 and ppx>0: self._flood_fill(wmf,ppx-1,ppy-1,source,target,conn8)
                if ppy>0 and ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy-1,source,target,conn8)
                if ppy<wmf.shape[0]-1 and ppx>0: self._flood_fill(wmf,ppx-1,ppy+1,source,target),conn8
                if ppy<wmf.shape[0]-1 and ppx<wmf.shape[1]-1: self._flood_fill(wmf,ppx+1,ppy+1,source,target,conn8)
    def check_safety(self):
        # This function checks if the player is in a shelter. It should be called
        # at the end of each successfully executed action to check if the game 
        # has finished. You do not have to do anything here.
        wall_map = numpy.zeros((game.mapwidth+2,game.mapheight+2)).astype(int)
        wall_map_bool = [numpy.in1d(row, ['brick','plank']) for row in game.map]
        wall_map[1:-1,1:-1] = numpy.array(wall_map_bool).astype(int)
        label = 2
        while((wall_map == 1).any()):
            py = numpy.where(wall_map==1)[0][0]
            px = numpy.where(wall_map==1)[1][0]
            self._flood_fill(wall_map, px, py, 1, label, False)
            label += 1
        ppx = game.player.pos[0]+1
        ppy = game.player.pos[1]+1
        if not wall_map[ppy,ppx]:
            for wall in range(2,label):
                wall_map_fill = (wall_map == wall).astype(int) 
                self._flood_fill(wall_map_fill,ppx,ppy,0,label)
                edges = [wall_map_fill[0,:],wall_map_fill[-1,:], wall_map_fill[:,0],wall_map_fill[:,-1]]
                if label not in numpy.array(edges):
                    self.safe = True
                    self.score_map = wall_map_fill[1:-1,1:-1]
                    self.picon = happy
                    break
    def calc_score(self):
        final_map = (numpy.array(self.map) == 'brick').astype(int) + self.score_map
        unique, counts = numpy.unique(final_map, return_counts=True)
        score = counts[-1]*3 + counts[-2]*3 + counts[-3]*2 #area*3+brick*3+plank*2
        return score
    def move_player(self,direction):
        # Move the player with respect to the instructions if possible, otherwise
        # print "I can not go up", "I can not go down", etc.
        if self.player.pos[1] == 0 and direction == "w":
            print("I can not go up")
            return False
        elif self.player.pos[1] == (self.mapheight-1) and direction == "s":
            print("I can not go down")
            return False
        elif self.player.pos[0] == 0 and direction == "a":
            print("I can not go left")
            return False
        elif self.player.pos[0] == (self.mapwidth-1) and direction == "d":
            print("I can not go right")
            return False
        self.player.move(direction)
        self.time.spend()

    def pick_item(self):
        # Pick item using the player object's pick method and update the map if 
        # there is an item to pick, otherwise print "There is nothing to pick!".
        if self.map[self.player.pos[1]][self.player.pos[0]] != "empty" :
            self.player.pick(self.map[self.player.pos[1]][self.player.pos[0]])
            self.map[self.player.pos[1]][self.player.pos[0]] = "empty"

            self.time.spend()
            return True
        print("There is nothing to pick!")
        return False
    def put_item(self,item):
        # Put the given item using the player object's put method if the current
        # square is empty, otherwise print ""There is nowhere to put!". If the
        # player scan successfully put the item, update the map.
        if self.map[self.player.pos[1]][self.player.pos[0]] == "empty":
            if self.player.put(item) == True :
                self.map[self.player.pos[1]][self.player.pos[0]] = item
                self.time.spend()
        else:
            print("There is nowhere to put!")



    def make(self,item):
        # Make the given item using the player object's corresponding method. If
        # the player can not make the item, print "Not enough material!".
        if item == "brick" and self.player.inventory["dirt "] >= 2 and self.player.inventory["water"] >= 1 :
            self.player.make_brick()
            self.time.spend()
        elif item == "plank" and self.player.inventory["wood "] >= 2 :
            self.player.make_plank()
            self.time.spend()
        print("Not enough material!")
        return False

class Player():
    def __init__(self):
        # Initialize the player position at the top left corner
        self.pos = [0,0]
        # Initialize the inventory as empty
        self.inventory = {'wood ':0,'dirt ':0,'water':0,'plank':0,'brick':0}
    def move(self, direction):
        # Update the player position with respect to move direction.
        if direction == "w":
            self.pos[1] -= 1
        elif direction == "s":
            self.pos[1] += 1
        elif direction == "d":
            self.pos[0] += 1
        elif direction == "a":
            self.pos[0] -= 1

    def pick(self, item):
        # Pick and update the player inventory with respect to the item.
        self.inventory[item] += 1

    def put(self,item):
        # Put and update the player inventory with respect to the item, if the
        # player has one or more of that item in the inventory. Return true if
        # successfully put, otherwise false.
        if self.inventory[item] != 0:
            self.inventory[item] -= 1
            return True
        return False

    def make_plank(self):
        # Make plank and update the player inventory with respect to the action,
        # if the player has enough materials. Return true if plank is successfully 
        # made, otherwise false.
        if self.inventory["wood "] >= 2:
            self.inventory["plank"] += 1
            self.inventory["wood "] -= 2
            return True
        return False
    def make_brick(self):
        # Make plank and update the player inventory with respect to the action,
        # if the player has enough materials. Return true if plank is successfully 
        # made, otherwise false.
        if self.inventory["dirt "] >= 2 and self.inventory["water"] >= 1:
            self.inventory["brick"] += 1
            self.inventory["water"] -= 1
            self.inventory["dirt "] -= 2
            return True
        return False
    def show_inventory(self):
        print()
        c = 1
        for key in sorted(self.inventory.keys()):
            print("{}. {}\t: {}".format(c, key, (COLORS[key]+" ")*self.inventory[key]))
            c += 1
        print()   

class Time():
    def __init__(self, mins, hours, action_cost):
        self.mins = mins
        self.hours = hours
        self.action_cost = action_cost
    def spend(self):
        # Spend the action cost and update mins and/or hours. If the time is
        # up return False, otherwise True.
        if self.mins == 0 and self.hours == 0 :
            return False
        if self.mins == 0 :
            self.hours -= 1
            self.mins = 45
            return True
        else:
            self.mins -= 15
            return True
    def show_time(self):
        print("{} hours {} minutes left!!!".format(self.hours, self.mins))


MAP_WIDTH = 10
MAP_HEIGHT = 10
ACTION_COST = 15                  #minutes
INIT_TIME = 16                  #hours
person = u"\u2689"
happy = u"\u263b"
COLORS = {'empty':'\033[40m   \033[0m', 'wood ':'\033[42m   \033[0m',
          'dirt ':'\033[47m   \033[0m', 'water':'\033[46m   \033[0m',
          'plank':'\033[43m   \033[0m', 'brick':'\033[41m   \033[0m'}
    
moves = {"w":"up", "s":"down", "a":"left", "d":"right"}
items = {"1":"brick", "2":"dirt ", "3":"plank", "4":"water", "5":"wood "}
products = {"e":"plank", "r":"brick"}

# A Game class is instantiated each time a new game begins.
game = Game(MAP_WIDTH, MAP_HEIGHT, INIT_TIME, ACTION_COST)

out = False
while game.cont and not game.safe:
    ################## THIS PART CAUSES AN INFINITE LOOP!!! ##################
    # Implement the game play. Take the instructions from the user and execute
    # them.

    if game.map == [['empty' for col in range(game.mapwidth)] for row in range(game.mapheight)]:
        game.generate_map()
    action = input("Enter Your Action:  ")

    if action in "wasd":
        game.move_player(action)

    elif action in "12345":
        game.put_item(items[action])

    elif action is "q":
        game.pick_item()

    elif action in "er":
        game.make(products[action])

    elif action is "o":
        out = True
        break

    game.update_screen()

    game.check_safety()
    if game.time.mins == 0 and game.time.hours == 0 and game.safe == False :
        game.cont = False



if game.safe:
    print("Congratulations! You are safe!!!")
    print("Your score is {}.".format(game.calc_score()))
elif out:
    print("Bye!")
else:
    print("Too late! They are coming!!!")

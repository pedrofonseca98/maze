# Get started with interactive Python
import turtle
import time
import queue
import timeit

#Inicia o GUI
wn = turtle.Screen()
wn.reset()
wn.setup(850,700)
wn.bgcolor("black")

#Paredes
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
#Square finish
class Finish(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)
#Player square
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("cyan")
        self.penup()
        self.speed(0)

    def go_up(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 22

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            return True;

        return False;

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 22

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            return True;

        return False;

    def go_right(self):
        move_to_x = player.xcor() + 22
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            return True;

        return False;

    def go_left(self):
        move_to_x = player.xcor() - 22
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            return True;

        return False;

#create Levels list
levels = [""]

maze_array = []
#Ler do ficheiro linha a linha até ao final
#Cada linha é um espaço de memoria diferente no array (maze_array)
with open('maze.txt') as my_file:
    for line in my_file:
        line = line.rstrip()
        maze_array.append(line)
#quarda no array levels
levels.append(maze_array)

print("\nrendering maze...\n")

#making the maze in GUI
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the Character at each x,y coordinate
            #NOTE the order of the y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -320 + (x * 22)
            screen_y = 200 - (y * 22)

            #Check if it is an X (representing a wall)
            if character == "X":
                #Se for a primeira linha mete a preto para nao se ver
                if screen_y == 200:
                    pen.color("black")
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    walls.append((screen_x,screen_y))
                    #desenha as paredes normais
                else:
                    pen.color("white")
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    walls.append((screen_x,screen_y))
            #inicio do jogo
            if character == "P":
                player.goto(screen_x, screen_y)
            #final do jogo
            if character == "F":
                finish.goto(screen_x, screen_y)

#verifies if sequence of moves is valid
def valid(moves):
    player.goto(initx, inity)
    prev = ""

    for x in moves:
        if trace == "y" or trace == "Y":
            time.sleep(0.02)
        #se bater na parede ou o anterior for simetrico vai retornar false e não é movimento válido
        if x == "U":
            if not player.go_up() or prev == "D":
                return False
        elif x == "L":
            if not player.go_left() or prev == "R":
                return False
        elif x == "D":
            if not player.go_down() or prev == "U":
                return False;
        elif x == "R":
            if not player.go_right() or prev == "L":
                return False

        #guarda o movimento para comprar na prox iteracao
        prev = x

    return True;

#verifica se o player chega ao final e também anda com o player
def final(moves):
    player.goto(initx, inity)
    #anda com o player
    for x in moves:
        if x == "U":
            player.go_up()
        elif x == "D":
            player.go_down()
        elif x == "L":
            player.go_left()
        elif x == "R":
            player.go_right()
    #verifica se é o quadrado final
    if player.xcor() == finish.xcor() and player.ycor() == finish.ycor():
        return True;

    return False;


#Create class instances
pen = Pen()
player = Player()
finish = Finish()

# Walls
walls=[]

#Set up the level
setup_maze(levels[1])

#Mostrar ou nao as animacoes
trace = input("Show animation? (y/n): ")

if trace == "n" or trace == "N":
    print("\ncalculating path...\n")
    wn.tracer(0) #nao mostra as animações

#escolher se queres usar queue ou stacks
choose = input("1-Queue\n2-Stack\n")

if choose == "1":
    nums = queue.Queue()
    nums.put("")
    add = ""
elif choose == "2":
    nums = queue.LifoQueue()
    nums.put("")
    add = ""
#guardar as coordenadas do inicio
initx = player.xcor()
inity = player.ycor()

#começa o timer
start = timeit.default_timer()

#Main Game Loop
while True:

    add = nums.get()

    #ajudar
    if trace == "y" or trace == "Y":
        print(add)
    #movimentos conter clockwise
    for j in ["U", "L", "D", "R"]:
        if trace == "y" or trace == "Y":
            time.sleep(0.02)
        #mete o movimento na variavel
        put = add + j
        #verifica se o movimento é valido
        #Se o movimento for valido adiciona a queue/stack
        if valid(put):
            nums.put(put)
        #anda com o player
        #verifica se chegamos ao fim
        if final(put):
            stop = timeit.default_timer()

            print("path: " + put)
            print("steps: ", len(put))
            print('time: ', stop - start)

            player.goto(initx, inity)

            #com o movimento final ele faz o caminho certo
            for x in put:
                wn.update()
                pen.goto(player.xcor(), player.ycor())
                pen.color("red")
                pen.stamp()
                time.sleep(0.1)
                if x == "U":
                    player.go_up()
                elif x == "D":
                    player.go_down()
                elif x == "L":
                    player.go_left()
                elif x == "R":
                    player.go_right()

                wn.update()

            #escreve os dados
            finish.color("red")
            wn.update()
            time.sleep(1)
            wn.reset()
            turtle.color("red")
            turtle.write("Finished \n", align= "center", font=("Arial", 60, "normal"))
            turtle.color("white")
            turtle.write("Path:  " + put + "\nSteps: %s\nTime: %.3f seconds" %(len(put),(stop - start)), align= "center", font=("Arial", 10, "normal"))
            time.sleep(3)
            exit()

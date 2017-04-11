#!/usr/bin/python3
from chatTCP import *
from game import *
import  random
import time
from collections import namedtuple

MAX_CONNECTS = 3
Player = namedtuple("Player", "socket addr num")

""" generate a random valid configuration """
def randomConfiguration():
    boats = [];
    while not isValidConfiguration(boats):
        boats=[]
        for i in range(5):
            x = random.randint(1,10)
            y = random.randint(1,10)
            isHorizontal = random.randint(0,1) == 0
            boats = boats + [Boat(x,y,LENGTHS_REQUIRED[i],isHorizontal)]
    return boats



def displayConfiguration(boats, shots=[], showBoats=True):
    Matrix = [[" " for x in range(WIDTH+1)] for y in range(WIDTH+1)]
    for i  in range(1,WIDTH+1):
        Matrix[i][0] = chr(ord("A")+i-1)
        Matrix[0][i] = i

    if showBoats:
        for i in range(NB_BOATS):
            b = boats[i]
            (w,h) = boat2rec(b)
            for dx in range(w):
                for dy in range(h):
                    Matrix[b.x+dx][b.y+dy] = str(i)

    for (x,y,stike) in shots:
        if stike:
            Matrix[x][y] = "X"
        else:
            Matrix[x][y] = "O"


    for y in range(0, WIDTH+1):
        if y == 0:
            l = "  "
        else:
            l = str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
        return l

""" display the game viewer by the player"""
def displayGame(game, player, ):
    otherPlayer = (player+1)%2
    sendMessage(player, displayConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    sendMessage(otherPlayer, displayConfiguration([], game.shots[player], showBoats=False)


""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

def startGame() :
    boats1 = randomConfiguration()
    boats2 = randomConfiguration()
    game = Game(boats1, boats2)
    displayGame(game, 0)
    print("======================")
    return game

def sendMessage(player, message) :
    print(message)
    if (skt != socks[x]) and (skt != sock)  :
        connects[player.num+1].send(message)

def waitMessage(player, socks ) :
    while True :
        message = connects[player.num].recv(2048)
        if len(message) == 0 :
            connects[x].socket.close()
            connects.remove(player)
            return None
        return message


def main():

    #make sockets
    sock = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 7777))
    sock.listen(1)
    connects = [sock]

    #wait for clients
    while True :
        (socks,_,_) = select.select(connects, [], [])
        for x in range(0, len(socks), 1) :
            if socks[x] == sock && len(connects) < 3 :
                acpt, addr = sock.accept()
                player = Player(socket=acpt, addr = addr. num = len(socks-1))
                connects.append(player);
            else if len(connects) >= 3
                break;




""" Find Clients (2)
    start game
    (how to avoid disconnections ?)
    while game
        for players
            message player
            validate input
            make move
            send game state to players
        check game over

fonctions to change -
    displayGame
    main

"""
    game = startGame()

    currentPlayer = 0
    displayGame(game, currentPlayer)
    while gameOver(game) == -1:
        print("======================")
        if currentPlayer == J0:
            sendMessage(0, "quelle colonne ? ")
            x_char = waitMessage(0, connects)
            if x_char != None :
                x_char.capitalize()
                x = ord(x_char)-ord("A")+1
                sendMessage(0, "quelle ligne ? ")
                y = waitMessage(0, connects)
                if y != None
                    y = int(y)
                else:
                    break;
            else:
                break;
        else:
            (x,y) = randomNewShot(game.shots[currentPlayer])
            time.sleep(1)
        addShot(game, x, y, currentPlayer)
        displayGame(game, 0)
        currentPlayer = (currentPlayer+1)%2

    for i in range(0, len(socks), 1 :

        print("game over")
        print("your grid :")
        displayGame(game, i)
        print("the other grid :")
        displayGame(game, i)

    if gameOver(game) == J0:
        print("You win !")
    else:
        print("you loose !")

main()

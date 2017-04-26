#!/usr/bin/python3
from game import *
import utils.py
import socket
import select
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
            l += "\n"
            l += str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
    l += "\n"
    return l

""" display the game viewer by the player"""
def displayGame(game, players, currentPlayer):
    #players = [addr, socket, 0; ...], currentPlayer = [0,1]
    otherPlayer = (currentPlayer+1)%2
    display1 = displayConfiguration(game.boats[currentPlayer], game.shots[otherPlayer], showBoats=True)
    display2 = displayConfiguration([], game.shots[otherPlayer], showBoats=False)
    sendMessage(players[currentPlayer], "Your Game:\n" + display1 + "\n")
    sendMessage(players[otherPlayer], "Your Shots:\n" + display2 + "\n")


def sendMessage(player, mesg):
    print(player)
    player.socket.send(mesg.encode('utf-8')) #removed "utf-8"

""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

def startGame(players) :
    boats1 = randomConfiguration()
    boats2 = randomConfiguration()
    game = Game(boats1, boats2)
    displayGame(game, players, 0)
    displayGame(game, players, 1)
    print("======================")
    return game

def waitMessage(player, players) :
    while True :
        message = player.socket.recv(2048)
        if len(message) == 0 :
            #Add code for monitor closing sockets
            #players[x].socket.close()
            #players.remove(player)
            return None
        return message.splitlines()


def main():
    print("this works")
    #make sockets
    sock = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 7777))
    sock.listen(1)
    connects = [sock]
    players = []

    print("Waiting for clients")

    #wait for clients
    while True :
        (socks,_,_) = select.select(connects, [], [])
        for x in range(0, len(socks), 1) :
            if (socks[x] == sock) & (len(connects) < 3) :
                print("New Player!")
                acpt, addr = sock.accept()
                player = Player(socket=acpt, addr = addr, num=len(socks)-1)
                connects.append(player.socket);
                players.append(player)
        if (len(connects) >= MAX_CONNECTS) :
            print("No new players :(")
            break;

    game = startGame(players)

    currentPlayer = 0
    while gameOver(game) == -1:
        print("======================") #>>>> utils shot validation
        if currentPlayer == J0:
            sendMessage(players[0], "quelle colonne ? ")
            x_char = waitMessage(players[0], connects)
            if x_char != None :
                x_char[0] = x_char[0].upper()
                x = ord(x_char[0].upper())-ord("A")+1
                sendMessage(players[0], "quelle ligne ? ")
                y = waitMessage(players[0], connects)
                if y != None :
                    y = int(y[0])
                else:
                    break;
            else:
                break;
        else:
            (x,y) = randomNewShot(game.shots[currentPlayer])
            time.sleep(1)
        addShot(game, x, y, currentPlayer)
        #Select here for awaiting connections and add them
        #this also allows us to validate that the players are still here
        displayGame(game, players, currentPlayer)
        currentPlayer = (currentPlayer+1)%2


    for i in range(0, len(socks), 1):

        print("game over")
        print("your grid :")
        displayGame(game, players, i)
        print("the other grid :")
        displayGame(game, players, i)

    if gameOver(game) == J0:
        print("You win !")
    else:
        print("you loose !")

main()

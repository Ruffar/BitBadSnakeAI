import tkinter as tk
import math
import random
import time

import numpy as np



class Direction:
    Up = np.array([0,1])
    Down = np.array([0,-1])
    Left = np.array([-1,0])
    Right = np.array([1,0])


class Snake:
    def __init__(self, headPos: np.ndarray, direction: np.ndarray):
        self._length = 2
        self._direction = direction #must be normalized
        self._parts = [headPos, headPos-direction]

    def getLength(self) -> int:
        return self._length

    def increaseLength(self) -> None:
        self._length += 1

    def getDirection(self) -> np.ndarray:
        return self._direction

    def setDirection(self, direction: np.ndarray) -> np.ndarray:
        if direction is not None and not np.array_equal(direction, -self._direction):
            self._direction = direction

    def getHead(self) -> np.ndarray:
        return self._parts[0]

    def getParts(self) -> list[np.ndarray]:
        return self._parts

    def isHeadInBody(self) -> bool:
        return self.isPartPresent(self._parts[0], includeHead=False)

    def isPartPresent(self, position: np.ndarray, includeHead = True) -> bool:
        for i in range(int(not includeHead), len(self._parts)):
            if np.array_equal(self._parts[i], position):
                return True
        return False

    def move(self) -> None:
        #Add new part at start of list (new head)
        self._parts.insert(0, self._parts[0]+self._direction)
        #Remove last part (tail has moved) unless apple is eaten
        if len(self._parts) > self._length:
            self._parts.pop()


class Apple:
    def __init__(self, pos: np.ndarray):
        self._pos = pos

    def getPos(self) -> np.ndarray:
        return self._pos
        

class SnakeGame:
    def __init__(self, boardSize: int):
        self._alive = True
        self._size = boardSize

        self._snake = Snake(np.array([random.randint(2,self._size-3), random.randint(2,self._size-3)]), Direction.Up)
        self._placeNewApple()
        

    def getSize(self) -> int:
        return self._size

    def isAlive(self) -> bool:
        return self._alive

    def getScore(self) -> int:
        return self._snake.getLength()-2 #Default length is 2

    def getGameObjects(self):
        return self._snake, self._apple

    def isSnakeBlocked(self, direction: np.ndarray) -> bool:
        targetPos = self._snake.getHead()+direction
        return self._snake.isPartPresent(targetPos) or targetPos[0] < 0 or targetPos[0] >= self._size or targetPos[1] < 0 or targetPos[1] >= self._size

    def _placeNewApple(self) -> None:
        self._apple = Apple(np.array([random.randint(2,self._size-3), random.randint(2,self._size-3)]))

    def step(self) -> None:
        #Move the snake
        self._snake.move()

        headPos = self._snake.getHead()

        #Check if apple is eaten
        if np.array_equal(self._apple.getPos(), headPos):
            self._snake.increaseLength()
            self._placeNewApple()

        #Check if snake has collided with anything
        if self._snake.isHeadInBody() or headPos[0] < 0 or headPos[0] >= self._size or headPos[1] < 0 or headPos[1] >= self._size:
            self._alive = False
        

class SnakeWindow:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Snake")

        self._size = 8
        self.simul = 20
        self.delta = 0.5
        self.restartGame()

        self.scoretext = tk.Label(self.master,text='Score: 0+0',font='legacy 15 bold')
        self.scoretext.pack()
        #self.scoretext.grid(row=int(math.floor(i/self.popscreendiv)*2)+1,column=int(i%self.popscreendiv))

        self.board = tk.Canvas(self.master,width=self._size*self.simul,height=self._size*self.simul,bg='#66bb66')
        self.board.pack()
        #self.boards[i].grid(row=int(math.floor(i/self.popscreendiv)*2)+2,column=int(i%self.popscreendiv))

        #master.bind("<Key>",self.keypress)
        #self.lastkey = 0
       
    #def keypress(self,event):
        #self.lastkey = event.keycode

    def getGame(self) -> SnakeGame:
        return self._game

    def restartGame(self) -> None:
        self._game = SnakeGame(self._size)

    def step(self):
        time.sleep(0.5)
        #self.gameloop()
        self.render()
        self.master.update()

    def render(self):
        board = self.board
        scoretext = self.scoretext
        snake, apple = self._game.getGameObjects()
        board.delete("all")

        for part in snake.getParts():
            x = part[0]*self.simul
            y = part[1]*self.simul
            try:
                board.create_rectangle(x,y,x+self.simul,y+self.simul,fill='white',width=0,outline='')
            except: print(x,y,self.simul)

        applePos = apple.getPos()*self.simul
        board.create_rectangle(applePos[0],applePos[1],applePos[0]+self.simul,applePos[1]+self.simul,fill='red',width=0,outline='')

        scoretext.config(text='Score: '+str(self._game.getScore()))

    def stop(self) -> None:
        self.master.destroy()
        

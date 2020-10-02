import pygame
from pygame.locals import *
from random import randint
import time

class Food:
	x = 0
	y = 0
	step = 20
	def __init__(self,x,y):
		self.x = x*self.step
		self.y = y*self.step

	def draw(self, Window, image):
		Window.blit(image, (self.x, self.y))

class Player:
	x = [0]
	y = [0]
	step = 20
	length = 4
	direc = 0
	uCountMax = 2
	uCount = 0
	def __init__(self, length):
		self.length = length
		for t in range(0,10000):
			self.x.append(-100)
			self.y.append(-100)

		self.x[0] = 1*self.step
		self.x[1] = 2*self.step

	def update(self):
		self.uCount = self.uCount +1
		if self.uCount > self.uCountMax:
			for t in range(self.length-1, 0, -1):
				self.x[t] = self.x[t-1]
				self.y[t] = self.y[t-1]

			if self.direc == 0:
				self.x[0] = self.x[0] + self.step
			if self.direc == 1:
				self.x[0] = self.x[0] - self.step
			if self.direc == 2:
				self.y[0] = self.y[0] - self.step
			if self.direc == 3:
				self.y[0] = self.y[0] + self.step

			self.uCount = 0
	def Right(self):
		self.direc = 0
	def Left(self):
		self.direc = 1
	def Up(self):
		self.direc = 2
	def Down(self):
		self.direc = 3

	def draw(self, Window, image):
		for t in range(0,self.length):
			Window.blit(image,(self.x[t],self.y[t]))

class AI:
	x = [0]
	y = [0]
	step = 20
	length = 4
	direc = 0
	uCountMax = 2
	uCount = 0
	def __init__(self, length):
		self.length = length
		for t in range(0,10000):
			self.x.append(-100)
			self.y.append(-100)

		self.x[0] = 1*self.step
		self.x[1] = 4*self.step

	def update(self):
		self.uCount = self.uCount +1
		if self.uCount > self.uCountMax:
			for t in range(self.length-1, 0, -1):
				self.x[t] = self.x[t-1]
				self.y[t] = self.y[t-1]

			if self.direc == 0:
				self.x[0] = self.x[0] + self.step
			if self.direc == 1:
				self.x[0] = self.x[0] - self.step
			if self.direc == 2:
				self.y[0] = self.y[0] - self.step
			if self.direc == 3:
				self.y[0] = self.y[0] + self.step

	def Right(self):
		self.direc = 0
	def Left(self):
		self.direc = 1
	def Up(self):
		self.direc = 2
	def Down(self):
		self.direc = 3

	def targetFood(self, xChange, yChange):
		if self.x[0] > xChange:
			self.Left()
		if self.x[0] < xChange:
			self.Right()
		if self.x[0] == xChange:
			if self.y[0] < yChange:
				self.Down()
			if self.y[0] > yChange:
				self.Up()

	def draw(self, Window, image):
		for t in range(0,self.length):
			Window.blit(image,(self.x[t],self.y[t]))

class collisionCheck:
	def isCollided(self, xTarget, yTarget, x, y, bSize):
		if xTarget >= x and xTarget < x+bSize:
			if yTarget >= y and yTarget < y+bSize:
				return True

		return False

class Game:
	Window_width = 900
	Window_height = 600

	player = 0
	food = 0

	def __init__(self):
		self._running = True
		self._Window = None
		self._imageWinPlayer = None
		self._imageWinAI = None
		self._foodWin = None
		self.start = collisionCheck()
		self.player = Player(5)
		self.food = Food(randint(1,10),randint(1,10))
		self.ai = AI(5)

	def onInit(self):
		pygame.init()
		self._Window = pygame.display.set_mode((self.Window_width,self.Window_height), pygame.HWSURFACE)
		self._running = True
		self._foodWin = pygame.image.load("hamburger.png").convert()
		self._imageWinPlayer = pygame.image.load("box.png").convert()
		self._imageWinAI = pygame.image.load("boxAI.png").convert()

	def quitEvent(self, event):
		if event.type == QUIT:
			self._running = False

	def loop(self):
		self.ai.targetFood(self.food.x, self.food.y)
		self.player.update()
		self.ai.update()

		for t in range(0,self.player.length):
			if self.start.isCollided(self.food.x, self.food.y, self.player.x[t], self.player.y[t], self.food.step):
				self.food.x = randint(2,9)*self.food.step
				self.food.y = randint(2,9)*self.food.step
				self.player.length = self.player.length + 1

		for t in range(0,self.ai.length):
			if self.start.isCollided(self.food.x, self.food.y, self.ai.x[t], self.ai.y[t], self.food.step):
				self.food.x = randint(2,9)*self.food.step
				self.food.y = randint(2,9)*self.food.step
				self.ai.length = self.ai.length + 1

		for t in range(2, self.player.length):
			if self.start.isCollided(self.player.x[0],self.player.y[0],self.player.x[t],self.player.y[t], self.player.step/2):
				print("player lost")
				print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
				print("x[" + str(i) + "] (" + str(self.player.x[t]) + "," + str(self.player.y[t]) + ")")

		for t in range(2, self.ai.length):
			if self.start.isCollided(self.ai.x[0],self.ai.y[0],self.ai.x[t],self.ai.y[t], self.ai.step/2):
				print("ai lost")
				print("x[0] (" + str(self.ai.x[0]) + "," + str(self.ai.y[0]) + ")")
				print("x[" + str(t) + "] (" + str(self.ai.x[t]) + "," + str(self.ai.y[t]) + ")")


	def displayStoff(self):
		self._Window.fill((255,255,255))
		self.player.draw(self._Window, self._imageWinPlayer)
		self.food.draw(self._Window, self._foodWin)
		self.ai.draw(self._Window,self._imageWinAI)
		pygame.display.flip()

	def cleanUp(self):
		pygame.quit()

	def excecute(self):
		if self.onInit() == False:
			self._running == False

		while self._running:
			pygame.event.pump()
			key = pygame.key.get_pressed()

			if(key[K_RIGHT]):
				self.player.Right()
			if(key[K_LEFT]):
				self.player.Left()
			if(key[K_DOWN]):
				self.player.Down()
			if(key[K_UP]):
				self.player.Up()

			self.loop()
			self.displayStoff()

			time.sleep(50/100)
		self.cleanUp()

if __name__ == "__main__":
	StartGame = Game()
	StartGame.excecute()
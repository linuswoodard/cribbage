## shows how to use a class to make a button element in pygame which, when clicked executes a function. 


import pygame as pg, sys
from pygame.locals import *
import time
import numpy as np

width = 600
height = 600

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Cribbage Board')

red = (125, 27, 42)
blue = (51, 55, 138)
rwhite = (220,220,220)


font = pg.font.SysFont('Bernard MT Condensed', 25)
objects = []

class Button():
	def __init__(self, x, y, width, height, color, arg, buttonText = "Button", onclickFunction = None):
		if color == 'red':
			self.fillColors = {
				'normal':red,
				'hover':(200,0,0),
				'pressed':(150,0,0),
				'textColor':rwhite
			}
		else:
			self.fillColors = {
				'normal':blue,
				'hover':(0,0,200),
				'pressed':(0,0,150),
				'textColor':rwhite
			}
		self.arg = arg
		self.onclickFunction = onclickFunction
		self.alreadyPressed = False
		self.buttonSurface = pg.Surface((width, height))
		self.buttonRect = pg.Rect(x, y, width, height)
		self.buttonSerf = font.render(buttonText, True, self.fillColors['textColor'])

		objects.append(self)

	def process(self):
		mousePos = pg.mouse.get_pos()
		self.buttonSurface.fill(self.fillColors['normal'])
		if self.buttonRect.collidepoint(mousePos):
			self.buttonSurface.fill(self.fillColors['hover'])

			if pg.mouse.get_pressed()[0]:
				self.buttonSurface.fill(self.fillColors['pressed'])
				if not self.alreadyPressed:
					self.onclickFunction(self.arg)
					self.alreadyPressed = True
			else:
				self.alreadyPressed = False

		self.buttonSurface.blit(self.buttonSerf, [
				self.buttonRect.width/2-self.buttonSerf.get_rect().width/2,
				self.buttonRect.height/2-self.buttonSerf.get_rect().height/2])
		screen.blit(self.buttonSurface, self.buttonRect)

def b1(text):
	print('Button 1 prints ' + text)

button1 = Button(100,100,80,60,'red','button one text', 'Button 1', b1)
button1 = Button(300,100,80,60,'blue','button two text', 'Button 2', b1)

while True:
	for event in pg.event.get():
		if event.type ==QUIT:
			pg.quit()
			sys.exit()
	for ob in objects:
		ob.process()
	pg.display.update()
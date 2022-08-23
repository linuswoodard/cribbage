# laoding good looking face pieces into a game
# constraints:  Faces must look good at a size of pg circle of radius 10 (can be a bit bigger but no bigger than the spacing of the holes)

import pygame as pg, sys
from pygame.locals import *

width = 400
height = 400

radius = 10

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Face Pieces')


# create little set of peg holes the same spacing as on the main cribage game
def group(x, y):
	vspace = 30
	hspace = 25
	group = []
	for i in range(5):
		group.append((x+hspace*i, y+vspace/2))
		group.append((x+hspace*i, y-vspace/2))
	return group
holes = group(140, 200)
for hole in holes:
	pg.draw.circle(screen, (200,200,200), hole, radius, width = 3)
pg.display.update()


# import face pictures
# "cody.png" is 387x525
aspect = 525/387
image_size = (25,25*aspect)
angle = 20
cody = pg.image.load("cody.png")
cody = pg.transform.scale(cody, image_size)
cody = pg.transform.rotate(cody, angle)

x_offset = 15
y_offset = 19
pic_holes = []
for hole in holes:
	x,y = hole
	x-=x_offset
	y-=y_offset
	ph = (x,y)
	pic_holes.append(ph)

screen.blit(cody, pic_holes[0])
screen.blit(cody, pic_holes[4])
pg.display.update()

print('picture', cody.get_bitsize())
print('screen', screen.get_bitsize())

while True:
	for event in pg.event.get():
		if event.type ==QUIT:
			pg.quit()
			sys.exit()

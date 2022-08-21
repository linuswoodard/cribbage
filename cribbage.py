import pygame as pg, sys
from pygame.locals import *
import time
import numpy as np

# Still a glitch where the program crashes when a team wins in some circumstances

# Global Variables
rwhite = (220,220,220)
white = (74, 56, 38) # not white
black = (0,0,0)
red = (125, 27, 42)
blue = (51, 55, 138)

width = 1500
height = 700

rhist = [0,1]
bhist = [0,1]
rscore = 0
bscore = 0
rGamesWon = 0
bGamesWon = 0

winner = None

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Cribbage Board')

#background image
background = pg.image.load('cribbage.png')
background = pg.transform.scale(background, (width,height))


# circle vars
vspace = 30
hspace = 25
radius = 10
line_width = 5

xs = np.arange(7)*140+300
ys = np.arange(3)*200+50

# Creates the coordinates for the curved portion on the right of the baord
rad_center_1 = (xs[-1]+4*hspace, ys[1])
inner_rad_1 = ys[1]-ys[0]+vspace/2
outter_rad_1 = ys[1]-ys[0]-vspace/2
angles = -np.pi/2+np.arange(15)*np.pi/14
angles = list(angles[2:7])+list(angles[8:13])
curved_holes_1 = []
for angle in angles:
	curved_holes_1.append((np.cos(angle)*outter_rad_1+rad_center_1[0], np.sin(angle)*outter_rad_1+rad_center_1[1]))
	curved_holes_1.append((np.cos(angle)*inner_rad_1+rad_center_1[0], np.sin(angle)*inner_rad_1+rad_center_1[1]))

# Creates the coordinates for the curved portion on the left side of the board
rad_center_2 = (xs[0], (ys[1]+ys[2])/2)
inner_rad_2 = (ys[1]+ys[2])/2-ys[1]+vspace
outter_rad_2 = (ys[1]+ys[2])/2-ys[1]-vspace
angles = np.pi/2+np.arange(10)*np.pi/8
angles = list(angles[2:7])
curved_holes_2 = []
for angle in angles:
	curved_holes_2.append((np.cos(angle)*outter_rad_2+rad_center_2[0], np.sin(angle)*outter_rad_2+rad_center_2[1]))
	curved_holes_2.append((np.cos(angle)*inner_rad_2+rad_center_2[0], np.sin(angle)*inner_rad_2+rad_center_2[1]))



# creates a list of 10 tuples for holes starting from x on the left side and y centered verticlly between the rows
# coordinates are in shape:	   x x x x x
#							   x x x x x 
def group(x, y):
	group = []
	for i in range(5):
		group.append((x+hspace*i, y+vspace/2))
		group.append((x+hspace*i, y-vspace/2))
	return group

# Creates coordinates for the starting holes
starting_holes = group(xs[0]-140, ys[0])[-4:]

# Creates coordinates for the number of games won scoring holes
scoring_holes = []
vstart = ys[0]-vspace/2
vend = ys[-1]+vspace/2
yholes = np.arange(8)*(vend-vstart)/7+vstart
x1,x2 = 50, 100
for y in yholes:
	scoring_holes.append((x1, y))
	scoring_holes.append((x2, y))

w = (7*140+300, ys[1])


### collects all the coordinates
coords = []
for y in ys:
	for x in xs:
		coords += group(x,y)
for hole in curved_holes_1:
	coords.append(hole)
for hole in curved_holes_2:
	coords.append(hole)
coords+=starting_holes
coords+=scoring_holes
coords.append(w)

# ordering the holes for the game
r = coords[::2]
b = coords[1::2]
red_path = []
blue_path = []
red_path += r[-11:-9] + r[:35] + r[105:115] + list(reversed(b[70:105])) + r[115:120] + r[35:70] + [coords[-1]]
blue_path += b[-10:-8] + b[:35] + b[105:115] + list(reversed(r[70:105])) + b[115:120] + b[35:70] + [coords[-1]]

# ordering overall score
r_score_holes = scoring_holes[::2]
b_score_holes = scoring_holes[1::2]

# Button Class
font = pg.font.SysFont('Jokerman Regular', 25)
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


def draw_board():
	'''draws a circle at every coordinate'''
	global white, coords
	screen.fill(black)
	screen.blit(background, (0,0))
	for coord in coords:
		pg.draw.circle(screen, white, coord, radius, width = line_width)
	pg.display.update()


def draw_pieces():
	global rGamesWon, bGamesWon
	for i in rhist[-2:]:
		pg.draw.circle(screen, red, red_path[i], radius)
	for i in bhist[-2:]:
		pg.draw.circle(screen, blue, blue_path[i], radius)

	pg.draw.circle(screen, red, r_score_holes[rGamesWon], radius)
	pg.draw.circle(screen, blue, b_score_holes[bGamesWon], radius)
	pg.display.update()

def start():
	global rhist, bhist, rscore, bscore, winner
	winner = None
	rhist = [0,1]
	bhist = [0,1]
	rscore = 0
	bscore = 0
	draw_board()
	draw_pieces()


def advance_red(points):
	global rhist, rscore, bhist, bscore, winner
	rpoints = points
	rscore +=rpoints
	if rscore >=121:
		winner = 'Red'
		rhist.append(122)
	else:
		rhist.append(rhist[-1]+rpoints)
	draw_board()
	if winner is None:
		draw_pieces()
	else:
		win()

def advance_blue(points):
	global rhist, rscore, bhist, bscore, winner
	bpoints = points
	bscore +=bpoints
	if bscore >= 121:
		winner='Blue'
		bhist.append(122)
	else:
		bhist.append(bhist[-1]+bpoints)
	draw_board()
	if winner is None:
		draw_pieces()
	else:
		win()

def undo_red(arg):
	global rhist, rscore
	rscore = rscore-(rhist[-1]-rhist[-2])
	rhist = rhist[:-1]
	draw_board()
	draw_pieces()

def undo_blue(arg):
	global bhist, bscore
	bscore = bscore-(bhist[-1]-bhist[-2])
	bhist = bhist[:-1]
	draw_board()
	draw_pieces()

buttonY = np.arange(3)*60+height-180
buttonX = np.arange(8)*85+50
advance = 1
for yloc in buttonY:
	for xloc in buttonX:
		Button(xloc, yloc, 75, 50, 'red', advance, str(advance), advance_red)
		advance+=1

buttonY = np.arange(3)*60+height-180
buttonX = np.arange(8)*85 + width/2+50
advance = 1
for yloc in buttonY:
	for xloc in buttonX:
		Button(xloc, yloc, 75, 50, 'blue', advance, str(advance), advance_blue)
		advance+=1

Button(width/2-22, height-180, 65, 50, 'red', None, "Undo", undo_red)
Button(width/2-22, height-60, 65, 50, 'blue', None, "Undo", undo_blue)




def win():
	global winner, rGamesWon, bGamesWon
	if winner == "Red":
		pg.draw.circle(screen, red, w, radius)
		rGamesWon += 1
	else:
		pg.draw.circle(screen, blue, w, radius)
		bGamesWon += 1
	font = pg.font.SysFont('Bernard MT Condensed', 50)
	message = winner + " Wins!!"
	text = font.render(message, True, rwhite)
	text_rect = text.get_rect()
	text_rect.center = (width/2, height/2)
	screen.blit(text, text_rect)
	pg.display.update()
	time.sleep(3)
	start()


start()

while True:
	for event in pg.event.get():
		if event.type ==QUIT:
			pg.quit()
			sys.exit()
	for ob in objects:
		ob.process()

	pg.display.update()
import pygame
#from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint

sx = 800
sy = 600

class glImage:
	_x = 0
	_y = 0
	_w = 0
	_h = 0
	_texture = None
	_DL = None
	
	def __init__(self, x=0, y=0):
		self._x = x
		self._y = y
		
	def drawRects(self, w, h):
		w += self._x
		h += self._y
		glColor3ub(randint(0, 255),randint(0, 255),randint(0, 255))
		glBegin(GL_QUADS)
		glVertex2f(self._x,h)
		glVertex2f(w, h)
		glVertex2f(w, self._y)
		glVertex2f(self._x, self._y)
		glEnd()
		
	def drawTexture(self, x, y):
		glTranslatef(x, y, 0)
		glCallList(self._DL)
		
	def setPos(self, x, y):
		self._x = x
		self._y = y
		
	def loadImage(self, imagefile):
		surface = pygame.image.load(imagefile)
		
		self._textureData = pygame.image.tostring(surface, "RGBA", 1)
		
		self._w = surface.get_width()
		self._h = surface.get_height()
		
		#create a new texture
		self._texture = glGenTextures(1)
		#activate the texture
		glBindTexture(GL_TEXTURE_2D, self._texture)
		#define the filters for texture scaling up and scaling down 
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		#copy the image data to the texture
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._w, self._h, 0, GL_RGBA, GL_UNSIGNED_BYTE, self._textureData )
		
	def optimizeTexture(self):
		self._DL = glGenLists(1)
		glNewList(self._DL,GL_COMPILE);
		glBindTexture(GL_TEXTURE_2D, self._texture)
		glBegin(GL_QUADS)
		#binds the texture position to a new rectangle
		glTexCoord2f(0, 0); glVertex2f(0, 0)    # Bottom Left Of The Texture and Quad
		glTexCoord2f(0, 1); glVertex2f(0, self._h)    # Top Left Of The Texture and Quad
		glTexCoord2f(1, 1); glVertex2f( self._w,  self._h)    # Top Right Of The Texture and Quad
		glTexCoord2f(1, 0); glVertex2f(self._w, 0)    # Bottom Right Of The Texture and Quad
		glEnd()
		glEndList()
		
	def __del__(self):
		if self._texture:
			glDeleteTextures(self._texture)
		if self._DL:
			glDeleteLists(self._DL, 1)




def main():
	pygame.init()
	pygame.display.set_mode((sx, sy), pygame.OPENGL | pygame.DOUBLEBUF)
	
	#initialize opengl view
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	#reset the current position
	glLoadIdentity()
	gluOrtho2D(0, sx, 0, sy)
	glMatrixMode(GL_MODELVIEW)
	
	#enable textures and blending effect
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	done = False
	
	#init some rects
	i = []
	#for z in range(3000):
	#	i.append(glImage())
	
	files = ['text.png', 'text2.png', 'text3.png', 'text4.png']
	#for v, q in enumerate(i):
	#	q.loadImage(files[randint(0,3)])
	#	q.optimizeTexture()
	
	i = glImage()
	i.loadImage('bg.png')
	i.optimizeTexture()
		
	#raw_input()
	
	fps = 0
	clock = pygame.time.Clock()
	layers = 1
	while not done:
		#reset the position
		glLoadIdentity()
		#clear the screen framebuffer
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		for k in range(layers):
			i.drawTexture(randint(0, 200), randint(0, 200))
		
		#draw the rects 1st layer
		#for w in range(layers):
		#	u = 0
		#	v = 0
		#	for q in i:
		#		glLoadIdentity()
		#		q.drawTexture(u, v)
		#		u += 16
		#		if u > sx-5:
		#			v +=16
		#			u = 0
		#		if v > sy-1:
		#			break
			
		#	q.setPos(randint(0,630), randint(0,470))
		#	q.draw(16,16)
		
		evts = pygame.event.get()
		for event in evts:
			if event.type == pygame.QUIT \
			or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				done = True
		
		pygame.display.flip()
		clock.tick()
		print 'FPS:', clock.get_fps(), 'Layers:', layers
		if clock.get_fps() > 30:
			layers += 1
		else:
			layers -= 1

if __name__ == '__main__':
	main()

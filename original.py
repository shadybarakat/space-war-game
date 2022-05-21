
from cmath import*
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

####################################
########### constants ##############
####################################
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
enemy_x=200
enemy_y=760
enemy_z=400
deltaX = 1
delta_x = -1
delta_z=1
first_enemy=280
second_enemy=280
third_enemy=280
player=220
scale_a=1
scale_b=1
level_2=0
go=0

INTERVAL = 20 #

####################################
######## graphics helpers ##########
####################################
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0) 

    glMatrixMode(GL_PROJECTION)  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f


    glMatrixMode(GL_MODELVIEW)

    loadTextures()
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING


texture_names = [0, 1,2,3,4]  # TODO IMPORTANT must be numbers


def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]


def loadTextures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer refernece number.
    """
    glEnable(GL_TEXTURE_2D)  # texture init step [1]
    # Load images from file system
    images = []  # texture init step [2]
    images.append(pygame.image.load("background.jpg"))  # repeat this for more images
    images.append(pygame.image.load("player.png"))  # repeat this for more images
    images.append(pygame.image.load("enemy.png"))  # repeat this for more images
    images.append(pygame.image.load("player_fire.png")) 
    images.append(pygame.image.load("fire_2.png"))  # repeat this for more images
    
    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True)  # TODO change True to False
                for image in images]  # texture init step [3]

    # Generate textures names from array
    glGenTextures(len(images), texture_names)  # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      texture_names[i],  # identifiers
                      images[i].get_width(),
                      images[i].get_height())

####################################
########### game state #############
####################################
#######################################################################################################


 # try texture[1] & texture[2] & texture[3] & texture[4]
    




mouse_x=0
Fire=0
Start=0
def MouseMotion(x, y):
        global mouse_x
        mouse_x=x
         

def Click_fun(button,state,x,y):
        global Fire
        if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
                Fire=1
        else:
                Fire=0

def keyboard(key, x, y):
        global Start
        if key == b"s": 
                Start=1


def draw_text(string, x, y,a,b,w):
    glColor(1,1,1)
    glLoadIdentity()
    glLineWidth(w)
    # glColor(1, 1, 1)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(a, b, 1)  # when writing text and see nothing downscale it to a very small value .001 and draw at center
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()
    glFlush()

def draw_fire(x,y1,y2,type):
        glColor(1,1,1)
        if type=='player':
           glBindTexture(GL_TEXTURE_2D, texture_names[3])
        elif type=='enemy':
           glBindTexture(GL_TEXTURE_2D, texture_names[4])
        glBegin(GL_QUADS)
        glTexCoord(0,1)
        glVertex(x-50,y1,0)
        glTexCoord(1,1 )
        glVertex(x+50,y1,0)
        glTexCoord(1, 0)
        glVertex(x+50,y2,0)
        glTexCoord(0, 0)
        glVertex(x-50,y2,0)
        glEnd() 

def drawSpaceShip(xaxis,yaxis,dir,type):
    glColor(1,1,1)
    if type=='player':
       glBindTexture(GL_TEXTURE_2D, texture_names[1])
       glBegin(GL_POLYGON)
       glTexCoord(0,0)
       glVertex(xaxis-40,yaxis,0)
       glTexCoord(0,1)
       glVertex(xaxis-40,yaxis+(dir*80),0)
       glTexCoord(1,1)
       glVertex(xaxis+40,yaxis+(dir*80),0)
       glTexCoord(1,0)
       glVertex(xaxis+40,yaxis,0)
       glEnd()
    elif type=='enemy':
       glBindTexture(GL_TEXTURE_2D, texture_names[2])
       glBegin(GL_POLYGON)
       glTexCoord(0,1)
       glVertex(xaxis-40,yaxis,0)
       glTexCoord(0,0)
       glVertex(xaxis-40,yaxis+(dir*80),0)
       glTexCoord(1,0)
       glVertex(xaxis+40,yaxis+(dir*80),0)
       glTexCoord(1,1)
       glVertex(xaxis+40,yaxis,0)
       glEnd()


def draw_health(x,y1,y2):
        glBegin(GL_POLYGON)
        glVertex(x,y1,0)
        glVertex(x+25,y1,0)
        glVertex(x+25,y2,0)
        glVertex(x,y2,0)
        glEnd()   

def draw_space():
        glBindTexture(GL_TEXTURE_2D, texture_names[0])
        glColor(1,1,1)
        glBegin(GL_QUADS)
        glTexCoord(0,1)
        glVertex(0,500,0)
        glTexCoord(1,1 )
        glVertex(800,500,0)
        glTexCoord(1, 0)
        glVertex(800,0,0)
        glTexCoord(0, 0)
        glVertex(0,0,0)
        glEnd() 
    



def display():
    global tail
    global enemy_x
    global enemy_y
    global delta_x
    global deltaX
    global enemy_y
    global first_enemy
    global second_enemy
    global player
    global scale_a
    global scale_b
    global enemy_z
    global level_2
    global delta_z
    global go
    global third_enemy
    global Fire
    global Start

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0,0, 0, 0)
    
    draw_space()
    #health
    glColor(1,0,0)
    draw_health(10,480,first_enemy)
    glColor(1,0,0)
    draw_health(50,480,second_enemy)
    glColor(0,1,0)
    draw_health(30,20,player)
    glLoadIdentity()
        
    


    if player <= 20:
            player=20
            draw_text('game over !',340,250,0.2,0.2,3)
            draw_text('press s to retry',330,220,0.15,0.15,2)
            if Start==1:
                player=220
                first_enemy=280
                second_enemy=280
                third_enemy=280
                level_2=0

#start level2
    if second_enemy==480 and first_enemy==480  and level_2 != 1:
          draw_text('level 1 compelet ',300,250,0.25,0.25,3)
          draw_text('press s for level 2 ',330,220,0.15,0.15,2)
          if Start==1:
              enemy_x=200
              enemy_y=760
              player=220
              first_enemy=280
              second_enemy=280
              level_2=1
              Start=0



#end of the game

    if second_enemy==480 and first_enemy==480 and third_enemy==480:
            first_enemy=480
            second_enemy=480
            third_enemy=480
            draw_text('you win! ',340,250,0.25,0.25,3)
            draw_text('press s to retry ',330,220,0.15,0.15,2)
            if Start==1:
                player=220
                first_enemy=280
                second_enemy=280
                third_enemy=280
                level_2=0

#colosion detection between wall and player
    MouseLimit=mouse_x
    if mouse_x > 760:
            MouseLimit=760
    elif mouse_x < 200:
            MouseLimit=200


#draw of fire
#player
    if Fire==1 and player >20:
      draw_fire(MouseLimit,520,80,'player')

#enemies
    go=go+1


#speed of enemies fire (60,95,115)
    if go%29==0 and first_enemy < 480:
            draw_fire(enemy_x,-70,500,'enemy')
    if go%67==0 and second_enemy < 480:
            draw_fire(enemy_y,-70,500,'enemy')
    if go%19==0 and level_2==1 and third_enemy < 480:
            draw_fire(enemy_z,-70,500,'enemy')


#draw of space ships

#player
    if player != 20:
      drawSpaceShip(MouseLimit,0,1,'player')

  
      
#enemies

    enemy_x=enemy_x+deltaX
    if first_enemy != 480:
       drawSpaceShip(enemy_x,500,-1,'enemy')
    enemy_y=enemy_y+delta_x
    if second_enemy != 480:
       drawSpaceShip(enemy_y,500,-1,'enemy')

    #enemy of level 2
    if level_2==1:
        glColor(1,0,0)
        draw_health(90,480,third_enemy)
        enemy_z=enemy_z+delta_z
        glColor(1,1,1)
        if third_enemy!=480:
          drawSpaceShip(enemy_z,500,-1,'enemy')   


#colosion detection between enemies and the wall
    if enemy_y > 760:
            delta_x=-1
    elif enemy_y < 200:
            delta_x=1

    if enemy_x > 760:
            deltaX=-1
    elif enemy_x < 200:
            deltaX=1

    if enemy_z > 760:
            delta_z=-1
    elif enemy_z < 200:
            delta_z=1

#colosion detection between enemies and the fire
    if (enemy_x -40) <MouseLimit and  MouseLimit < (enemy_x +40) and Fire == 1 and player > 20: 
            if first_enemy!=480:
               first_enemy=first_enemy+5
            Fire=0
    if (enemy_y - 40) < MouseLimit and MouseLimit < (enemy_y + 40) and Fire == 1 and player > 20:
            if second_enemy!=480:  
               second_enemy=second_enemy+5
            Fire=0
    if (enemy_z - 40) < MouseLimit and MouseLimit < (enemy_z + 40) and Fire==1 and player > 20:
            if third_enemy != 480:
               third_enemy=third_enemy+5
            Fire=0

#colosion detection between player and the fire
    if (enemy_x - 40) < MouseLimit and MouseLimit < (enemy_x + 40) and go%29==0 and first_enemy != 480:
        if player!=20:
            player=player-5

    if (enemy_y - 40) < MouseLimit and MouseLimit < (enemy_y + 40) and go%67==0 and second_enemy != 480:
        if player!=20:
            player=player-5

    if (enemy_z - 40) < MouseLimit and MouseLimit < (enemy_z + 40) and go%19==0 and third_enemy != 480 and level_2==1:
        if player!=20:
            player=player-5










 
    glutSwapBuffers()


####################################
############### Timers #############
####################################
def game_timer(v):
    display()
    glutTimerFunc(INTERVAL, game_timer, 1)


####################################
############ Callbacks #############
####################################



if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Space war OpenGL game")
    glutDisplayFunc(display)
    glutTimerFunc(INTERVAL, game_timer, 1)
    glutPassiveMotionFunc(MouseMotion)
    glutMouseFunc(Click_fun)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()
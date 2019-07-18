# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

from collections import namedtuple

def camera_lookat(c, x,y,z, cx,cy,cz, ux,uy,uz):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(x, y, z, cx, cy, cz, ux, uy, uz)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # camera
    camera_lookat(None,0.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #draw
    glColor3f(1.0, 0.0, 0.0)
    glutWireTeapot(1.0)   # wireframe
    glutSolidTeapot(1.0)  # solid

    glFlush()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def key(key,x,y):
    print(key)
    if key == b'q' or key == b'Q':
        sys.exit()

MouseInfo = namedtuple('MouseInfo', ('state', 'x', 'y'))
mouse_info = None

def mouse(button,state,x,y):
    print('mouse')
    print(button)
    print(state)
    if glutGetModifiers() == GLUT_ACTIVE_CTRL:
        print('ctrl')
    print(str(x)+','+str(y))

    if state == GLUT_UP:
        mouse_info = None

    if state == GLUT_DOWN:
        if button == 3: # scroll up
            pass
        elif button == 4: # scroll down
            pass
        else:
            mouse_info = MouseInfo(button,x,y)

def motion(x, y):
    print(str(x)+','+str(y))

def init(width, height):
    glClearColor(0.25, 0.25, 0.25, 1.0)
    glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ##set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(500,500)  # window size
    glutInitWindowPosition(0,0)  # window position

    glutCreateWindow(b'test')

    #camera
    # camera_lookat(None,0.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glutDisplayFunc(display) # draw callback function
    glutReshapeFunc(reshape) # resize callback function
    glutKeyboardFunc(key)    # keyboard callback function
    glutMouseFunc(mouse)     # mouse callback function
    glutMotionFunc(motion)   # mouse drag callback function

    init(300, 300)
    glutMainLoop()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

from collections import namedtuple


WindowInfo = namedtuple('WindowInfo', ('x', 'y', 'w', 'h'))
MouseInfo = namedtuple('MouseInfo', ('button', 'x', 'y', 'mode'))

# global
viewpoint_info = None
camera_info = None
mouse_info = None

# camera pose
def cameraSet(x,y,z,pan,tilt,roll):
    global camera_info
    camera_info = [0.0, 0.0, 1.0, 0.0,
                   1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0 ]
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(camera_info)

    glRotated(-tilt, 0.0, 1.0, 0.0)
    glRotated(-roll, 1.0, 0.0, 0.0)
    glRotated(-pan,  0.0, 0.0, 1.0)
    glTranslated(-x, -y, -z)
    # glGetDoublev(GL_MODELVIEW_MATRIX, camera_info)
    # todo:
    # オリジナルのopenglの関数と引数，戻り値とかが違うらしい
    cam = glGetDoublev(GL_MODELVIEW_MATRIX)
    print(camera_info)
    print(cam)

def cameraRotate(angle,x,y,z):
    global camera_info
    print('rotate')
    print(camera_info)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(angle, x, y, z)
    glMultMatrixd(camera_info)
    glGetDoublev(GL_MODELVIEW_MATRIX, camera_info)

def cameraRotateLock(angle,x,y,z):
    global camera_info
    ax = camera_info[0]*x + camera_info[1]*y + camera_info[2]*z;
    ay = camera_info[4]*x + camera_info[5]*y + camera_info[6]*z;
    az = camera_info[8]*x + camera_info[9]*y + camera_info[10]*z;
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(camera_info)
    glRotated(angle, ax, ay, az);
    glGetDoublev(GL_MODELVIEW_MATRIX, camera_info)

def cameraMove(x,y,z):
    global camera_info
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(camera_info)
    glTranslated(-x, -y, -z)
    glGetDoublev(GL_MODELVIEW_MATRIX, camera_info)

def cameraRelMove(x,y,z):
    global camera_info
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(-y, -z, -x)
    glMultMatrixd(camera_info)
    glGetDoublev(GL_MODELVIEW_MATRIX, camera_info)






def camera_lookat(c, x,y,z, cx,cy,cz, ux,uy,uz):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(x, y, z, cx, cy, cz, ux, uy, uz)

def drawTeapot():
    glColor3f(1.0, 0.0, 0.0)
    glutWireTeapot(1.0)   # wireframe
    # glutSolidTeapot(1.0)  # solid

def display():
    global camera_info
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(camera_info);
    # camera_lookat(None,0.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #draw
    drawTeapot()

    glutSwapBuffers()

def reshape(width, height):
    global viewpoint_info
    glViewport(0, 0, width, height)
    glScissor(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

    viewpoint_info = WindowInfo(0,0,width,height)

def key(key,x,y):
    print(key)
    if key == b'q' or key == b'Q':
        sys.exit()

def mouse(button,state,x,y):
    global mouse_info
    if state == GLUT_UP:
        mouse_info = None

    if state == GLUT_DOWN:
        if button == 3: # scroll up
            pass
        elif button == 4: # scroll down
            pass
        else:
            mouse_info = MouseInfo(button,x,y,glutGetModifiers())

def mouseDrag(x,y):
    global viewpoint_info
    global mouse_info
    dx =  float(x - mouse_info.x) / viewpoint_info.h
    dy = -float(y - mouse_info.y) / viewpoint_info.w
    c = mouse_info.mode & GLUT_ACTIVE_CTRL
    if mouse_info.button == GLUT_LEFT_BUTTON:
        r = 180 * math.sqrt(dx*dx + dy*dy)
        cameraRotateLock(r, -dy, dx, 0) if c else cameraRotate(r, -dy, dx, 0)
    elif mouse_info.button == GLUT_RIGHT_BUTTON:
        cameraRelMove(0, dx, dy) if c else cameraMove(0, dx, dy)
    elif mouse_info.button == GLUT_MIDDLE_BUTTON:
        cameraRelMove(-dy, 0, 0) if c else cameraMove(-dy, 0, 0)
    mouse_info = MouseInfo(mouse_info.button,x,y,mouse_info.mode)
    glutPostRedisplay()

def idle():
    pass

def init(width, height):
    glClearColor(0.25, 0.25, 0.25, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_CULL_FACE)
    glEnable(GL_SCISSOR_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    cameraSet(5.0,0,0,0,0,0)

    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def main():
    w = 500
    h = 500
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(w,h)  # window size
    glutInitWindowPosition(0,0)  # window position

    glutCreateWindow(b'test')

    glutDisplayFunc(display) # draw callback function
    glutReshapeFunc(reshape) # resize callback function
    glutKeyboardFunc(key)    # keyboard callback function
    glutMouseFunc(mouse)     # mouse callback function
    glutMotionFunc(mouseDrag)   # mouse drag callback function
    glutIdleFunc(idle)

    init(w, h)
    #camera
    # camera_lookat(None,0.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glutMainLoop()

if __name__ == "__main__":
    main()

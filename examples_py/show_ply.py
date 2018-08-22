from OpenGL.GL import *
from OpenGL.GLUT import *

import numpy as np

import sys
sys.path.append("../python")
import dfm2
#import dfm2.gl

def glut_print(x, y, font, text, color):
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  glColor3f(color[0], color[1], color[2])
  glRasterPos2f(x, y)
  for ch in text:
    glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

def draw_sphere(pos, rad, color):
  if pos is None:
    return
  glColor3d(color[0], color[1], color[2])
  glTranslatef(+pos[0], +pos[1], +pos[2])
  glutSolidSphere(rad, 32, 32)
  glTranslatef(-pos[0], -pos[1], -pos[2])

camera = None
modifier = 0
mouse_x = 0.0
mouse_y = 0.0

mshtri = None
####

def display():
  global camera
  glClearColor(0.3, 0.5, 0.8, 1.0)
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  ####
  camera.set_gl_camera(600, 600)
  ####
  glColor3d(1, 0, 0)
#  glutSolidTeapot(0.1)
  mshtri.Draw()

  glLineWidth(3)
  dfm2.gl.draw_axis(size=0.5)
  glutSwapBuffers()


def reshape(width, height):
  glViewport(0, 0, width, height)


def idle():
  glutPostRedisplay()


def keyboard(bkey, x, y):
  global edit_mode, view_mode, view_face_mode, path_csv_img
  global scale, quat, trans
  key = bkey.decode("utf-8")
  if key == 'q':
    exit()
  glutPostRedisplay()

def special(key, x, y):
  global camera
  if key == int(GLUT_KEY_PAGE_UP):
    camera.scale *= 1.03
  elif key == int(GLUT_KEY_PAGE_DOWN):
    camera.scale *= (1.0 / 1.03)
  glutPostRedisplay()


def mouse(button, state, x, y):
  global modifier, mouse_x, mouse_y
  modifier = glutGetModifiers()
  mouse_x, mouse_y = dfm2.gl.mouse(x, y)
  glutPostRedisplay()


def motion(x, y):
  global camera, mouse_x, mouse_y
  if modifier == 1:
    mouse_x, mouse_y, camera.quat, camera.trans = dfm2.gl.motion("ROT", x, y, mouse_x, mouse_y, camera.quat,
                                                                    camera.trans, camera.view_height)
  if modifier == 2:
    mouse_x, mouse_y, camera.quat, camera.trans = dfm2.gl.motion("TRANS", x, y, mouse_x, mouse_y, camera.quat,
                                                                        camera.trans, camera.view_height)
  glutPostRedisplay()


def main():
  global camera, mshtri

  glutInit()
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # zBuffer
  glutInitWindowSize(600, 600)
  glutInitWindowPosition(100, 100)
  glutCreateWindow("Visualizzatore_2.0")

  # Register callbacks
  glutReshapeFunc(reshape)
  glutDisplayFunc(display)
  glutMouseFunc(mouse)
  glutMotionFunc(motion)
  glutKeyboardFunc(keyboard)
  glutSpecialFunc(special)
  glutIdleFunc(idle)

  camera = dfm2.gl.Camera(1.0)
  mshtri = dfm2.dfm2.CMeshTri();
  mshtri.Read("../test_inputs/bunny_1k.ply")
  mshtri.ScaleXYZ(0.01)

  ####
  # Turn the flow of control over to GLUT
  glutMainLoop()


if __name__ == "__main__":
  main()

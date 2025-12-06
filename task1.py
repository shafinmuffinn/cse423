from OpenGL.GL import *     # Core OpenGL functions (drawing, colors, etc.)
from OpenGL.GLUT import *   # GLUT library (window creation, display, loop)
from OpenGL.GLU import *    # OpenGL Utility Library (projection utilities)

import  math, random, time
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720

def draw_box(x,y,w,h):
    glBegin(GL_QUADS)
    glVertex2d(x,y)
    glVertex2d(x,y+h)
    glVertex2d(x+w,y+h)
    glVertex2d(x+w,y)
    glEnd()

def draw_triangle(x,y,w,h):
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0) 
    glVertex2d(x,y)
    
    glVertex2d(x+w,y)
    glColor3f(1, 1, 1)
    glVertex2d(x+(w//2),y+h)
    glEnd()
def draw_triangle_house(x, y, w, h):
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.2, 0.5) 
    glVertex2d(x,y)
    
    glVertex2d(x+w,y)
    glVertex2d(x+(w//2),y+h)
    glEnd()
    
def draw_window_lines(x, y, w, h):
    glColor3f(0.2, 0.2, 0.2)
    glLineWidth(2)
    glBegin(GL_LINES)
    # vertical
    glVertex2f(x + w / 2, y)
    glVertex2f(x + w / 2, y + h)
    # horizontal
    glVertex2f(x, y + h / 2)
    glVertex2f(x + w, y + h / 2)
    glEnd()

def house():
    glColor3f(1,1,1)
    draw_box(-100, -100, 200, 100)

    
    glColor3f(0.5,0.8,1)
    draw_box(-60, -60, 20, 30)
    draw_window_lines(-60, -60, 20, 30)

    glColor3f(0.5,0.8,1)
    draw_box(40, -60, 20, 30)
    draw_window_lines(40, -60, 20, 30)
    #glColor3f(0.5,0.8,1)
    #glColor3f(0.5,0.8,1)

    draw_box(-20, -100, 40, 70)
    glColor3f(1, 1, 0)
    draw_box(10, -65, 5,5)
    glColor3f(0, 0.3, 0.3)
    draw_triangle_house(-120,0,240,80)
    

def grass():
    
    global WINDOW_WIDTH
    glColor3f(0,1,0)
    for i in range(-250,WINDOW_WIDTH,40):
        draw_triangle(i,-20,40,80)
        # glBegin(GL_QUADS)
        # glColor3f(0.0, 0.4, 0.0)   # dark base
        # glVertex2f(-i, -2)
        # glVertex2f(250, -250)
        # glColor3f(0.4, 1.0, 0.4)   # top fade
        # glVertex2f(250, 0)
        # glVertex2f(-250, 0)
        # glEnd()

rain_positions = []

def init_rain():


    for i in range(100):
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        speed = random.uniform(25, 28)
        color = random.choice([(0.5, 0.5, 1.0),(0.3, 0.8, 1.0)])
        rain_positions.append([x, y, speed, color])

rain_angle = 90
wind = 0.0

def draw_rain():
    global rain_angle
    length = 25
    angle_rad = math.radians(rain_angle)

    glBegin(GL_LINES)
    for x, y, _, color in rain_positions:
        glColor3f(*color)
        dx = length * math.cos(angle_rad)
        dy = length * math.sin(angle_rad)
        glVertex2f(x, y)
        glVertex2f(x + dx, y - dy)
    glEnd()

def update_rain():
    for drop in rain_positions:
        drop[1] -= drop[2]
        drop[0] += wind * 0.5

        if drop[1] < -250:
            drop[1] = random.randint(250, 300)
            drop[0] = random.randint(-250, 250)
MAX_WIND = 12
def special_keys(key, x, y):
    global rain_angle, wind
    if key == GLUT_KEY_LEFT:
        wind = max(-MAX_WIND, wind - 1)
        rain_angle += 2
    elif key == GLUT_KEY_RIGHT:
        wind = min(MAX_WIND, wind + 1)
       #wind += 0.6
        rain_angle -= 2
    #print(wind, rain_angle)

    rain_angle = max(60, min(120, rain_angle))

sky_color = [0.05, 0.05, 0.1]

def draw_sky():
    glColor3f(*sky_color)
    draw_box(-250, 20, 500, 500)

def change_sky(daytime=True):
    global sky_color
    step = 0.03
    if daytime:
        target = [0.5, 0.8, 1.0]
        # for i in range(3):
        #     target[i] = sky_color[i] - step
        # sky_color = target
        sky_color = [min(sky_color[i] + step, target[i]) for i in range(3)]
    else:
        target = [0.05, 0.05, 0.1]
        # for i in range(3):
        #     target[i] = sky_color[i] - step
        # sky_color = target
        sky_color = [max(sky_color[i] - step, target[i]) for i in range(3)]


def keyboard_listener(key, x, y):
    if key == b'j':
        change_sky(daytime=True)
    elif key == b'k':
        change_sky(daytime=False)
    glutPostRedisplay()


def display():
    """Main display callback for rendering each frame."""
    #glClearColor(0.8, 10/100, 0.1, 0)
    glClearColor(153/255, 75/255, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    draw_sky() 
    grass()
    house()
    draw_rain()
    glutSwapBuffers() 

def animate():
    update_rain()
    glutPostRedisplay()
    time.sleep(1/60)  

def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"task1: Blank Canvas")
    setup_projection() 
    init_rain()
    glutSpecialFunc(special_keys)
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    

    glutMainLoop()


if __name__ == "__main__":
    main()
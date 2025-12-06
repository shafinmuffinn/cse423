from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

balls_array = []
speed = 1.0
blink = False
balls_paused = False
last_blink_time = 0
ball_visibility = True


def draw_points():
    global ball_visibility
    if blink and not ball_visibility:
        return

    glPointSize(8)
    glBegin(GL_POINTS)
    for x, y, _, _, r, g, b in balls_array:
        glColor3f(r, g, b)
        glVertex2f(x, y)
    glEnd()

def update_points():
    global balls_array, speed
    boundary_l_r = 250
    boundary_t_b = 250

    for p in balls_array:
        p[0] += p[2] * speed
        p[1] += p[3] * speed

        if p[0] > boundary_l_r or p[0] < -boundary_l_r:
            p[2] *= -1
        if p[1] > boundary_t_b or p[1] < -boundary_t_b:
            p[3] *= -1

def mouse(btn, state, x, y):
    global blink

    if balls_paused:
        return

    if btn == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        x_world = (x / WINDOW_WIDTH) * 500 - 250
        y_world = ((WINDOW_HEIGHT - y) / WINDOW_HEIGHT) * 500 - 250


        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        color = [random.random(), random.random(), random.random()]

        balls_array.append([x_world, y_world, dx, dy, *color])

    elif btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
        # true = not true, false
def special_keys(key, x, y):
    global speed
    if balls_paused:
        return
    if key == GLUT_KEY_UP:
        speed += 0.2
    elif key == GLUT_KEY_DOWN:
        speed = max(0.2, speed - 0.2)

def keyboard(key, x, y):
    global balls_paused
    if key == b' ':
        balls_paused = not balls_paused

def handle_blink():
    global blink, ball_visibility, last_blink_time
    if blink is False:
        ball_visibility = True
        return

    current = time.time()
    if current - last_blink_time >= 0.5:
        ball_visibility = not ball_visibility
        last_blink_time = current
    #print(last_blink_time)
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_points()

    glutSwapBuffers()

def animate():
    if not balls_paused:
        handle_blink()
        update_points()

    glutPostRedisplay()
    time.sleep(1/60)

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    glutCreateWindow(b"task2: amazing box")
    glClearColor(0, 0, 0, 1)
    setup_projection()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()



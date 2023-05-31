import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

vertices1 = [[-0.5, 0.5], [-0.5, -0.5], [-1.5, -0.5], [-1.5, 0.5]]
edges1 = ((0, 1), (1, 2), (2, 3), (3, 0))

vertices2 = [[0.5, 2], [0.5, 1], [-0.5, 1], [-0.5, 2]]
edges2 = ((0, 1), (1, 2), (2, 3), (3, 0))

vertices3 = [[1.5, 0.5], [1.5, -0.5],[0.5, -0.5],[0.5, 0.5]]
edges3 = ((0, 1), (1, 2), (2, 3), (3, 0))

vertices1 = np.array(vertices1, dtype=np.float32)
vertices2 = np.array(vertices2, dtype=np.float32)
vertices3 = np.array(vertices3, dtype=np.float32)


tex_coords = [[1, 1], [1, 0], [0, 0], [0, 1]]

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1) # type: ignore
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def draw(vertices, edges, tex_coords, texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    for e in edges:
        for vertex in e:
            glTexCoord2fv(tex_coords[vertex])
            glVertex2fv(vertices[vertex])

    glEnd()
    glDisable(GL_TEXTURE_2D)

def main():
    flag = True

    pygame.init()
    width, height = 1366, 768 #800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    # glRotatef(0,0,1,1)

    # Load textures
    texture1 = load_texture("textures/face0.png")
    texture2 = load_texture("textures/face1.png")
    texture3 = load_texture("textures/face2.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            x, y = pygame.mouse.get_pos()
            x = 1.2*(x-(width/2))/(width/4)
            y = 1.2*(-y + (height/2))/(height/4)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_s:
                    if flag:
                        texture1 = load_texture("textures/real.png")
                        texture2 = load_texture("textures/real2.png")
                        texture3 = load_texture("textures/real3.png")
                        flag = not flag

                    else:              
                        texture1 = load_texture("textures/face0.png")
                        texture2 = load_texture("textures/face1.png")
                        texture3 = load_texture("textures/face2.png")
                        flag = not flag
                    
                match event.key:
                    case pygame.K_1:
                        vertices1[3] = np.array([x, y])
                    case pygame.K_2:
                        vertices1[0] = np.array([x, y])
                    case pygame.K_3:
                        vertices1[2] = np.array([x, y])
                    case pygame.K_4:
                        vertices1[1] = np.array([x, y])
                        
                    case pygame.K_5:
                        vertices2[3] = np.array([x, y])
                    case pygame.K_6:
                        vertices2[0] = np.array([x, y])
                    case pygame.K_7:
                        vertices2[2] = np.array([x, y])
                    case pygame.K_8:
                        vertices2[1] = np.array([x, y])
                        
                    case pygame.K_9:
                        vertices3[3] = np.array([x, y])
                    case pygame.K_0:
                        vertices3[0] = np.array([x, y])
                    case pygame.K_a:
                        vertices3[2] = np.array([x, y])
                    case pygame.K_b:
                        vertices3[1] = np.array([x, y])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw(vertices1, edges1, tex_coords, texture1)
        draw(vertices2, edges2, tex_coords, texture2)
        draw(vertices3, edges3, tex_coords, texture3)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()

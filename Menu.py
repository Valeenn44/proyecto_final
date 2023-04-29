import pygame
import sys

# Inicializar pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi Juego")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
fuente_titulo = pygame.font.SysFont(None, 48)
fuente_menu = pygame.font.SysFont(None, 36)

# Textos
titulo = fuente_titulo.render("Mi Juego", True, BLANCO)
opcion1 = fuente_menu.render("Jugar", True, BLANCO)
opcion2 = fuente_menu.render("Opciones", True, BLANCO)
opcion3 = fuente_menu.render("Salir", True, BLANCO)

# Variables de control
opcion_seleccionada = 0
opciones = ["Jugar", "Opciones", "Salir"]

# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif event.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif event.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:
                    print("¡Jugar!")
                elif opcion_seleccionada == 1:
                    print("¡Opciones!")
                elif opcion_seleccionada == 2:
                    pygame.quit()
                    sys.exit()

    # Limpiar pantalla
    screen.fill(NEGRO)

    # Dibujar título
    screen.blit(titulo, (240, 100))

    # Dibujar opciones del menú
    for i, opcion in enumerate(opciones):
        if opcion_seleccionada == i:
            color = BLANCO
        else:
            color = NEGRO
        text = fuente_menu.render(opcion, True, color)
        screen.blit(text, (280, 200 + i * 50))

    # Actualizar pantalla
    pygame.display.flip()
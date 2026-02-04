import pygame
import sys

# -------------------------
# CONFIGURACIÓN GENERAL
# -------------------------
WIDTH, HEIGHT = 1200, 700
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# -------------------------
# INICIALIZACIÓN
# -------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Resonador - Vista 2D")
clock = pygame.time.Clock()

# -------------------------
# LOOP PRINCIPAL
# -------------------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Texto de prueba
    font = pygame.font.SysFont(None, 30)
    text = font.render("Simulación Resonador - En construcción", True, BLACK)
    screen.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()

input("\nPresioná ENTER para cerrar el programa...")

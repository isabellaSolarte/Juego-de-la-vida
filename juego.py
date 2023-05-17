import pygame
import random

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Dimensiones de las células y del tablero
CELULA_TAMANO = 5
TABLERO_COLUMNAS = ANCHO // CELULA_TAMANO
TABLERO_FILAS = ALTO // CELULA_TAMANO

# Colores en RGB para la presentación
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la Vida")

class Celula:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.estado = random.choice([0, 1])  # 0 para muerta, 1 para viva se le da un valor inicial a la célula cuando se crea
        self.vecinos = []

    def dibujar(self):
        color = BLANCO if self.estado == 1 else NEGRO
        pygame.draw.rect(ventana, color, (self.posX * CELULA_TAMANO, self.posY * CELULA_TAMANO, CELULA_TAMANO, CELULA_TAMANO))

    def contar_vecinos_vivos(self):
        return sum(vecino.estado for vecino in self.vecinos) #cantidad de vecinos vivos que tiene la célula

    def actualizar_estado(self):
        vecinos_vivos = self.contar_vecinos_vivos()
        if self.estado == 1:
            if vecinos_vivos < 2 or vecinos_vivos > 3:
                self.estado = 0
        else:
            if vecinos_vivos == 3: #revive
                self.estado = 1

class Tablero:
    def __init__(self):
        self.celulas = []
        #se inicializa el tablero
        for fila in range(TABLERO_FILAS):
            for columna in range(TABLERO_COLUMNAS):
                celula = Celula(columna, fila)
                self.celulas.append(celula)

        # Establecer vecinos de cada célula
        for celula in self.celulas:
            for dx in [-1, 0, 1]:#posiciones relativas de la célula
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: #descartamos si se encuentra un vecino de mi mismo
                        continue
                    vecino_x = (celula.posX + dx + TABLERO_COLUMNAS) % TABLERO_COLUMNAS
                    vecino_y = (celula.posY + dy + TABLERO_FILAS) % TABLERO_FILAS
                    vecino = self.celulas[vecino_y * TABLERO_COLUMNAS + vecino_x]#se tiene en cuenta la célula vecina con base a las coordenadas X y Y
                    celula.vecinos.append(vecino)

    def dibujar(self):
        for celula in self.celulas:
            celula.dibujar()

    def actualizar_estado(self):
        for celula in self.celulas:
            celula.actualizar_estado()

class Juego:
    def __init__(self):
        self.tablero = Tablero()

    def ejecutar(self):
        reloj = pygame.time.Clock()
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            ventana.fill(NEGRO)

            self.tablero.dibujar()
            #aplicación de la mutación
            self.tablero.actualizar_estado()

            pygame.display.flip()
            reloj.tick(20)  # Velocidad de actualización

juego = Juego()
juego.ejecutar()
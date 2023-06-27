import pygame, random
from constantes import *
#from nivel_1 import espada, grupo_plataformas

def obtener_rectangulos(principal: pygame.Rect):
    diccionario = {}
    diccionario["main"] = principal
    diccionario["bottom"] = pygame.Rect(principal.left, principal.bottom - 10, principal.width, 10)
    diccionario["right"] = pygame.Rect(principal.right -2, principal.top, 2, principal.height)
    diccionario["left"] = pygame.Rect(principal.left, principal.top, 2, principal.height)
    diccionario["top"] = pygame.Rect(principal.left, principal.top, principal.width, 6)
    
    return diccionario

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = imagen
        self.image = pygame.image.load(imagen)
        self.image = pygame.transform.scale(self.image, (120, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones):
        super().__init__()
        self.animaciones = animaciones
        self.contador_pasos = 0
        self.velocidad = 10
        self.posicion_actual_x = 0
        self.imagenes_reescaladas = imagenes_reescaladas
        self.rect = self.animaciones[self.posicion_actual_x].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)
        self.que_hace = "Quieto"
        self.desplazamiento_y = 0
        self.desplazamiento_x = 0
        self.esta_saltando = False
        self.tiene_escudo = False

    def update(self, espada):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < W - self.velocidad:
            self.que_hace = "Derecha"
            self.rect.x += self.velocidad
        elif keys[pygame.K_LEFT] and self.rect.left > self.velocidad:
            self.que_hace = "Izquierda"
            self.rect.x -= self.velocidad
        elif keys[pygame.K_UP] and not self.esta_saltando:
            self.que_hace = "Salta"
            self.desplazamiento_y = -20
            self.esta_saltando = True
        elif keys[pygame.K_SPACE]:
            self.que_hace = "Atacando"
            espada.atacando = True 
        else:
            self.que_hace = "Quieto"
            self.desplazamiento_x = 0
        
        self.desplazamiento_y += 1

        if self.que_hace != "Salta":
            self.desplazamiento_y += gravedad

        self.rect.x += self.desplazamiento_x
        for lado in self.lados:
            if lado == "top":
                self.rect.y += self.desplazamiento_x

        if self.rect.bottom >= H:
            self.rect.bottom = H
            self.esta_saltando = False
            self.desplazamiento_y = 0
        
        self.lados = obtener_rectangulos(self.rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones):
        super().__init__()
        self.animaciones = animaciones
        self.contador_pasos = 0
        self.velocidad = 3
        self.direccion = 1
        self.posicion_actual_x = 0
        self.rect = self.animaciones[self.posicion_actual_x].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)
        self.que_hace = "quieto"
        self.cayendo = True

    def update(self, grupo_plataformas):
        if self.cayendo:
            self.rect.y += self.velocidad + 5  
            self.que_hace = "quieto"   
            colision_plataforma = pygame.sprite.spritecollide(self, grupo_plataformas, False)
            if colision_plataforma:
                self.cayendo = False  
                plataforma = colision_plataforma[0]  
                self.rect.bottom = plataforma.rect.top  
                return

        self.rect.x += self.velocidad * self.direccion
        if self.direccion == 1:
            self.que_hace = "izquierda"
        elif self.direccion == -1:
            self.que_hace = "derecha"

        if self.rect.left <= 0 or self.rect.right >= W:
            self.direccion *= -1
        if pygame.sprite.spritecollide(self, grupo_plataformas, False):
            self.direccion *= -1

        if self.rect.bottom >= piso.top:
            self.rect.bottom = piso.top  
            self.cayendo = False  

        self.lados = obtener_rectangulos(self.rect)

    def generar_enemigos(cantidad):
        enemigos = pygame.sprite.Group()

        for _ in range(cantidad):
            x = random.randint(0, W - 50)  
            y = random.randint(-200, -50)  
            enemigo = Enemigo(x, y, enemigo_camina)  
            enemigos.add(enemigo)
        return enemigos
    
class Espada(pygame.sprite.Sprite):
    def __init__(self, x, y, z, animacion_ataque):
        super().__init__()
        self.animacion_ataque = animacion_ataque
        self.x = x
        self.y = y
        self.z = z
        self.rect = pygame.Rect(x, y, z, z)
        self.atacando = False
        self.contador_pasos = 0

    def atacar(self):
        self.atacando = True

    def animar_ataque(self, pantalla):
        largo = len(self.animacion_ataque)
        self.contador_pasos += 1
        if self.contador_pasos >= largo:
            self.contador_pasos = 0

        pantalla.blit(self.animacion_ataque[self.contador_pasos], self.rect.topleft)

class Orbe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.image.load("orbes/11.png"),
            pygame.image.load("orbes/15.png"),
            pygame.image.load("orbes/19.png"),
            pygame.image.load("orbes/20.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)

class Boss(pygame.sprite.Sprite):
    def __init__(self, imagenes_enemigo, imagen_proyectil):
        super().__init__()
        self.imagenes = imagenes_enemigo
        self.image = self.imagenes[0]
        self.rect = self.image.get_rect()
        self.rect.x = W - self.rect.width  
        self.rect.y = H // 2 - self.rect.height // 2  
        self.proyectil_image = pygame.image.load(imagen_proyectil)
        self.proyectiles = pygame.sprite.Group()
        self.contador_pasos = 0

    def update(self):
        self.proyectiles.update()
        self.contador_pasos += 1
        if self.contador_pasos >= len(self.imagenes):
            self.contador_pasos = 0
        self.image = self.imagenes[self.contador_pasos]

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
        self.proyectiles.draw(pantalla)

    def lanzar_proyectil(self):
        proyectil = Proyectil(self.proyectil_image, self.rect.x, self.rect.y)
        self.proyectiles.add(proyectil)

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, imagen_proyectil, x, y):
        super().__init__()
        self.image = pygame.image.load(imagen_proyectil)
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y  

    def update(self):
        self.rect.x -= velocidad_proyectil

class Boton():
	def __init__(self, imagen, escala, x, y):
		super(Boton, self).__init__()
		self.escala = escala
		self.imagen = pygame.transform.smoothscale(imagen, self.escala)
		self.rect = self.imagen.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clickeado = False

	def actualizar_imagen(self, imagen):
		self.imagen = pygame.transform.smoothscale(imagen, self.escala)

	def renderizar(self, pantalla):
		accionar = False
		posicion = pygame.mouse.get_pos()
		if self.rect.collidepoint(posicion):
			if pygame.mouse.get_pressed()[0] and not self.clickeado:
				accionar = True
				self.clickeado = True

			if not pygame.mouse.get_pressed()[0]:
				self.clickeado = False

		pantalla.blit(self.imagen, self.rect)
		return accionar 
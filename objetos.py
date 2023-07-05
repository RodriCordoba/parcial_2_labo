import pygame, random
from constantes import *

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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < W - self.velocidad:
            self.que_hace = "Derecha"
            self.rect.x += self.velocidad
        elif keys[pygame.K_LEFT] and self.rect.left > self.velocidad:
            self.que_hace = "Izquierda"
            self.rect.x -= self.velocidad
        elif keys[pygame.K_UP]:
            self.que_hace = "Salta"
            self.desplazamiento_y = -20
            self.esta_saltando = True
        elif keys[pygame.K_q]:
            self.que_hace = "Atacando"  
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
    
    def agregar_enemigos(enemigos_actuales, cantidad):
        enemigos = pygame.sprite.Group(enemigos_actuales)

        for _ in range(cantidad):
            x = random.randint(0, W - 50)
            y = random.randint(-200, -50)
            enemigo = Enemigo(x, y, enemigo_camina)
            enemigos.add(enemigo)

        return enemigos
    
class Espada(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.rect = pygame.Rect(x, y, z, z)

class Orbe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("orbes/20.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)

proyectiles_juego = pygame.sprite.Group()  

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen = pygame.image.load("enemigo/62.png")
        self.rect = self.imagen.get_rect()
        self.rect.right = W  
        self.rect.bottom = 450
        self.vida = 5
        self.tiro_delay = 2000
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):

        PANTALLA.blit(self.imagen, self.rect)

    def shoot_proyectil(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.ultimo_tiro >= self.tiro_delay:
            self.ultimo_tiro = tiempo

            proyectil = Proyectil(self.rect.right, self.rect.centery, -5)
            proyectiles_juego.add(proyectil)

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.imagen = pygame.image.load("enemigo/67.png")
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        PANTALLA.blit(self.imagen, self.rect)

        if self.rect.right < 0 or self.rect.left > W:
            self.kill()


class Boton():
    def __init__(self, imagen, escala, x, y):
        super(Boton, self).__init__()
        self.escala = escala
        self.imagen = pygame.transform.smoothscale(imagen, self.escala)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clickeado = False
        self.estado_volumen = True

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
    
    def on_off_volumen(self, pantalla):
        accionar = False
        posicion = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] and not self.clickeado:
                accionar = True
                self.clickeado = True

                self.estado_volumen = not self.estado_volumen
                if self.estado_volumen:
                    pygame.mixer.music.set_volume(0.2)
                else:
                    pygame.mixer.music.set_volume(0.0)

            if not pygame.mouse.get_pressed()[0]:
                self.clickeado = False

        pantalla.blit(self.imagen, self.rect)
        return accionar

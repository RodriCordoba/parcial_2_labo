import pygame
from constantes import *
from objetos import *

#FONDO
fondo = pygame.image.load("fondo_ciudad.jpg")
fondo = pygame.transform.scale(fondo, (W,H))

personaje = Personaje(H/2 -250, 450, personaje_quieto)

piso.top = personaje.rect.bottom
lados_piso = obtener_rectangulos(piso)
plataforma_1 = Plataforma(380, 460, ("fondos/13.png"))
plataforma_2 = Plataforma(1000, 460, ("fondos/14.png"))
lados_plataforma = obtener_rectangulos(plataforma_1.rect)
lados_plataforma_2 = obtener_rectangulos(plataforma_2.rect)
lista_plataformas = [lados_piso, lados_plataforma, lados_plataforma_2]
grupo_plataformas = pygame.sprite.Group()
grupo_plataformas.add(plataforma_1, plataforma_2)

grupo_enemigos = Enemigo.generar_enemigos(3)

espada = Espada(H/2 -230, 430, 40, ataque_espada)
grupo_espadas = pygame.sprite.Group()
grupo_espadas.add(espada)

orbe = Orbe(500, 390)
grupo_orbes = pygame.sprite.Group()
grupo_orbes.add(orbe)

boss_mira_izquierda = girar_imagenes(boss_dispara, True, False)

boss = Boss(boss_mira_izquierda, "enemigo/67.png")
lados_boss = obtener_rectangulos(boss.rect)

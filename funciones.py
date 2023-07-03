import pygame, sys, time
from objetos import *
from nivel_1 import *
#from nivel_2 import *
from modo import *
from base_de_datos import crear_tablas_db, insertar_jugador, obtener_ranking
pygame.init()

def centrar(imagen):
    return (W // 2) - imagen.get_width() // 2

#FONDOS
fondo_opciones = pygame.image.load(UBICACION_FONDO_PAUSA)
fondo_opciones = pygame.transform.smoothscale(fondo_opciones, (W, H))
fondo_ranking = pygame.image.load(UBICACION_FONDO_RANKING)
fondo_ranking = pygame.transform.smoothscale(fondo_ranking, (W, H))
fondo_perdiste = pygame.image.load(UBICACION_FONDO_PERDISTE)
fondo_perdiste = pygame.transform.smoothscale(fondo_perdiste, (W, H))
fondo_iniciar = pygame.image.load(UBICACION_FONDO_INICIO)
fondo_iniciar = pygame.transform.smoothscale(fondo_iniciar, (W, H))
# IMAGENES DE BOTONES
jugar_imagen = pygame.image.load(UBICACION_BOTON_JUGAR)
pausar_imagen = pygame.image.load(UBICACION_BOTON_PAUSA)
ranking_imagen = pygame.image.load(UBICACION_BOTON_RANKING)
salir_imagen = pygame.image.load(UBICACION_BOTON_SALIR)
volver_imagen = pygame.image.load(UBICACION_BOTON_VOLVER)
guardar_imagen = pygame.image.load(UBICACION_BOTON_GUARDAR)
#CREACION DE BOTONES
jugar_boton = Boton(jugar_imagen, (140, 50), 120, H-80)
pausar_boton = Boton(pausar_imagen, (120, 40), 30, H-580)
volver_boton = Boton(jugar_imagen, (100, 34), 780, H-80)
jugar_boton_centrado = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, H-220)
jugar_boton_centrado_menu = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, H-220)

jugar_boton_centrado_inicio = Boton(jugar_imagen, (160, 60), 500, H-310)
ranking_boton_inicio = Boton(ranking_imagen, (140, 50), 280, H-305)
salir_boton_inicio = Boton(salir_imagen, (140, 50), 740, H-305)

volver_boton_centrado_opciones = Boton(volver_imagen, (150, 50), 410, H-220)
salir_boton_opciones = Boton(salir_imagen, (150, 50), 650, H-220)

jugar_boton_centrado_ranking = Boton(jugar_imagen, (150, 50), 310, H-180)
volver_boton_ranking = Boton(volver_imagen, (150, 50), 650, H-180)

guardar_boton_perdiste = Boton(guardar_imagen, (150, 50), 310, H-220)
salir_boton_perdiste = Boton(salir_imagen, (150, 50), 650, H-220)

def iniciar_juego(volumen = 0.2):
    modo_intro = True
    crear_tablas_db()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)

    while modo_intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_intro = False
                    seleccion_jugar(volumen)
                if evento.key == pygame.K_SPACE:
                    audio_jugar.play()
                    modo_intro = False
                    seleccion_jugar(volumen)
        PANTALLA.blit(fondo, (0, 0))

        if jugar_boton_centrado_inicio.renderizar(PANTALLA):
            audio_jugar.play()
            modo_intro = False
            seleccion_jugar(volumen)
        if ranking_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            ranking()
        if salir_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            sys.exit()
        pygame.display.update()

def iniciar_bucle_juego(volumen):
    bucle_de_juego(volumen)
    return False

def seleccion_jugar(volumen):
    modo_empezar_jugar = True
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)

    while modo_empezar_jugar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_empezar_jugar = False
                if evento.key == pygame.K_SPACE:
                    audio_jugar.play()
                    modo_empezar_jugar = iniciar_bucle_juego(volumen)
        PANTALLA.blit(fondo_iniciar, (0, 0))

        pygame.display.flip()

def mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo):
    fuente = pygame.font.SysFont("Arial", 24)
    enemigos_eliminados_texto = fuente.render("Enemigos eliminados: " + str(enemigos_eliminados), True, "Yellow")
    puntuacion_texto = fuente.render("Puntuacion: " + str(puntuacion), True, "Yellow")
    nivel_texto = fuente.render("Nivel: " + str(nivel), True, "Yellow")
    tiempo_texto = fuente.render("Tiempo: " + str(tiempo//1000) + " segundos", True, "Yellow")
    PANTALLA.blit(enemigos_eliminados_texto, (10,H - 70))
    PANTALLA.blit(puntuacion_texto, (10,H - 45))
    PANTALLA.blit(nivel_texto, (700, H - 70))
    PANTALLA.blit(tiempo_texto, (700, H - 45))

def ranking(volumen=0.2):
    modo_ranking = True
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    while modo_ranking:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_ranking = False

        PANTALLA.blit(fondo_ranking, (0, 0))
        ranking = obtener_ranking()
        posiciones = [(350, 250), (350, 300), (350, 350)]
        num_elementos = len(ranking)

        for i in range(3):
            if i < num_elementos:
                nombre, puntuacion = ranking[i]
                if i < 3:
                    x, y = posiciones[i]
                    color_fuente = "White" if i == 0 else "Grey"
                    fuente = pygame.font.SysFont("Arial", 36, bold=True)
                    texto_puesto = f"{i+1}. {nombre}"
                    text_puesto = fuente.render(texto_puesto, True, color_fuente)
                    text_puntuacion = fuente.render(str(puntuacion), True, color_fuente)
                    PANTALLA.blit(text_puesto, (x, y))
                    PANTALLA.blit(text_puntuacion, (x + 250, y))

        if jugar_boton_centrado_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            seleccion_jugar(volumen)
        if volver_boton_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            iniciar_juego(volumen)

        pygame.display.flip()

def pausa(volume_parametro):
    modo_pausa = True
    volumen = volume_parametro
    tiempo_pausa = 0
    tiempo_inicial_pausa = pygame.time.get_ticks()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)    
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)
    esta_arrastrando_mouse = False

    while modo_pausa:
        tiempo_pausa = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_pausa = False
                sys.exit()          
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicion_mouse = pygame.mouse.get_pos()
                    if posicion_mouse[0] >= 200 and posicion_mouse[0] <= 700 and posicion_mouse[1] >= 300 and posicion_mouse[1] <= 325:
                        esta_arrastrando_mouse = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1: 
                    esta_arrastrando_mouse = False
            elif evento.type == pygame.MOUSEMOTION:
                if esta_arrastrando_mouse:
                    posicion_mouse = pygame.mouse.get_pos()
                    volumen = (posicion_mouse[0] - 300) / 400 # Calcula el volumen con la posición del mouse
                    if volumen < 0.0:
                        volumen = 0.0
                    elif volumen > 1.0:
                        volumen = 1.0
                    pygame.mixer.music.set_volume(volumen)
        PANTALLA.blit(fondo_opciones, (0, 0))

        # Renderizar el deslizador
        pygame.draw.rect(PANTALLA, "Grey", (405, 300, 400, 30))
        posicion_slider = int(volumen * 400) + 405 
        pygame.draw.circle(PANTALLA, "Yellow", (posicion_slider, 314), 16) 
        
        if volver_boton_centrado_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
        if salir_boton_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
            sys.exit()
        pygame.display.flip()

        tiempo_actual_pausa = pygame.time.get_ticks()
        tiempo_pausa = tiempo_actual_pausa - tiempo_inicial_pausa

    retorno = {
        "volumen": volumen,
        "tiempo_pausa": tiempo_pausa
    }
    return retorno

def perdiste(puntuacion, volumen):
    modo_perdiste = True
    fuente = pygame.font.SysFont("Arial", 26)
    nombre = ''
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    textbox_rect = pygame.Rect(340, 300, 300,32)

    while modo_perdiste:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_perdiste = False
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 18:
                        nombre += evento.unicode

        PANTALLA.blit(fondo_perdiste, (0, 0))
        pygame.draw.rect(PANTALLA, "White", textbox_rect, 2)

        texto = fuente.render(nombre, True, "White")
        ingresar_nombre_texto = fuente.render("Ingresar nombre:", True, "White")
        PANTALLA.blit(ingresar_nombre_texto, (textbox_rect.x, textbox_rect.y - 30))
        PANTALLA.blit(texto, (textbox_rect.x +5, textbox_rect.y + 5))

        if guardar_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_perdiste = False
            insertar_jugador(nombre, puntuacion)
            ranking(volumen)
        if salir_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_perdiste = False
            sys.exit()
        
        pygame.display.flip()

def aplicar_gravedad(pantalla, personaje_animacion, rectangulo_personaje: pygame.Rect, pisos: pygame.Rect):
    if personaje.esta_saltando:
        animar_personaje(pantalla, rectangulo_personaje["main"], personaje_animacion)

        for lado in rectangulo_personaje:
            rectangulo_personaje[lado].y += personaje.desplazamiento_y

        if personaje.desplazamiento_y + gravedad < limite_velocidad_caida:
            personaje.desplazamiento_y += gravedad
        
    for plataforma in pisos:
        if rectangulo_personaje["bottom"].colliderect(plataforma["top"]):
            personaje.esta_saltando = False
            personaje.desplazamiento_y = 0
            rectangulo_personaje["main"].bottom = plataforma["main"].top + 1
            break
        else:
            personaje.esta_saltando = True

def mover(rectangulo: pygame.rect, velocidad):
    for lado in rectangulo:
        rectangulo[lado].x += velocidad

def animar_personaje(pantalla, rectangulo, accion):
    largo = len(accion)
    if personaje.contador_pasos >= largo:
        personaje.contador_pasos = 0

    pantalla.blit(accion[personaje.contador_pasos], rectangulo)
    personaje.contador_pasos += 1

def actualizar_pantalla(pantalla, que_hace, lados_personaje, velocidad, plataformas, que_hace_enemigo, lados_enemigo):
    pantalla.blit(fondo, (0,0))
    for plataforma in grupo_plataformas:
        pantalla.blit(plataforma.image, plataforma.rect)
    pantalla.blit(orbe.image, orbe.rect)
    #animar_personaje(pantalla, orbe.rect, orbe.images)

    match que_hace:
        case "Derecha":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, lados_personaje["main"], personaje_camina)
            mover(lados_personaje, velocidad)
        case "Izquierda":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, lados_personaje["main"], personaje_camina_izquierda)
            mover(lados_personaje, velocidad*-1)
        case "Salta":
            if not personaje.esta_saltando:
                personaje.esta_saltando = True
                personaje.desplazamiento_y = potencia_salto
        case "Quieto":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, lados_personaje["main"], personaje_quieto)
        case "Atacando":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, lados_personaje["main"], ataque_espada)
                personaje.atacando = False
    match que_hace_enemigo:
        case "derecha":
            animar_personaje(pantalla, lados_enemigo["main"], enemigo_camina)
        case "izquierda":
            animar_personaje(pantalla, lados_enemigo["main"], enemigo_camina_izquierda)
        case "quieto":
            animar_personaje(pantalla, lados_enemigo["main"], enemigo_quieto)  
    aplicar_gravedad(pantalla, personaje_salta, lados_personaje, plataformas)

def animar_muerte_enemigo(pantalla, enemigo_muere, rectangulo_enemigo): 
    global contador_muerte
    largo = len(enemigo_muere)
    if contador_muerte >= largo:
        return

    pantalla.blit(enemigo_muere[contador_muerte], rectangulo_enemigo)
    contador_muerte += 1
    pygame.display.flip()
    pygame.time.delay(100)
def eliminar_enemigo(enemigo):
    enemigo.x = -1000
    enemigo.y = -1000

def verificar_colisiones(rectangulo_personaje, rectangulo_enemigo, perdiste_texto, puntuacion, volumen, rectangulo_espada):
    retorno = True
    if rectangulo_personaje.colliderect(orbe.rect):
        personaje.tiene_escudo = True
        eliminar_enemigo(orbe.rect)
        print("escudo")
        puntuacion += 1

    if rectangulo_personaje.colliderect(rectangulo_enemigo) and personaje.tiene_escudo==False:
        print("Personaje eliminado!")
        PANTALLA.blit(fondo_perdiste, (0,0))
        PANTALLA.blit(perdiste_texto, (450, 250))
        pygame.display.flip()
        time.sleep(3)
        perdiste(puntuacion, volumen)
        retorno = False
    elif rectangulo_personaje.colliderect(rectangulo_enemigo) and personaje.tiene_escudo==True:
        print("ataque bloqueado")
        personaje.tiene_escudo = False
    elif personaje.que_hace == "Atacando" and rectangulo_enemigo.colliderect(rectangulo_espada):
        animar_muerte_enemigo(PANTALLA, enemigo_muere, rectangulo_enemigo)
        eliminar_enemigo(rectangulo_enemigo)
        print("Enemigo eliminado por ataque de espada!")
        puntuacion += 1
    return retorno

def bucle_de_juego(volumen_parametro = 0.2):
    #MUSICA
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    volumen = volumen_parametro
    pygame.mixer.music.set_volume(volumen)
    #TEXTO
    fuente = pygame.font.SysFont("Arial", 100)
    perdiste_texto = fuente.render("Perdiste!", 0, "Red")
    #FONDO
    fondo = pygame.image.load("fondo_ciudad.jpg")
    fondo = pygame.transform.scale(fondo, (W,H))
    #FPS
    FPS = 15
    RELOJ = pygame.time.Clock()
    tick = pygame.USEREVENT + 0
    pygame.time.set_timer(tick, 100)
    #PERSONAJE
    personaje = Personaje(H/2 -250, 450, personaje_quieto)
    #PLATAFORMAS
    piso.top = personaje.rect.bottom
    lados_piso = obtener_rectangulos(piso)
    plataforma_1 = Plataforma(380, 460, ("fondos/13.png"))
    plataforma_2 = Plataforma(1000, 460, ("fondos/14.png"))
    lados_plataforma = obtener_rectangulos(plataforma_1.rect)
    lados_plataforma_2 = obtener_rectangulos(plataforma_2.rect)
    lista_plataformas = [lados_piso, lados_plataforma, lados_plataforma_2]
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(plataforma_1, plataforma_2)
    #ENEMIGO
    grupo_enemigos = Enemigo.generar_enemigos(2)
    #ESPADA
    # espada = Espada(H/2 -230, 430, 40, ataque_espada)
    # grupo_espadas = pygame.sprite.Group()
    # grupo_espadas.add(espada)
    #personaje.atacando = False
    x = H/2 -230
    y = 430
    z = 40
    rectangulo_espada = pygame.Rect(x,y,z,z)
    lados_espada = obtener_rectangulos(rectangulo_espada)
    #ORBE
    orbe = Orbe(500, 390)
    grupo_orbes = pygame.sprite.Group()
    grupo_orbes.add(orbe)
    #PUNTUACION 
    enemigos_eliminados = 0
    nivel = 1
    puntuacion = 0

    juego_corriendo = True
    tiempo = 0

    while juego_corriendo:
        milisegundos = RELOJ.tick(FPS)
        tiempo += milisegundos

        #EVENTOS 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_corriendo = False
                sys.exit(0)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    retorno = pausa(volumen)
                    volumen = retorno['volumen']
                if evento.key == pygame.K_TAB:
                    cambiar_modo()

        personaje.update()
        rectangulo_espada.x = personaje.rect.x +45
        rectangulo_espada.y = personaje.rect.y 
        lados_espada = obtener_rectangulos(rectangulo_espada)
        personaje.esta_saltando = False
        orbe.update()
        grupo_plataformas.update()
        for enemigo in grupo_enemigos:
            verificar_colisiones(personaje.lados["main"], enemigo.lados["main"], perdiste_texto, puntuacion, volumen, rectangulo_espada)
            enemigo.update(grupo_plataformas)
        grupo_plataformas.draw(PANTALLA)


        actualizar_pantalla(PANTALLA, personaje.que_hace, personaje.lados, personaje.velocidad, lista_plataformas, enemigo.que_hace, enemigo.lados)
        if get_mode():
            for lado in personaje.lados:
                pygame.draw.rect(PANTALLA, "Blue", personaje.lados[lado], 2)

            for lado in lados_espada:
                pygame.draw.rect(PANTALLA, "Red", lados_espada[lado], 2)

            for lado in lados_piso:
                pygame.draw.rect(PANTALLA, "Green", lados_piso[lado], 2)

            for lado in lados_plataforma:
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_2[lado], 2)

            for enemigo in grupo_enemigos:
                for lado in enemigo.lados:
                    pygame.draw.rect(PANTALLA, "Cyan", enemigo.lados[lado], 2)

            for lado in orbe.lados:
                pygame.draw.rect(PANTALLA, "Magenta", orbe.lados[lado], 2)

            #for lado in lados_boss:
                #pygame.draw.rect(PANTALLA, "White", lados_boss[lado], 2)

        #BOTON PAUSA
        if pausar_boton.renderizar(PANTALLA):
            retorno = pausa(volumen)
            volumen = retorno['volumen']
            tiempo -= retorno['tiempo_pausa']
            
        mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo)
        pygame.display.flip()

# encoding: UTF-8
# Autor: Andrea Montero Rivas, A01374496
#Descripción = Es un videojuego en el cual tienes que dispararle a los meteoritos que van cayendo.
# Moves la nave con el mouse, y al hacer click la nave dispara verticalmente para eliminar a los meteoritos.
# Cuentas con tres vidas, que se restarán si algun meteorito pega con la nave o si un meteorito llega a la parte inferior de la pantalla.
# La score va sumando si eliminas a un meteorito pero si no le das y la bala alcanza el alto de la pantalla se restará un punto.


from random import randint
import pygame

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))

# Colores
BLANCO = (255, 255, 255)  # R,G,B en el rango [0,255]
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

def dibujarMenu(ventana, botonJugar):
    imgFdoMenu = pygame.image.load("images/fondoMenu .jpg")
    ventana.blit(imgFdoMenu, (0, 0))
    ventana.blit(botonJugar.image, botonJugar.rect)

def dibujarJuego(ventana, listaEnemigos, listaBalas):
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)

    for bala in listaBalas:
        ventana.blit(bala.image, bala.rect)

def dibujarGameOver(ventana):
    imgFdoGameOver = pygame.image.load("images/GO.jpg")
    ventana.blit(imgFdoGameOver, (0,0))


def actualizarBalas(listaBalas, listaEnemigos, efectoExplota, imgExplota, listaScore):
    for bala in listaBalas:  # NO DEBEN modificar
        bala.rect.top -= 20
        if bala.rect.top <= 0:
            listaBalas.remove(bala)
            if len(listaScore) > 0:
                del listaScore[0]
            continue  # REGRESA al inicio del ciclo
        borrarBala = False
        for k in range(len(listaEnemigos) - 1, -1, -1):
            enemigo = listaEnemigos[k]
            if bala.rect.colliderect(enemigo):
                listaScore.append(enemigo)
                ventana.blit(imgExplota, bala.rect)
                efectoExplota.play()
                listaEnemigos.remove(enemigo)
                borrarBala = True
                break  # TERMINA el ciclo
        if borrarBala:
            listaBalas.remove(bala)

    fuente = pygame.font.SysFont("monospace", 48)
    texto = fuente.render("score = " + str(int(len(listaScore))), 1, BLANCO)
    ventana.blit(texto, (ANCHO - 160, 10))



def generarEnemigoAzar(listaEnemigos, imgEnemigo, listaVidas, nave, efectoExplota, imgExplota):
    cx = randint(0, ANCHO - 30)
    cy = 0
    enemigo = pygame.sprite.Sprite()
    enemigo.image = imgEnemigo
    enemigo.rect = imgEnemigo.get_rect()
    enemigo.rect.left = cx
    enemigo.rect.top = cy + 20
    listaEnemigos.append(enemigo)

    for enemigo in listaEnemigos:
        enemigo.rect.top += 20
        if enemigo.rect.top >= ALTO:
            listaEnemigos.remove(enemigo)
            ventana.blit(imgExplota, enemigo.rect)
            efectoExplota.play()
            if len(listaVidas) > 0:
                del listaVidas[0]
            else:
                dibujarGameOver(ventana)

        elif enemigo.rect.colliderect(nave):
            listaEnemigos.remove(enemigo)
            ventana.blit(imgExplota, nave)
            efectoExplota.play()
            if len(listaVidas) > 0:
                del listaVidas[0]
            else:
                dibujarGameOver(ventana)


def moverNave(imgNave, widthNave, heightNave):   #funcion para mover la imagen de la nave
    #global drag, x, y
    xm, ym = pygame.mouse.get_pos()
    x = xm - (widthNave/2)  #WidthNave/ 2 para centrar el mouse en la imagen.
    y = ym - (heightNave/2)
    nave = pygame.sprite.Sprite()
    nave.image = imgNave
    nave.rect = imgNave.get_rect()
    nave.rect.left = x
    nave.rect.top = y-10
    return nave.image, nave.rect

def mostrarVidas(listaVidas, imgVida):
    for vida in range(len(listaVidas)):
        imgVida_rect = imgVida.get_rect()
        imgVida_rect.x = 30 * vida
        imgVida_rect.y = 0
        ventana.blit(imgVida, imgVida_rect)

def dibujar():
    # Ejemplo del uso de pygame
    pygame.init()  # Inicializa pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana de dibujo
    reloj = pygame.time.Clock()  # Para limitar los fps
    termina = False  # Bandera para saber si termina la ejecución

    estado = "menu"  # jugando, fin
    # Cargar imágenes
    imgBtnJugar = pygame.image.load("images/botonJugar .png")
    # Sprite
    botonJugar = pygame.sprite.Sprite()
    botonJugar.image = imgBtnJugar
    botonJugar.rect = imgBtnJugar.get_rect()
    botonJugar.rect.left = ANCHO // 2 - botonJugar.rect.width // 2
    botonJugar.rect.top = ALTO // 2 - botonJugar.rect.height // 2

    #explocion
    imgExplota = pygame.image.load("images/regularExplosion02.png")

    # Enemigos
    listaEnemigos = []
    imgEnemigo = pygame.image.load("images/enemigo.png")

    #nave
    imgNave = pygame.image.load('images/nave.png')
    widthNave = 60
    heightNave = 70


    # Vidas
    imgVida = pygame.image.load("images/vida.png")
    listaVidas = []
    listaVidas.append(imgVida)
    listaVidas.append(imgVida)
    listaVidas.append(imgVida)

    # Balas
    listaBalas = []
    imgBala = pygame.image.load("images/bala.png")

    # Tiempos
    timer = 0

    # MUSICA de fondo
    pygame.mixer.init()
    pygame.mixer.music.load("images/musicaFondo2.mp3")
    pygame.mixer.music.play(-1)
    efectoDisparo = pygame.mixer.Sound("images/shoot.wav")
    efectoExplota = pygame.mixer.Sound("images/expl3.wav")

    # fondo
    imagenFondo = pygame.image.load("images/fondo.jpg")
    y = 0

    #score
    listaScore = []

    while not termina:
        # Procesa los eventos que recibe
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # El usuario hizo click en el botón de salir
                termina = True

            elif evento.type == pygame.MOUSEBUTTONDOWN:  # El usuario hizo click
                xm, ym = pygame.mouse.get_pos()
                if estado == "menu":
                    xb, yb, anchoB, altoB = botonJugar.rect
                    if xm >= xb and xm <= xb + anchoB:
                        if ym >= yb and ym <= yb + altoB:
                            # Cambiar de ventana
                            estado = "jugando"

                elif estado == "jugando":
                    efectoDisparo.play()
                    bala = pygame.sprite.Sprite()
                    bala.image = imgBala
                    bala.rect = imgBala.get_rect()
                    bala.rect.left = xm - bala.rect.left
                    bala.rect.top = ym - bala.rect.height
                    listaBalas.append(bala)

                elif estado == "game_over":
                    quit()

        # Borrar pantalla
        ventana.fill(BLANCO)
        ventana.blit(imagenFondo, (0, y-ALTO))
        ventana.blit(imagenFondo, (0, y))

        y += 5
        if y >= ALTO:
            y = 0

        # Dibujar, aquí haces todos los trazos que requieras
        if estado == "menu":
            dibujarMenu(ventana, botonJugar)

        elif estado == "jugando":

            mostrarVidas(listaVidas, imgVida)
            ni, nr = moverNave(imgNave, widthNave, heightNave)
            ventana.blit(ni, nr)
            actualizarBalas(listaBalas, listaEnemigos, efectoExplota, imgExplota, listaScore)
            dibujarJuego(ventana, listaEnemigos, listaBalas)
            # Generar enemigos cada 2 segundos
            timer += 1 / 40
            if timer >= .2:
                timer = 0
                generarEnemigoAzar(listaEnemigos, imgEnemigo, listaVidas, nr, efectoExplota, imgExplota)

            if len(listaVidas) == 0:
                estado = "game_over"


        elif estado == "game_over":
            dibujarGameOver(ventana)


        pygame.display.flip()  # Actualiza trazos
        pygame.display.update()
        reloj.tick(40)  # 40 fps

    pygame.quit()  # termina pygame


def main():
    dibujar()

main()
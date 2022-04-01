from pygame.mixer import pause, stop
from pygame.event import wait
from pytmx.pytmx import TiledMap
from PPlay.animation import*
from typing import*
from PPlay.window import*
from PPlay.gameimage import*
from PPlay.sprite import*
from pytmx.util_pygame import load_pygame
import random
from pygame.locals import *

#Inicializaçao
janela = Window(1920,1080)
janela.set_title("ONE PONG")

fundo = GameImage("Aula/Fundo.jpg")

portal = Sprite("Aula/portal.png",1)
portal.x = random.randint(420,1500)
portal.y = random.randint(240,900)

bola = Sprite("Aula/Bolinha.png",1)
bola.x = (janela.width/2) - (bola.width/2)
bola.y = (janela.height/2) - (bola.height/2)
velbolax = 500
velbolay = 500

barco1 = Sprite("Aula/Bdireita.png",1)
barco1.x = (janela.width/2) - (barco1.width/2)
barco1.y = janela.height - barco1.height
barco2 = Sprite("Aula/Besquerda.png",1)
velbarco = 150


padD = Sprite("Aula/pad1.png", 1)
padD.x = 1862
padD.y = (janela.height/2) - (padD.height/2)

padE = Sprite("Aula/pad1.png", 1)
padE.x = 2
padE.y = (janela.height/2) - (padE.height/2)
velPad = 480

teclado = Window.get_keyboard()
placarE = 0
placarD = 0

relogio = 0
contadorFrames = 0
#GameLoop
while(True):
    ##Entrada de dados
    if(teclado.key_pressed("UP")):
        if(padD.y >= 0):
            padD.y = padD.y - velPad*janela.delta_time()
    if(teclado.key_pressed("DOWN")):
        if((padD.y + padD.height) <= janela.height):
            padD.y = padD.y + velPad*janela.delta_time()
    
    if((padE.y + padE.height) <= janela.height):
        if bola.y > 1.05*padE.y:
            padE.y = padE.y + velPad*janela.delta_time()
    if(padE.y >= 0):
        if bola.y < 1.05*padE.y:
            padE.y = padE.y - velPad*janela.delta_time()

            
    
    ##Update dos Game Objects
    
    bola.x = bola.x + velbolax*janela.delta_time()
    bola.y = bola.y + velbolay*janela.delta_time()
    barco1.x = barco1.x + velbarco*janela.delta_time()
    
    ##Physics
    
    #Colisao dos Pads
    if(padD.collided(bola)):
        bola.x = (janela.width - padD.width) - (1.2*bola.width)
        velbolax = 500
        velbolax = velbolax*(-1.1)
        if(velbolay > 0):
            velbolay = 500
        else:
            velbolay = -500
    if(padE.collided(bola)):
        bola.x = padE.width + (0.2*bola.width)
        velbolax = -500
        velbolax = velbolax*(-1.1) 
        if(velbolay > 0):
            velbolay = 500
        else:
            velbolay = -500

    #Para bola nao sair da tela em cima e embaixo   
    if((bola.y + bola.height) >= janela.height):
        bola.y = janela.height - bola.height
        velbolay = velbolay * (-1)
    if(bola.y <= 0):
        bola.y = 0
        velbolay = velbolay * (-1)

    #Pontuaçao
    if((bola.x + bola.width) > janela.width):
        placarE += 1
    if(bola.x <= 0):
        placarD += 1

    #Recomeço
    if((bola.x + bola.width) > janela.width) or (bola.x < 0): 
        bola.x = (janela.width/2) - (bola.width/2)
        bola.y = (janela.height/2) - (bola.height/2)   
        velbolax = 500
        velbolay = 500
    
    #Portal
    if(portal.collided(bola)):
        velbolax = velbolax * (1.5)
        velbolay = velbolay * (1.5)
        portal.x = random.randint(420,1500)
        portal.y = random.randint(240,900)

    #Barquinho andando na tela
    if((barco1.x + barco1.width) > janela.width):
        velbarco = velbarco*(-1)
        barco1 = Sprite("Aula/Besquerda.png",1)
        barco1.x = janela.width - barco1.width
        barco1.y = janela.height - barco1.height   
    if(barco1.x <= 0):
        velbarco = velbarco*(-1)
        barco1 = Sprite("Aula/Bdireita.png",1)
        barco1.y = janela.height - barco1.height

    #FPS
    relogio += janela.delta_time()
    contadorFrames += 1
    if relogio >= 1:
        print(contadorFrames)
        relogio = 0
        contadorFrames = 0

    
    ##Desenho dos Game Objects
    fundo.draw()
    janela.draw_text(str(placarE)+"         "+str(placarD),710, 20, 170, (255,255,255))
    barco1.draw()
    bola.draw()
    portal.draw()
    padD.draw()
    padE.draw()
    janela.update()
    
##Encerramento
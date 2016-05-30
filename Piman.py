#Copyright 2016 Théotime Dugois and Andrew Pouret

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#IMPORTS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Nous importons les librairies de code nécessaire au programme"""
from random import randint #nous permet d'obtenir une fonction nous donnant un entier aléatoire0
from time import sleep  #nous permet d'avoir un temps de delai dans nos fonctions
import RPi.GPIO as GPIO  #module gérant les ports GPIO du Pi
import pygame #le module pygame possède une des façons les plus simples de jouer un son

#VARIABLES------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""Variables  du jeux"""
sequence = []   #sequence génerée par le programme

userseq = []    #sequence entrée par l'utilisateur

inputpins = [31,33,35] #Pins d'input des boutons

outputpins = [11,13,15] #Pins d'output des LEDS

score = 0

status = False #Status du jeu, "False" s'il n'est pas en marche, utilisé dans tout le programme

"""Variables temps"""
btime = 500  #temps "bouncetime" soit le temps de delai entre chaque détection d'entrée de bouton
stime1 = 0.5 #temps d'affichage led
btime2 = 0.6 #temps de delai minimum entre l'activation des fonctions LEDS.


#Mise en place des Ports GPIOs---------------------------------------------------------------------------------------------------------------------------------------------------------------------

GPIO.setwarnings(False) #évite d'avoir des message d'erreurs constants dans IDLE 

GPIO.cleanup() #met tout les GPIOs sur leur position 0

GPIO.setmode(GPIO.BOARD) #système de numérotation de GPIO

GPIO.setup(11,GPIO.OUT)     #output led rouge
GPIO.setup(13,GPIO.OUT)     #output led verte
GPIO.setup(15,GPIO.OUT)     #output led jaune

GPIO.setup(33,GPIO.IN,pull_up_down = GPIO.PUD_UP)   #input bouton rouge
GPIO.setup(35,GPIO.IN,pull_up_down = GPIO.PUD_UP)   #input bouton vert
GPIO.setup(31,GPIO.IN,pull_up_down = GPIO.PUD_UP)   #input bouton jaune
GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_UP)    #input bouton start/stop
GPIO.setup(8,GPIO.IN,pull_up_down = GPIO.PUD_UP)    #input bouton instructions jeu






#FONCTIONS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##MECANISME PRINCIPAL DU JEU PIMAN-----------------------------------------------------------------------------------------------------------------------------------------------------
                #rappel: 0=rouge, 1=vert, 2=jaune

def addseq():
    """ajoute une valeur a la sequence et allume les leds dans l'ordre correspondant"""
    global sequence
    print("---------------")    #sépare visuellement les séquences, pratique pour debugger
    sequence.append(randint(0,2))   #ajoute une valeur aléatoire a la sequence, soit un entier entre 0 et 2 correspondant à une couleur
    for i in sequence:
    #pour chaque entier de la séquence, cette boucle fait un clignotement de la LED associé ainsi que son son 
        if i == 0:  #rouge
            print('rouge')  #affiche la couleur dans IDLE, pour déboguer plus facilement
            GPIO.output(11,True) #Allume LED
            play_son("red.wav") #joue le son associé à la LED
            GPIO.output(11,False) #Eteint LED

        if i == 1:  #vert
            print('vert')
            GPIO.output(13,True)
            play_son("green.wav")
            GPIO.output(13,False)

        if i == 2:  #jaune
            print('yellow')
            GPIO.output(15,True)
            play_son("yellow.wav")
            GPIO.output(15,False)
        sleep(0.5) #temps d'attente à la fin de la boucle

def checkseq():
    """verifie que les sequences rentrées sont correctes"""
    global sequence,userseq,score #variable en global pour que la fonction utilise et modifie la variable en dehors de la fonction
       
    if len(userseq) <= len(sequence):        #tant que l'utilisateur est en train de rentrer la sequence
                
        if userseq[len(userseq)-1] == sequence[len(userseq)-1]:    #si la sequence est correcte
           
            if userseq == sequence:       #quand la sequence est terminée et correcte
                score += 1
                userseq = []              #efface la sequence entrée
                sleep(0.5)                #laisse une pause à l'utilisateur. Sinon, sa séquence et celle de l'ordinateur s'enchainent trop rapidement
                addseq()                  #lance addseq pour ajouter une valeur a la sequence
            
        else:                                   #si la sequence n'est pas correcte
            lost()
            
    
    
def red(n=None):
    """ajoute rouge a la sequence de l'utilisateur"""
    
    global userseq
    play_son("red.wav") #joue le son du rouge

    GPIO.output(11,True)
    if status == True:
        userseq.append(0)
        checkseq()
        
    sleep(stime1)
    GPIO.output(11,False)
    sleep(btime2)

def green(n=None):
    """ajoute vert a la sequence de l'utilisateur"""
    
    global userseq
    play_son("green.wav") #joue le son du vert 

    GPIO.output(13,True)
    if status == True:
        userseq.append(1)
        checkseq()
        
    sleep(stime1)
    GPIO.output(13,False)
    sleep(btime2)

def yellow(n=None):
    """ajoute jaune a la sequence de l'utilisateur"""
    
    global userseq
    play_son("yellow.wav") #joue le son du jaune 

    GPIO.output(15,True)
    if status == True:
        userseq.append(2)
        checkseq()
        
    sleep(stime1)
    GPIO.output(15,False)
    sleep(btime2)


def lost():
    """fonction acitivée si le joueur perd ou appuye sur le boutton stop quand le jeu est lancé"""
    global status,userseq,sequence,score #utilise et modifie dans tout le programme les variables/listes suivantes
    userseq = [] #la séquence entrée par le joueur est effacée
    sequence = [] #la séquence générée par l'ordinateur est effacée
    play_son("son_perdu.wav") #le son de quand le joueur perd est lancé
    status = False  #le jeu est mis en status "False"
    play_son("son_score/son_score"+str(score)+".wav") #Joue le son du score obtenu, stocké dans le fichier "son_score"
    print ("\n" * 40)
    print('Vous avez perdu')                #Pour débogage
    print ("----------------------------")
    print ("score = %i" % (score)) 
    print ("----------------------------")
    score = 0
    
    #Les lEDs clignotent simultanément pour annoncer que le joueur a perdu
    for counter in range(3):
        for i in outputpins:
            GPIO.output(i,True)
        sleep(0.25)
        for i in outputpins:
            GPIO.output(i,False)
        sleep(0.25)
#    GPIO.cleanup()
    sleep(0.5)
    play_son("son_recommencer.wav") #joue le son qui invite le joueur à recommencer
    
    



def start_stop(n=None):
    """ Fonction permettant de commencer le jeu (lors de l'appui du boutton)
    et de le terminer lorsqu'il est réappuyé"""    
    global status #utilise et modifie le booléen annonçant le status du jeu 
    if status == False: #Variable du jeu "False" devient "True" et le jeu commence
        sleep(1) 
        print ("----------------------------")
        print ("Le Jeu commence !!!")           #permet de deboguer
        print ("----------------------------")
        sleep(1)
        status = True
        addseq() #lance la fonction qui commence le jeu
    elif status == True: #Variable du jeu lancé, devient "False" et lance la fonction lost()
        status = False
        sleep(1)
        print ("----------------------------")
        print ("Vous avez quitté le jeu")       #permet de deboguer
        print ("----------------------------") #Fonction lançant la fonction "le joueur a perdu ou a voulu arrêter le jeu
        lost()

        
##Fonction utilisant Pygame permettant de jouer du son------------------------------------------------------------------------------------------

def play_son(n=None): #expérimental pas encore testé
    """ Joue un son """
    pygame.mixer.music.load(n)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue
    
def play_son_credit(n=None):
    """Joue le son des Instructions"""
    play_son("son_credit.wav")
        

#EVENTS-----------------------------------------------------------------------------------------------------------------------------------------
"""Fait que tout au long du programme un bouton peut être appuyé et va lancer une fonction associée"""
GPIO.add_event_detect(33,GPIO.FALLING,callback=red,bouncetime=btime) #Bouton Rouge, lance la fonction associée à la LED rouge
GPIO.add_event_detect(35,GPIO.FALLING,callback=green,bouncetime=btime) #Bouton Verte, lance la fonction associée à la LED Verte
GPIO.add_event_detect(31,GPIO.FALLING,callback=yellow,bouncetime=btime) #Bouton Jaune, lance la fonction associée à la LED jaune
GPIO.add_event_detect(7,GPIO.FALLING,callback=start_stop,bouncetime=btime) #Bouton Start/Stop, lance la fonction associée
GPIO.add_event_detect(8,GPIO.FALLING,callback=play_son_credit,bouncetime=btime) #Bouton Instruction, lance la fonction associée
pygame.mixer.init() #initialise le mixer de pygame afin de jouer du son 

#PROGRAMME--------------------------------------------------------------------------------------------------------------------------------------

play_son("son_intro.wav") #joue le son au démarrage du progamme
print ("Appuyez sur le bouton <<START/STOP>>")
"""Le programme s'exécute lors de l'appui du bouton start stop"""

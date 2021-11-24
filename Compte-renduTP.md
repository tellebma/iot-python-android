

# TP 1 - Prise en main d’un micro-contrôleur

## Exercice 1. Étude du système

### Question 1. Rechercher les caractéristiques des diverses cartes en question et les micro-contrôleurs utilisés par chacune d’entre elles.

C8051F02x de SiliconLabs : 
- 8 bits
Arduino Uno : 
 - Mémoire flash: 32 kB
STM32 de ST Micro-electronics :

## Exercice 2. Documentations techniques

### Question 1. Rechercher les différents documentations techniques pour la carte Micro :bit et de ses composants. Est-ce que le site du distributeur (BBC) propose des documentations plus complètes que ceux des fabricants des composants ?

https://microbit-micropython.readthedocs.io/fr/latest/
https://microbit.org/get-started/user-guide/python/

### Question 2. Quels sont les outils dont j’aurais besoin pour passer de mon code source à un systèmefonctionnant avec la carte Micro-bit ?

## Exercice 3. Test du module

OK

## Exercice 4. Interaction avec les LEDs embarquées
```python
from microbit import *

while True:
    if button_a.is_pressed() :
        display.show("COUCOU ")
    else:
        display.show("SALUT")
```

Exercice 5. Capteur de température

```python
from microbit import *
while True:
    if temperature()>35:
        #alerte
        for i in range(0,5):
            for j in range(0,5):
                display.set_pixel(i,j,9)
        sleep(1000)
        display.show(temperature())
        
```


Exercice 6. Capteur accéléromètre
```python
left = 0
right = 0
while True:
    display.show(left)
    if accelerometer.was_gesture('left'):
        left+=1
```
Exercice 7. Capteur boussole
```python
while True:
    compass.calibrate()
    while compass.is_calibrated():
        #heading [0-360] => 0 - N
        display.show(Image.ALL_CLOCKS[(compass.heading()//30)])
```
# TP2 - Interaction avec capteurs et acteurs depuis un micro-contrôleur
## Exercice 1. Feu de circulation
```python
rouge = pin0
orange = pin1
vert = pin8
while True:
    rouge.write_digital(1)
    sleep(2000)
    rouge.write_digital(0)
    orange.write_digital(1)
    sleep(500)
    orange.write_digital(0)
    vert.write_digital(1)
    sleep(2000)
    vert.write_digital(0)
```



## Exercice 2 LED RGB Neopixel
```python
from microbit import *
import neopixel
np = neopixel.NeoPixel(pin0, 3)
while True:
    #init couleurs
    bleu = (0,0,255)
    blanc = (255,255,255)
    rouge = (255,0,0)
    drapeau = [bleu,blanc,rouge]
    for couleur in drapeau:
        np[0] = couleur
        np[1] = couleur#nous avons plusieurs neopixel.
        np[2] = couleur
        np.show()
        sleep(300)
```
 ## Exercice 3 Interface Série
```python
from microbit import *
uart.init(115200)
uart.write('hello world')
```
Lancer minicom sur le port USB via la commande `minicom -D /dev/ttyACM0`
## Exercice 4
```python
from microbit import i2c, display
import bme280

bme = bme280.BME280(i2c)
temp, pres, humi = bme.values()

while True:
    display.show(temp)
```
https://github.com/neliogodoi/MicroPython-BME280
Importer la version lowmem microbit sur la carte 
## Exercice 5. Écran mono-couleur
```python
from ssd1306 import initialize, clear_oled
from ssd1306_bitmap import show_bitmap

initialize()
clear_oled()
show_bitmap("microbit_logo")
```
https://github.com/CPELyon/microbit_ssd1306
- [ ] Verifier que l'écran est en bonne état...

```python
from microbit import temperature,i2c, display
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
import bme280
bme = bme280.BME280(i2c)
temp_sensor = bme.values()
initialize()
clear_oled()
add_text(0, 0, "Temperature:")
tempe = str(temperature())
add_text(5, 2, temp_capt)
add_text(5, 3, temp_sensor)

```
:Attention: Il faut réduire la taille des différents fichiers pour éviter les memory Error.

# TP 3:

## Exercice 1: Une application simple
Émetteur : 
```python
from microbit import *
import radio
radio.on()
while True:
    if button_a.was_pressed():
        radio.send("COUCOU")
```
Récepteur:
```python
from microbit import *
import radio
radio.on()
while True:
    recep = radio.receive()
    if recep:
        display.scroll(recep)
```
  
##### Question 1.  Quelle est la fonction que vous utilisez pour l’envoie des données par radio fréquence ?
in init le module radio. `radio.send()`
##### Question 2.Pouvez-vous choisir le destinataire ?
Non il n'est pas possible de choisir le destinataire.
##### Question 3.Quelle fréquence est utilisé pour la configuration de la carte RF ?
Entre 2.4Ghz et 2.5Ghz.
##### Question 4.Quelle est la taille maximale de chaque message envoyé/reçu ?
Maximum 251 caractères. 

## Exercice 2: Affichage température distante
Dans les applications de suivie de la température dans le but de régler automatiquement le chauffage, ondoit prendre en compte la température extérieur et intérieur.Dans cet exercice vous allez afficher la température distante (du deuxième micro :bit) ainsi que la température local pour pouvoir les comparer.
```python
from microbit import *
import radio
radio.config(channel=24)
radio.on()
while True:
    if button_a.is_pressed():#permet de ne pas spammer les radio.send()
        temp = str(temperature())
        display.scroll(temp)
        radio.send(temp)
```
        
## Exercice 3: Protocole de communication

La puce nRF51822 présente dans votre carte donne accès direct à la couche physique de la communication réseaux pour l’envoie de chaînes des bytes. Cependant, le protocole d’échange de données est à la charge du développeur, c’est à dire, vous !
##### Question 1. Proposez et implémentez un protocole simple de communication entre les puces nRF51822, en tenant compte les capacités restreintes d’un objet connecté : taille maximale de chaque message, nombre des messages échangés, consommation d’énergie, capacité de calcul,... 
Commencez d’abord par identifier les composants d’une trame : destinataire, source, données, somme de contrôle, ...(comme dans un modèle OSI)
Puis proposez un protocole simple pour une communication unicast, ensuite en intégrant des autres binômes, proposez une méthode pour adresser plusieurs micro-contrôleurs pour une diffusion dans votre réseau.
##### Question 2.Avez vous remarquez, que les messages échangés entre les micro-contrôleurs pourrait être écoutés par les autres cartes, modifiez le code de l’application simple pour protéger les messages échangés avec vos destinataires. Quel type d’attaque pourriez-vous faire pour altérer les trames échangés par vos collègues de classe ?

```python
# protocole simple (très simple)
from microbit import *
import radio
radio.config(channel=24)
radio.on()
moi = "1"

def get_message():
    recep = radio.receive()
    if recep:
        message_recup = recep.split("|")
        if message_recup[0] == moi:
            #le message s'addresse a moi.
            display.scroll(message_recup[2])
            return message_recup[1],message_recup[2]
    return 0,0

def send_message(dest,msg):
    to_send = dest+"|"+moi+"|"+msg
    radio.send(to_send)
    #return 1 pour send.
    return 1

while True:
    if button_a.was_pressed():#send
        display.set_pixel(2,2,9)
        send_message("2","Salut ca marche")
        sleep(100)
        display.clear()
        
    source,message = get_message()
    if source and message:
        display.scroll(message)
```

```python
#protocole moins simple


```








```python
#completement HS mais ... <3
from microbit import *
import radio
radio.config(channel=24)
radio.on()

def deplacement(direction,x=0,y=0):
    #directions possible:
    #haut et droite en str
    display.clear()
    if direction == "haut":
       x+=1
       if x>4:
           x=0
       display.set_pixel(x,y,9)
       
       return x,y
    elif direction == "droite":
       y+=1
       if y>4:
           y=0
       display.set_pixel(x,y,9)
       
       return x,y
    
x=0
y=0
while True:
    if button_a.was_pressed():
        x,y = deplacement("haut",x,y)
    elif button_a.was_pressed():
        x,y = deplacement("droite",x,y)
```
# Projet:
## Trop simple

```python
from microbit import *
import radio

def getFromTel():
    if button_a.was_pressed():
        return ""
    return 0   

def get():
    source,message = ProtocoleRadio().get_message()
    if source and message:
        if source == "2":
            if message == "sendMeTemp":
                ProtocoleRadio().send_message(source,"temp:"+str(temperature()))
                #Send Temp to source
                pass
            elif message == "changeLED":
                pass
            else:
                ProtocoleRadio().send_message(source,"Not Possible")

def ask(fonction:str):
    """
    fonction:
        sendMeTemp
    """
    ProtocoleRadio().send_message("2",fonction)
    #Demande latemperature a l'autre microbit
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio().get_message()
        if source and message:
            if source == "2": 
                return message
        if tentative > 200:
            ProtocoleRadio().send_message("2",fonction)
            tentative = 0

class Secu:
    def crypt(self,message:str,key:int=10):
        cryptedMessage = ""
        for lettre in message:
            key+=1
            cryptedMessage += chr(ord(lettre)+key)
        return cryptedMessage

    def decrypt(self,cryptedMessage:str,key:int=10):
        clearMessage = ""
        for lettre in cryptedMessage:
            key+=1
            clearMessage += chr(ord(lettre)-key)
        return clearMessage
        
    def hash(self,message:str):
        """
        hash de remplacement. #nul
        """
        checksum = 0
        for letter in message:
            checksum += ord(letter)
        return str(checksum)
    """
    import hashlib ne fonctionne pas :/
    def hash(self,message):
        return hashlib.md5(message.encode()).hexdigest()"""
    
    
class ProtocoleRadio:
    def __init__(self):
        self.moi = "1"
    
    def get_message(self):
        recep = radio.receive()
        if recep:
            message_recup = Secu().decrypt(recep).split("|")
            if message_recup[0] == self.moi:
                if Secu().hash(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
                    #le message s'addresse a moi.
                    return message_recup[1],message_recup[2]
        return 0,0

    def send_message(self,dest,msg):
        to_send_informations = dest+"|"+self.moi+"|"+msg
        to_send = to_send_informations+"|"+Secu().hash(to_send_informations)
        radio.send(Secu().crypt(to_send))
        #return 1 pour send.
        return 1


if __name__ == "__main__":
    radio.config(channel=24)
    radio.on()
    while True:
        get()
        demande = getFromTel()
        if demande:
            display.show(ask(demande))
            
```

### VM
#### Serveur Ubuntu: 
	id: **ubuntu** **server**
	pass: **password**

 depuis le serveur ubuntu, mettre une @IP  a la machine sur le même port que le Raspberry.
ex : 192.168.1.2 ( Raspberry  192.168.1.1) 
depuis le terminal : 
```bash 
ssh 192.168.1.1 -l pi
```
config :
```bash
sudo nano /etc/netplan/{tab}

:: 
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
      - 192.168.1.2/24
::
sudo netplan try
sudo netplan apply

```

#### Raspberry:
	id: **pi**
	pass: **raspberrycpe**



# Ecrit ton programme ici ;-)
```python
from microbit import *
import radio

def getFromTel():
    recep = uart.read()
    if recep:
        return str(recep,'utf-8')
    #Man pr debug.
    if button_a.was_pressed():
        return "t"
    if button_b.was_pressed():
        return "l"
    return 0   

def ask(fonction:str):
    """
    fonction:
        sendMeTemp
    """
    ProtocoleRadio().send_message("2",fonction)
    #Demande latemperature a l'autre microbit
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio().get_message()
        if source and message:
            if source == "2": 
                return message
        if tentative > 200:
            ProtocoleRadio().send_message("2",fonction)
            tentative = 0

class Secu:
    """
    Securité. vraiment très sur!
    Algo de césar remodifié car on est vraiement très chaud  ! 
    """
    def crypt(self,message:str,key:int=10):
        cryptedMessage = ""
        for lettre in message:
            key+=1
            cryptedMessage += chr(ord(lettre)+key)
        return cryptedMessage

    def decrypt(self,cryptedMessage:str,key:int=10):
        clearMessage = ""
        for lettre in cryptedMessage:
            key+=1
            clearMessage += chr(ord(lettre)-key)
        return clearMessage
        
    def hash(self,message:str):
        """
        hash de remplacement. #nul
        """
        checksum = 0
        for letter in message:
            checksum += ord(letter)
        return str(checksum)
    """
    import hashlib ne fonctionne pas :/
    def hash(self,message):
        return hashlib.md5(message.encode()).hexdigest()"""
    
    
class ProtocoleRadio:
    """
    protocole codé avec le cul.
    """
    def __init__(self):
        self.moi = "1"
    
    def get_message(self):
        recep = radio.receive()
        if recep:
            message_recup = Secu().decrypt(recep).split("|")
            if message_recup[0] == self.moi:
                if Secu().hash(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
                    #le message s'addresse a moi.
                    return message_recup[1],message_recup[2]
        return 0,0

    def send_message(self,dest,msg):
        to_send_informations = dest+"|"+self.moi+"|"+msg
        to_send = to_send_informations+"|"+Secu().hash(to_send_informations)
        radio.send(Secu().crypt(to_send))
        #return 1 pour send.
        return 1

if __name__ == "__main__":
    radio.config(channel=24)
    radio.on()
    uart.init(115200)
    while True:
        """
        Main Boucle
        """
        demande = getFromTel()
        if demande:
            message = ask(demande)
            sleep(500)
            uart.write(bytes(message,'utf-8'))
       

#//ETIENNE
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio

def get():
    source,message = ProtocoleRadio().get_message()
    if source and message:
        if source == "1":
            add_text(2, 3, "msg:" + message)         
            if message == "TL":
                ProtocoleRadio().send_message(source,str(temperature())+","+str(display.read_light_level()))                
            elif message == "LT":
                ProtocoleRadio().send_message(source,str(display.read_light_level())+","+str(temperature()))
            elif message == "t":
                ProtocoleRadio().send_message(source,str(temperature()))
            elif message == "l":
                ProtocoleRadio().send_message(source,str(display.read_light_level()))                
            else:
                pass

def ask(fonction:str):
    
    ProtocoleRadio().send_message("1",fonction)
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio().get_message()
        if source and message:
            if source == "1": 
                return message
        if tentative > 200:
            ProtocoleRadio().send_message("1",fonction)
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
        checksum = 0
        for letter in message:
            checksum += ord(letter)
        return str(checksum)    
    
    
class ProtocoleRadio:
    def __init__(self):
        self.moi = "2"
    
    def get_message(self):
        recep = radio.receive()
        if recep:
            recep = Secu().decrypt(recep)
            message_recup = recep.split("|")
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
    initialize(pinReset=pin0)
    clear_oled()
    radio.config(channel=24)
    radio.on()
    while True:
        add_text(2, 1, "temp: "+ str(temperature()))
        add_text(2, 2, "lum: " + str(display.read_light_level()))        
        get()

#//MAXIME
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

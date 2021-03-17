import socket
import threading    # pour pouvoir gérer plusieurs demandes en même temps

addresse_ip = input("Entrez l'adresse IP du serveur : ")
port = int(input("Entrer le numero de port : "))

# Entrer du pseudo du client
pseudo = input("Entrer votre Pseudo : ")

# Connexion au client

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((addresse_ip, port))

# Ecoute le serveur et envoie le Pseudo


def reception():
    while True:
        try:
            # SI on se connecte et qu on recoit un message du serveur
            message = client.recv(1024).decode('UTF-8')
            if message == 'ENVOI_TON_PSEUDO_MR_LE_CLIENT':
                client.send(pseudo.encode('UTF-8'))
            else:
                print(message)
        except:
            # on ferme la connexion si ya une erreur
            print("Erreur !!!!!")
            client.close()
            break


# Envoie du message au serveur
def envoi_mess():
    while True:
        message = '{}> {}'.format(pseudo, input(''))
        client.send(message.encode('UTF-8'))


# Commence la gestion des messages (reception et envoi message)
reception_thread = threading.Thread(target=reception)
reception_thread.start()

envoi_mess_thread = threading.Thread(target=envoi_mess)
envoi_mess_thread.start()

import socket
import threading  # pour pouvoir gérer plusieurs demandes en même temps


# Donnée de Connexion
addresse_ip = input("Entrez l'adresse IP du serveur : ")
port = int(input("Entrer le numero de port : "))

# Initialisation du socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Association du socket à une adresse local
server.bind((addresse_ip, port))

# commence à ecouter les connexions entrantes
server.listen()

# Initialisation de la liste qui va contenir les Clients et celle pour les surnoms
clients = []
pseudos = []

# max_size est un entier indiquant la taille maximale
# d octects pouvant etre recue en une fois : c est un entier
max_size = 4096


# Fonction qui envoie un message à tous les clients connectés
def envoi_A_Tlemonde(message):
    for client in clients:
        client.send(message)


# Fonction qui gere les messages des clients
def gereMessage(client):
    while True:
        try:
            # Envoi à tous le monde un message
            message = client.recv(max_size)
            envoi_A_Tlemonde(message)
        except:
            # Lorsqu'un client ferme la conversation , on le suppr
            index = clients.index(client)
            clients.remove(client)
            client.close()

            pseudo = pseudos[index]
            envoi_A_Tlemonde(
                '{} à quitter le chat :( '.format(pseudo).encode('UTF-8'))
            pseudos.remove(pseudo)
            break


# fonction qui recoit et ecoute
def reception():
    while True:
        # Permettre au serveur d'accepter de nouvellle connexion
        client, address = server.accept()
        print("Connecté au : {}".format(str(address)))

        # Sauvegarde du pseudo
        client.send('ENVOI_TON_PSEUDO_MR_LE_CLIENT'.encode('UTF-8'))

        pseudo = client.recv(max_size).decode('UTF-8')
        pseudos.append(pseudo)
        clients.append(client)

        # On ecrit et on send à tt le monde le pseudo
        print("Le pseudo est {}".format(pseudo))
        envoi_A_Tlemonde("{} a rejoint le chat :) ".format(
            pseudo).encode('UTF-8'))
        client.send('Connecté au serveur!'.encode('UTF-8'))

        # Commence la gestion des messages (plusieurs demande en mm temps)
        thread = threading.Thread(target=gereMessage, args=(client,))
        thread.start()


reception()


# Thread doc
# Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)

# Pas_interesse :)   groupe devrait être None; réservé pour une extension future lorsqu'une ThreadGroupclasse est implémentée
# target est l'objet appelable à appeler par la run()méthode. La valeur par défaut est None, ce qui signifie que rien n'est appelé.
# Pas_interesse :)   name est le nom du thread. Par défaut, un nom unique est construit sous la forme «Thread- N » où N est un petit nombre décimal.
# args est le tuple d'argument pour l'invocation cible. La valeur par défaut est ().
# Pas_interesse :)   kwargs est un dictionnaire d'arguments de mots clés pour l'invocation cible. La valeur par défaut est {}.

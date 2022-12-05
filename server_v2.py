import socket
import threading

HOST = 'localhost'
PORT = 55555  

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

with open('bans.txt', 'w') as f:
    f.write("")

def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    kick_name = message.decode('ascii')[5:]
                    aux1 = kick_name.split()[0]                  
                    kick_user(aux1)
                    broadcast(f'{aux1} foi expulso do chat\n'.encode('ascii'))
                else:
                     client.send('Comando nao executado'.encode('ascii'))
            elif message.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    ban_name = message.decode('ascii')[4:]
                    aux = ban_name.split()[0]                    
                    kick_user(aux)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{aux}\n')
                    broadcast(f'{aux} foi banido do chat'.encode('ascii'))
                else:
                    client.send('Comando nao executado'.encode('ascii'))
            else:
                broadcast(message)
        except:          
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do chat'.encode("ascii"))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado com {str(address)}')

        client.send('NICK'.encode('ascii')) 

        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        nicknames.append(nickname) 
        clients.append(client)
 
        print(f'O apelido do usuario e {nickname}')
        broadcast(f'{nickname} entrou no chat!\n'.encode('ascii'))
        client.send(f'Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('Voce foi expulso do chat pelo administrador'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} foi expulso pelo administrador'.encode('ascii'))

print("Servidor iniciado")
receive()
 

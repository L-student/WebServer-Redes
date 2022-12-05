import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('192.168.0.14', 55555))
        message = tkinter.Tk()
        message.withdraw()
        self.nickname = simpledialog.askstring("Apelido", "Escolha um apelido", parent = message)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target = self.gui_loop)
        receive_thread = threading.Thread(target = self.receive)
        
        gui_thread.start()
        receive_thread.start()
       
    
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "purple")
        
        self.chat_label = tkinter.Label(self.win, text = "Chat:", bg = "purple")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state = 'disabled')

        self.message_label = tkinter.Label(self.win, text = "Message:", bg = "purple")
        self.message_label.config(font = ("Arial", 12))
        self.message_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height = 3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text = "Send", command = self.write)
        self.send_button.config(font = ("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.client.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':   
                    self.client.send(self.nickname.encode('ascii'))
                    next_message = self.client.recv(1024).decode('ascii')
                    if next_message == 'PASS':
                        self.client.send(self.password.encode('ascii'))
                        if self.client.recv(1024).decode('ascii') == 'REFUSE':
                            print("Senha incorreta, conexao interrompida")   
                            stop_thread = True                     
                    elif next_message == 'BAN':
                        print('voce esta banido, conexão interrompida')
                        self.client.close()
                        stop_thread = True
                else:
                    if self.gui_done:
                        self.text_area.config(state = 'normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')
            except ConnectionAbortedError:
                break
            except:
                print("An error ocurred!")
                self.client.close() 
                break
    def write(self):
        
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        if message[len(self.nickname)+2:].startswith('/'):
            if self.nickname == 'admin':
                if message[len(self.nickname)+2:].startswith('/kick'):
                    self.client.send(f'KICK{message[len(self.nickname)+1+6:]}'.encode('ascii'))
                elif message[len(self.nickname)+2:].startswith('/ban'):
                    self.client.send(f'BAN{message[len(self.nickname)+1+5:]}'.encode('ascii'))               
            else:
                print("voce nao tem permissao para usar esse comando")    
        else: 
            self.client.send(message.encode('ascii'))
        self.input_area.delete('1.0', 'end ')

client = Client('192.168.0.14', 55555)
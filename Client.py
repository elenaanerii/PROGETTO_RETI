#!/usr/bin/env python3

#NERI ELENA MATRICOLA 0001098044

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
import sys

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            message_list.insert(tkt.END, message)
            message_list.see(tkt.END)
        except Exception as e:
            print("Errore durante la ricezione del messaggio: ", e)
            break

def stop():
    try:
        check_window_count()
        window.destroy()
    except tkt.TclError:
        pass
    try:
        client_socket.close()
    except:
        pass
        

def closeWindow(event=None):
    my_msg.set("{quit}")
    send()

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    try:
        if msg == "{quit}":
            client_socket.send(bytes(msg, "utf8"))
            stop()
        else:
            client_socket.send(bytes(msg, "utf8"))
    except ConnectionResetError:
        stop()

def check_window_count():
    global open_windows
    open_windows -= 1
    # Controlla il numero di finestre aperte
    if open_windows == 0:
        sys.exit(0)

def start():
    global client_socket, window, message_list, my_msg, open_windows
    open_windows=1
    HOST = 'localhost'
    PORT = 53000

    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
    except Exception as e:
        print("Errore durante la connessione al server: ", e)
        return
    
    window = tkt.Tk()
    window.title("CHATROOM CONDIVISA") 
    messages_frame = tkt.Frame(window)
    my_msg = tkt.StringVar()
    my_msg.set(" ")
    scrollbar = tkt.Scrollbar(messages_frame)
    message_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="lightgrey", fg="black", font=("Helvetica", 12))
    scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
    message_list.pack(side=tkt.LEFT, fill=tkt.BOTH, expand=True)
    messages_frame.pack(padx=10, pady=10, expand=True, fill=tkt.BOTH)
    entry_field = tkt.Entry(window, textvariable=my_msg, font=("Helvetica", 12))
    entry_field.bind("<Return>", send)
    entry_field.pack(padx=10, pady=10, fill=tkt.X)
    send_button = tkt.Button(window, text="Invio", command=send, font=("Helvetica", 12), bg="blue", fg="white")
    send_button.pack(pady=10)
    window.protocol("WM_DELETE_WINDOW", closeWindow)
    open_windows +=1

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkt.mainloop()

if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        print("Errore durante l'esecuzione del client: ", e)
    finally:
        stop()
        sys.exit(0)
import os, time

from whatsender import WhatSender

CURRENT_PATH = os.path.abspath( os.path.dirname(__file__) )
ROOT_PATH = os.path.dirname( CURRENT_PATH )


def elapsed_time(start_time):
    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

def whatsapp_sender():
    ws = WhatSender(chromedriver=os.path.join(CURRENT_PATH, "chromedriver"))

    # list = [
    #     {'full_name': 'Roberto West', 'phone': '3816168251', 'name': 'Roberto', 'surname': 'West'},
    # ]
    # ws.PassContactList(list)
    ws.ContactList(os.path.join(CURRENT_PATH, "listado.csv"))

    if ws.contacts:
        ws.Open()
    
        try:
            # ws.SendMessage("Hola {nombre}\n
            #                 Somos *Lubre SRL* tu empresa de YPF Agro.\n
            #                 \n
            #                 No dudes en llamarnos.")
            ws.SendImage(os.path.join(CURRENT_PATH, "imagen.png"))
        finally:
            ws.Close()


if __name__ == "__main__":
    start_time = time.time()
    whatsapp_sender()
    print("Tiempo transcurrido: {}".format( elapsed_time(start_time)) )

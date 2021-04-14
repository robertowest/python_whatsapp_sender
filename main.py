from whatsender import WhatSender

ws = WhatSender()

list = [
    {'full_name': 'Roberto West', 'phone': '3816168251', 'name': 'Roberto', 'surname': 'West'},
]
ws.PassContactList(list)
# ws.ContactList('contacts.csv')

try:
    ws.SendMessage("Hola {nombre}\nSomos *Lubre SRL* tu empresa de YPF Agro.\n\nNo dudes en llamarnos.")
    # ws.SendImage("/home/roberto/Imágenes/django-icon-0.jpg")
finally:
    ws.Close()

import csv, os, time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class WhatSender:
    def __init__(self, chromedriver="/usr/bin/chromedriver"):
        self.contacts = []
        self.chromedriver = chromedriver
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('lang=es')
        self.options.add_argument('--window-size=800,700')


    def Open(self):
        self.driver = webdriver.Chrome(executable_path=self.chromedriver, options=self.options)
        self.driver.get('https://web.whatsapp.com/')
        wait = WebDriverWait(self.driver, 20)
        input(str("Lea el código QR\nCuando aparezca la ventana de WhatsApp pulse [enter] para continuar ... "))


    def ContactList(self, csvfile='listado.csv'):
        """Pasamos el archivo CSV con la información de contactos"""
        if os.path.isfile(csvfile):
            with open(csvfile, mode='r', encoding='utf8') as openfile:
                # fieldnames=['full_name', 'phone', 'name', 'surname']
                rows = csv.DictReader(openfile, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in rows:
                    self.contacts.append(dict(row))

            if self.contacts == []:
                print("No existe listado de contactos para enviar mensaje.")
                return None
        else:
            print("No existe el archivo {}".format(csvfile))


    def PassContactList(self, contactlist=[]):
        """
        Pasamos una lista de contactos con formato
        full_name, phone, name, surname
        list = [
                 {
                    'full_name': 'Roberto West', 
                    'phone': '3816168251', 
                    'name': 'Roberto', 
                    'surname': 'West'
                 },
               ]
        """
        self.contacts = contactlist


    def SendMessage(self, message):
        if self.contacts == []:
            # print("No existe listado de contactos para enviar mensaje.")
            return None

        # localizamos el cuadro de búsqueda de contacto
        if self.__person_box():
            for contact in self.contacts:
                print( "Enviando mensaje a: {} ({})".format(contact['full_name'], contact['phone']) )
                if self.__search_person(contact['phone']):
                    self.__multiline(message.replace('{nombre}', contact['name']))
                    time.sleep(3)
                else:
                    print( "    No existe el contacto: {} ({})" \
                           .format(contact['full_name'], contact['phone']) )
        else:
            print("No existe el cuadro de búsqueda de contactos.")


    def SendImage(self, message):
        if self.contacts == []:
            # print("No existe listado de contactos para enviar mensaje.")
            return None

        # localizamos el cuadro de búsqueda de contacto
        if self.__person_box():
            for contact in self.contacts:
                print( "Enviando mensaje a: {} ({})".format(contact['full_name'], contact['phone']) )
                if self.__search_person(contact['phone']):
                    # adjuntar imagen y enviar
                    try:
                        self.__attachment_box()
                        self.__image_box(message)
                        self.__send_box()
                        time.sleep(4)
                    except Exception as e: 
                        print( "        Error: {}".format(e) )
                else:
                    print( "    No existe el contacto: {} ({})" \
                           .format(contact['full_name'], contact['phone']) )
        else:
            print("No existe el cuadro de búsqueda de contactos.")


    def Close(self):
        self.driver.quit()


    # staticmethod (decorador)
    def __person_box(self):
        # cuadro de búsqueda de contacto
        try:
            xpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
            self.person_box = WebDriverWait(self.driver, 3).until(lambda x:x.find_element_by_xpath(xpath))
            return True
        except:
            self.person_box = None
            return False

    def __search_person(self, searchtext):
        self.person_box.clear()
        ActionChains(self.driver).click(self.person_box).perform()
        ActionChains(self.driver).send_keys(searchtext).perform()
        ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        try:
            # si el elemento existe, significa que el contacto no existe
            xpath = '//*[@id="pane-side"]/div[1]/div/span'
            element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_xpath(xpath))
            return False
        except:
            # self.person_box.send_keys(Keys.ENTER)
            return True

    def __attachment_box(self):
        xpath = '//div[@title="Adjuntar"]'
        obj = WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_xpath(xpath))
        obj.click()

    def __image_box(self, message):
        xpath = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
        obj = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(xpath))
        obj.send_keys(message)

    def __send_box(self):
        xpath = '//span[@data-icon="send"]'
        obj = WebDriverWait(self.driver, 20).until(lambda x: x.find_element_by_xpath(xpath))
        obj.click()

    def __multiline(self, message):
        print("multilinea")
        for line in message.split("\n"):
            ActionChains(self.driver).send_keys(line).perform()
            ActionChains(self.driver).key_down(Keys.SHIFT) \
                                     .key_down(Keys.ENTER) \
                                     .key_up(Keys.SHIFT) \
                                     .key_up(Keys.ENTER).perform()
        ActionChains(self.driver).send_keys(Keys.RETURN).perform()

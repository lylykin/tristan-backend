from subscribeData import PBdataListener
from time import sleep

# Récupération de l'écoute de modification PocketBase
pb_data_listener = PBdataListener()


while True :
    pb_data_listener.subscribe_sparkfun()
    print('test')
    sleep(3)
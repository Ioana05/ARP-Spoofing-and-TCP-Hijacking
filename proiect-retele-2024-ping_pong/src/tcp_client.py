# TCP client
import socket
import logging
import time
import sys

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2' # ip server
server_address = (adresa, port)

try:
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)
    # odata ce ne-am conectat incepem sa trimitem mesaje
    counter = 0
    while True:
    	counter += 1
    	time.sleep(2) # trimitem odata la 2 secunde
    	mesaj = "Hello server, nr: " + str(counter) 
    	sock.send(mesaj.encode('utf-8'))
    	data = sock.recv(1024) #primim mesajul de la server
    	logging.info('Content primit de la server: "%s"', data)

finally:
    logging.info('closing socket')
    sock.close()

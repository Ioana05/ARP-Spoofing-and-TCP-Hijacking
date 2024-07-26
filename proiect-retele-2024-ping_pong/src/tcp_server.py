# TCP Server
import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)
# bind socket la portul 10000
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(1) # asteptam o singura (2) conexiune

logging.info('Asteptam o conexiune...')
conexiune, address = sock.accept()
logging.info("Handshake cu %s", address)

# odata ce am facut 3-way handshake cu clientul, 
# incepem sa trimitem mesaje random
counter = 0
while True:
    counter += 1
    time.sleep(2)
    data = conexiune.recv(1024) # citim din buffer
    logging.info('Content primit: "%s"', data)
    # trimitem cate un numar
    mesaj = "Primim de la server mesajul " + str(counter)
    conexiune.send(mesaj.encode('utf-8'))

# inchidem conexiunea si socketul la final
conexiune.close()
sock.close()

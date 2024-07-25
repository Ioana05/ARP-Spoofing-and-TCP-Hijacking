# ARP-Spoofing-and-TCP-Hijacking

## Used architecture
![image](https://github.com/user-attachments/assets/b1dd4570-a394-4a7c-aac3-266730cf1b75)


## Arp-Spoofing 🕵️
<b> Address Resolution Protocol(ARP) </b> is a protocol or procedure that connects an ever-changing Internet Protocol address to a fixed physical machine address, also known as a <b> media access control(MAC) </b> address, in a <b> local-area network(LAN) </b> . <b> ARP Spoofing </b> is an attack in which a malicious actor sends falsified ARP messages over a local area network. This results in the linking of an attacker's MAC address with the IP address of a legitimate computer or server on the network.  

The strategy is to create a 'poisoned' ARP in which the source IP will be the spoof IP and the source MAC address will be the attacker's MAC address. These packets will be constantly sent until the victim saves this association in the ARP table. Because in the architecture I used, the attacker is between SERVER and ROUTER, I used two threads to send packets simultaneously to both.

## How to run it:
⚠️ In the code there are already written the IP address of the victim, the spoof_ip, and the MAC address of the attacker. These need to be changed if you're working on other containers instead of those from the given architecture.
  <li> Open the victim's container(in our case is the server) and the man in the middle container</li>
  <li> Run the script from the man in the middle container </li>
  <li> Run in the man in the middle container "tcpdump -SntvXX -i any"</li>
  <li> Run in the server container(victim) " wget http://old.fmi.unibuc.ro (or any other address) ". The wget command will make a HTTP request to the specifies URL and download the HTML content of the web page located at that URL.   </li>
  <li> If the middlle man can see HTML content from the request , congrats, your ARP-Spoofing attack worked! 😎 </li>


## TCP-Hijacking
TCP/IP hijacking is a man-in-the-middle attack where an user can gain access to another user's or client's authorized network connection. After hijackinga TCP/IP session, an attacker is able to easily read and modify the transferred packets and the hacker is also able to send its own request to the user. For this attack, the above project was used to "sneak" the middle man in the network.

This project was made in collaboration with @ana-rosu and @iam-mj👧🏻👧🏻👧🏻

## How does TCP-Hijacking work?
Firstly, we will use the ARP-spoofing attack to get the packets from either the server, the client, or the connection between them. After we've managed to do this, the main thing behind TCP Hijacking is to correctly calculate the SEQ and ACK values for the next packet that the real target would send. You can find more about TCP protocol and why do we need to calculate this values, here:  https://medium.com/@R00tendo/tcp-connection-hijacking-deep-dive-9bbe03fce9a9

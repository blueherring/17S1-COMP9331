import socket;
import time;
import sys;

##if len(sys.argv) != 3:
##    print("Required arguments:host and port")
##    sys.exit()
    
ipaddress = sys.argv[1];
port = sys.argv[2];

for i in range(1,11):
    try:
        message = "PING {} {}".format(i, int(time.time()))
        sendtime = time.time()
        message = message.encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(message, (ipaddress, int(port)))
        received = sock.recvfrom(1024)
        receivetime = time.time()
        print ("pint to {}, seq = {}, rtt = {:.2f} ms".format(ipaddress, i, (receivetime - sendtime) * 1000))
    except Exception as exception:
        pass

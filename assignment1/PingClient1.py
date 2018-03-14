import socket;
import time;
import sys;

targetIp = sys.argv[1];
targetPort = sys.argv[2];

for i in range (1, 11) :
	try :
		msgSent = "PING {} {}".format(i, int(time.time()));
		sendTime = time.time();
		msgSent = msgSent.encode();
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		sock.settimeout(1);
		sock.sendto(msgSent, (targetIp, int(targetPort)));
		msgReceived = sock.recvfrom(1024);
		receiveTime = time.time();
		print ("pint to {}, seq = {}, rtt = {:.2f} ms".format(targetIp, i, (receiveTime - sendTime) * 1000));
	except Exception as e:
		pass;
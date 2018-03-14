import sys;
import socket;
import re;

#host, port = '', 8888;
host = '';
port = int(sys.argv[1]);

listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
listenSocket.bind((host, port));
listenSocket.listen(1);

print ('Web service online.');
print ('Port: ', port);

while True:
	clientConnection, clientAddress = listenSocket.accept();
	request = clientConnection.recv(1024);
	request = request.decode();
	print (request);

	pattern = re.compile(r'GET (.*) HTTP[ ]?/[ ]?(\d\.\d|\d)');
	parsedRequest = pattern.split(request);
	try :
		requestFileDirectory = parsedRequest[1];
		if (requestFileDirectory == '/') :
			requestFileDirectory = 'index.html';
		else :
			requestFileDirectory = requestFileDirectory[1:];
		requestFile = open(requestFileDirectory, 'r');
		response = """\
HTTP/1.1 200 OK

""" + requestFile.read();
	except :
		response = """\
HTTP/1.1 404 Not Found

404 Not found\n
Oops, I can't find the file: 
""" + parsedRequest[1];
	clientConnection.sendall(response.encode());
	clientConnection.close();
	print ('========================');
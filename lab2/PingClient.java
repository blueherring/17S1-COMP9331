import java.io.*;
import java.net.*;
import java.util.*;
import java.text.SimpleDateFormat;
/*
 * Client Server to send ping to PingServer.
 * The server sends 10 packets.
 * When a packet in, the server simply print RTT.
*/

public class PingClient{


	public static void main(String[] args) throws Exception{

		//get command line argument.
		if (args.length != 2) {
			System.out.println("Required arguments: Address Port");
			return;
		}
		int port = Integer.parseInt(args[1]);
		InetAddress serveraddress = InetAddress.getByName(args[0]);
		String ip = serveraddress.getHostAddress();



		// Create a datagram socket for receiving and sending UDP.
		// Through the port and address specified on the command lines.
		DatagramSocket soc = new DatagramSocket(1258);
		
		soc.connect(serveraddress, port);
		//catch(IllegalArgumentException e){System.out.println("IAE");}

		//processing loop.
		for(int i=0; i<10; i++){
			//create a datagram packet to process UDP packet.
			DatagramPacket respond = new DatagramPacket(new byte[1024], 1024);
			
			//record sending time
			Date sendtime = new Date();

			//send a UDP packet.
			byte[] buf = {1,1,1,1,1,1,1};
			DatagramPacket sending = new DatagramPacket(buf, buf.length, serveraddress, port);
			try{soc.send(sending);}

			catch(PortUnreachableException f){
				System.out.println("IOError");
			}

			//wait 1 second to receive reply
			try{
				soc.setSoTimeout(1000);
				soc.receive(respond);
			//record receiving time if get responding 
				Date receivetime = new Date();
				long rtt = receivetime.getTime() - sendtime.getTime();
				printData(i, ip, rtt);
			}
			catch(Exception g){
				System.out.println("ping to " + ip + ", seq = " + i + " Loss");
			}
			
			//String outputtime = outputtimeformat.format(receivetime);
			//Print the received data.

		}


	}



	private static void printData(int seq, String ip, long rtt) throws Exception{
		

		System.out.println("ping to " + ip + ", seq = " + seq + ", rtt = " + rtt + " ms");


	}





}
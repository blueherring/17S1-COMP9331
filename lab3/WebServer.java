import java.net.*;
import java.io.*;

public class WebServer  {


	public static void main(String[] args) throws IOException{
		PrintStream out;
		InputStream input;
		ServerSocket server;
		if(args.length == 1){
			server = new ServerSocket(Integer.parseInt(args[0]));
		}
		else{
			server = new ServerSocket(80);
		}
		while(true){
			Socket client = server.accept();
			Socket socket;
			input = socket.getInputStream();
			out = new PrintStream(socket.getOutputStream());
			
			BufferedReader in = new BufferedReader(new InputStreamReader(input));
			String inputContent = in.readLine();
			String request[] = inputContent.split(" ");
			String fileName = request[1];
			
			File file = new File(fileName);
			if (file.exists()){
				InputStream incontent = new FileInputStream(file);
				byte content[] = new byte[(int) file.length()];
				incontent.read(content);
				out.println("HTTP/1.0 200 OK");
				out.write(content);
				out.flush();
				incontent.close();
			}
			else{
				String msg1="<html><head><title>Not Found</title></head><body><h1>Error 404-file not found</h1></body></html>";
		        out.println("HTTP/1.0 404 no found");
		        out.println("Content_Type:text/html");
		        out.println("Content_Length:"+msg1.length()+2);
		        out.println("");
		        out.println(msg1);
		        out.flush();
			}
		}
		
	}
}

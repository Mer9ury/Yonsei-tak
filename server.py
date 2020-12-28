from multiprocessing import Queue
import time
import socket, threading
import turtle

IP='172.20.5.205'
PORT=35355

turtle.setup(800, 600)
t=turtle.Turtle()
t.hideturtle()
t.penup()
t.setposition(-330, 0)


###executer
class Executer:
    
    def __init__(self, tcpServer):
        self.andRaspTCP = tcpServer
    
    def startCommand(self, command):
 
        if command=='refresh\n':
            self.andRaspTCP.sendAll(format(50-(int(time.time()-atime)//60), '>2')+' '*32+format(50-(int(time.time()-btime)//60), '>2')+'\n')
        elif command=='1\n':
            self.andRaspTCP.sendAll(format(50-(int(time.time()-atime)//60), '>2')+'\n')
        elif command=='2\n':
            self.andRaspTCP.sendAll(format(50-(int(time.time()-btime)//60), '>2')+'\n')
        else:
            self.andRaspTCP.sendAll('er\n')

###tcpserverthread
 
class TCPServerThread(threading.Thread):
        
    def __init__(self, commandQueue, tcpServerThreads, connections, connection, clientAddress):
        threading.Thread.__init__(self)
 
        self.commandQueue = commandQueue
        self.tcpServerThreads = tcpServerThreads
        self.connections = connections
        self.connection = connection
        self.clientAddress = clientAddress
 
    def run(self):
        try:
            while True:
                data = self.connection.recv(1024).decode()
 
                # when break connection
                if not data:
                    print ('tcp server :: exit :',self.connection)
                    break
 
 
                print ('tcp server :: client :', data)
                self.commandQueue.put(data)
        except:
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)
        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)
 
    def send(self, message):
        print ('tcp server :: ',message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
             pass


###tcpserver
class TCPServer(threading.Thread):
    def __init__(self, commandQueue, HOST, PORT):
        threading.Thread.__init__(self)
 
        self.commandQueue = commandQueue
        self.HOST = HOST
        self.PORT = PORT
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.HOST, self.PORT))
        self.serverSocket.listen(1)
 
        self.connections = []
        self.tcpServerThreads = []
 
    def run(self):
        try:
            while True:
                print ('tcp server :: server wait...')
                connection, clientAddress = self.serverSocket.accept()
                self.connections.append(connection)
                print ("tcp server :: connect :", clientAddress)
    
                subThread = TCPServerThread(self.commandQueue, self.tcpServerThreads, self.connections, connection, clientAddress)
                subThread.start()
                self.tcpServerThreads.append(subThread)
        except:
            print ("tcp server :: serverThread error")
 
    def sendAll(self, message):
        try:
            self.tcpServerThreads[0].send(message)
        except:
            pass


###main
atime, btime=time.time(), time.time()

##RASP
def rasp():
    global atime, btime
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    while True:
        data=sock.recv(200).decode()
        if data=='A':
            atime=time.time()
            t.clear()
            t.write('1번 세탁기 태그됨', font=('Time New Romans', 50, 'bold'))
        elif data=='B':
            btime=time.time()
            t.clear()
            t.write('2번 세탁기 태그됨', font=('Time New Romans', 50, 'bold'))
        time.sleep(1)
        

t=threading.Thread(target=rasp, args=())
t.start()

##APP
# make public queue
commandQueue = Queue()
 
# init module
andRaspTCP = TCPServer(commandQueue, "", PORT)
andRaspTCP.start()
 
 
# set module to executer
commandExecuter = Executer(andRaspTCP)
 
 
while True:
    try:
        command = commandQueue.get()
        commandExecuter.startCommand(command)
    except:
        pass

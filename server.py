# import socket
# import pickle


# HEADERSIZE=10
# s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(),1234))
# s.listen(5)

# while True:
# 	clientsocket,address=s.accept()
# 	print(f"Connection established with {address} address")
# 	d={1:"hey",2:"There"}
# 	msg=pickle.dumps(d)
# 	msg=bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg
# 	clientsocket.send(msg)

# 	# while True:
# 	# 	time.sleep(3)
# 	# 	msg=f'The time is! {time.time()}'
# 	# 	msg=f'{len(msg):<{HEADERSIZE}}'+msg
# 	# 	clientsocket.send(bytes(msg,"utf-8`1"))

import socket
import select

HEADER_LENGTH=10
IP='127.0.0.1'
PORT=1234

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list=[server_socket]
clients={}

def receive_msg(client_socket):
	try:
		message_header=client_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False
		msglen=int(message_header.decode('utf-8'))
		return {"header": message_header, "data": client_socket.recv(msglen)}
	except:
		return False

while True:
	read_sockets, _, exception_sockets=select.select(sockets_list, [], sockets_list)

	for notified_socket in read_sockets:
		if notified_socket==server_socket:
			client_socket,client_address=server_socket.accept()
			user=receive_msg(client_socket)
			if user is False:
				continue

			sockets_list.append(client_socket)

			clients[client_socket]=user
			print(f"Accepted  new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

		else:
			message=receive_msg(notified_socket)

			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			user=clients[notified_socket]
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user['header']+user['data']+message['header']+message['data'])

	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]